from django import forms
from functools import partial
from .models import Asado,User,Item
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
