from django.db import models
from django.core.validators import validate_unicode_slug
import sys
from functools import partial
from collections import defaultdict

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
        estimated_by_items = sum([ assignment.estimated_cost for
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

    def validate(self,an_assignment,quantity):
        raise NotImplementedError("You must provide a subclass of Supply with a definition for validate")

    @property
    def cost(self):
        return "$%s" % self.estimated_cost

    def __str__(self):
        return self.description + ' ' + self.cost

class AssignmentValidationError(Exception):
    def __init__(self,message):
        self.message = message

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
        kind_of_supply = self.required_supply.kind
        rule = self.rule_for(kind_of_supply)
        rule(self,quantity)
        self.save()

    def rule_for(self,a_kind_of_supply):
        try:
            return self.__class__.validation_rules[a_kind_of_supply]
        except KeyError as e:
            raise AssignmentValidationError('Unsupported kind of supply')

    #Esto se puede abstraer en clases

    def rule_for_food(self,quantity):
        if quantity == self.required_quantity:
            self.fullfilled = True
        else:
            error_message = 'Deben confirmarse todas las unidas requeridas de comida'
            raise AssignmentValidationError(error_message)

    def rule_for_drink(self,quantity):
        self.fullfilled = True

    validation_rules = {
            'food': rule_for_food,
            'drink': rule_for_drink,
    }
