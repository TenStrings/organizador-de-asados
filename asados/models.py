from django.db import models
from django.core.validators import validate_unicode_slug
import sys
from functools import partial
from collections import defaultdict
from abc import ABC,abstractmethod

class User(models.Model):
    name = models.CharField(max_length=128, primary_key=True,
                            validators=[validate_unicode_slug])
    def __str__(self):
        return self.name

class Asado(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Organizador')
    attendee = models.ManyToManyField(User, through='Invitation',related_name='Invitados')
    datetime = models.DateTimeField()
    place = models.CharField(max_length=128, default='')

    @property
    def estimated_cost(self):
        estimated_by_items = sum([ assignment.estimated_cost() for
                                    assignment in self.shop_list.all()])
        return "$ %s" % estimated_by_items

    class Meta:
        ordering = ['datetime']

class Invitation(models.Model):
    #TODO: remove?
    invite = models.ForeignKey(User, on_delete=models.CASCADE)
    asado = models.ForeignKey(Asado, on_delete=models.CASCADE)

class Supply(models.Model):
    VALID_OPTIONS = (
        ('drink', 'Drink'),
        ('food', 'Food'),
    )

    kind = models.CharField(max_length=64, choices=VALID_OPTIONS)
    description = models.CharField(max_length=128,unique=True)
    estimated_cost = models.DecimalField(max_digits=7,decimal_places=2)

    @property
    def cost(self):
        return "$%s" % self.estimated_cost

    def __str__(self):
        return self.description + ' ' + self.cost

class Assignment(models.Model):

    designated_user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=256, default='')
    fullfilled = models.BooleanField(default=False)
    asado = models.ForeignKey(Asado, related_name='shop_list')
    required_supply = models.ForeignKey(Supply,on_delete=models.CASCADE)
    required_quantity = models.IntegerField(default=0)

    def estimated_cost(self):
        return self.required_quantity * self.required_supply.estimated_cost

    def finished_with(self,quantity):

        rule = AssignmentValidationRule.rule_for(
                self.required_supply
            )
        self.fullfilled = rule.fullfills_for(self,quantity)
        self.save()

class AssignmentValidationError(Exception):
    def __init__(self,message):
        self.message = message

class AssignmentValidationRule(ABC):

    @classmethod
    def rule_for(cls,a_supply):
        try:
            return next(
                rule for rule in cls.__subclasses__() if
                rule.works_for(a_supply)
            )
        except StopIteration as e:
            raise AssignmentValidationError(
                'You must provide a rule for'
                'this kind of supply ' + a_kind_of_supply
            )
    @classmethod
    @abstractmethod
    def works_for(a_supply):
        pass

    @abstractmethod
    def fullfills_for(an_assignment,a_quantity):
        pass

class FoodAssignmentValidationRule(AssignmentValidationRule):
    def works_for(a_supply):
        return a_supply.kind == 'food'

    def fullfills_for(an_assignment,a_quantity):
        if a_quantity == an_assignment.required_quantity:
            return True
        else:
            ERROR_MESSAGE = (
            'Deben confirmarse todas las unidas requeridas de comida'
            )
            raise AssignmentValidationError(ERROR_MESSAGE)

class DrinkAssignmentValidationRule(AssignmentValidationRule):
    def works_for(a_supply):
        return a_supply.kind == 'drink'

    def fullfills_for(an_assignment,a_quantity):
        return True
