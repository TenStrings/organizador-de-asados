from django import forms
from functools import partial
from .models import Asado,User,Assignment,Supply,Invitation
from datetimewidget.widgets import DateTimeWidget
from django.utils import timezone

class AddAsadoForm(forms.ModelForm):
    class Meta:
        model = Asado
        dateTimeOptions = {
        'format': 'dd/mm/yyyy HH:ii P',
        'autoclose': True,
        'showMeridian' : True,
        'startDate': str(timezone.now())
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
                   'place' : 'Lugar' }


        def clean_datetime(self):
            datetime = self.cleaned_data['datetime']
            if datetime < timezone.now():
                raise forms.ValidationError("The date cannot be in the past!")
            return datetime

        fields = ['organizer','attendee','datetime','place']

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

class AddAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        labels = {  'required_supply' : 'Insumo',
                    'designated_user' : 'Invitado designado',
                    'comment' : 'Comentarios',
                    'required_quantity' : 'Cantidad' }

        fields = ['designated_user','required_supply','required_quantity','comment']
