from django.db import models
from django.core.validators import validate_unicode_slug
import datetime
import sys

class User(models.Model):
    name = models.CharField(max_length=128, primary_key=True,
                            validators=[validate_unicode_slug])
    def __str__(self):
        return self.name

class Asado(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Organizador')
    attendee = models.ManyToManyField(User, through='Invitation',related_name='Invitados')
    datetime = models.DateTimeField()
    estimated_cost = models.DecimalField(max_digits=7,decimal_places=2)
    place = models.CharField(max_length=128, default='')

    @property
    def cost(self):
        return "$%s" % self.estimated_cost

    class Meta:
        ordering = ['datetime']

class Invitation(models.Model):
    #TODO: remove?
    invite = models.ForeignKey(User, on_delete=models.CASCADE)
    asado = models.ForeignKey(Asado, on_delete=models.CASCADE)

class Supply(models.Model):
    #Podría usar __subclasses__ y hacer un find_first alla Hernán también (?)
    VALID_OPTIONS = (
        ('drink', 'Drink'),
        ('food', 'Food'),
    )

    kind = models.CharField(max_length=64, choices=VALID_OPTIONS)
    description = models.CharField(max_length=128,unique=True)
    estimated_cost = models.DecimalField(max_digits=7,decimal_places=2)

    def validate(self,an_assignment,quantity):
        raise NotImplementedError("You must provide a subclass of Supply with a definition for validate")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.kind:
            self.__class__ = getattr(sys.modules[__name__], self.kind.title() + self.__class__.__name__)

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

    def finished_with(self,quantity):
        self.required_supply.validate(self,quantity)

    def validate_for_food(self,quantity):
        if quantity == self.required_quantity:
            self.fullfilled = True
        #else return error?

    def validate_for_drink(self,quantity):
        self.fullfilled = True



class DrinkSupply(Supply):
    def validate(self,an_assignment,quantity):
        an_assignment.validate_for_drink(quantity)
    class Meta:
        proxy = True


class FoodSupply(Supply):
    def validate(self,an_assignment,quantity):
        an_assignment.validate_for_food(quantity)
    class Meta:
        proxy = True
