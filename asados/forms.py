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

        fields = ['organizer','attendee','datetime','estimated_cost','place']

    class Media:
        js = ('asados/javascript/asado-form.js',)

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description','estimated_cost','designated_user','comment']
