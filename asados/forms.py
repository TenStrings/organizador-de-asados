from django import forms
from functools import partial
from .models import Asado,User,Item,Invitation
from datetimewidget.widgets import DateTimeWidget

class AddAsadoForm(forms.ModelForm):
    class Meta:
        model = Asado
        dateTimeOptions = {
        'format': 'dd/mm/yyyy HH:ii P',
        'autoclose': True,
        'showMeridian' : True
        }
        widgets = {
            #Use localization and bootstrap 3
            'datetime': DateTimeWidget( attrs={'id':"yourdatetimeid"},
            bootstrap_version=3,
            usel10n=True,
            options=dateTimeOptions)
        }
        labels = { 'organizer' : 'Organizador',
                   'attendee'  : 'Invitados',
                   'datetime'  : 'Fecha',
                   'estimated_cost': 'Costo estimado',
                   'place' : 'Lugar' }

        fields = ['organizer','attendee','datetime','estimated_cost','place']

    class Media:
        js = ('asados/javascript/asado-form.js',)

    def save(self, *args, **kwargs):
        new_asado = super().save(*args,**kwargs,commit=False)
        new_asado.save()
        if self.is_valid():
            for user_name in self.cleaned_data['attendee'].all():
                user = User.objects.get(name=user_name)
                invitation = Invitation.objects.create( invite=user,
                                                        asado=new_asado)
        return new_asado

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        labels = { 'name' : 'Nombre' }
        fields = ['name']

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        labels = { 'description' : u'Descripción',
                    'estimated_cost' : 'Costo estimado',
                    'designated_user' : 'Invitado designado',
                    'comment' : 'Comentarios'}
        fields = ['description','estimated_cost','designated_user','comment']
