from django.db import models
import datetime

class User(models.Model):
    name = models.CharField(max_length=128, primary_key=True)
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
    invite = models.ForeignKey(User, on_delete=models.CASCADE)
    asado = models.ForeignKey(Asado, on_delete=models.CASCADE)

class Item(models.Model):
    description = models.CharField(max_length=128)
    estimated_cost = models.DecimalField(max_digits=7,decimal_places=2)
    designated_user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    comment = models.CharField(max_length=256, default='')
    ready = models.BooleanField(default=False)
    #No estoy seguro de si hacer esto o ManyToMany
    asado = models.ForeignKey(Asado, related_name='items')

    def __str__(self):
        if self.ready:
            ready = 'Listo'
        else:
            ready = 'Falta'

        return str(self.description) + ' ' + str(self.estimated_cost) + ' ' + ready
