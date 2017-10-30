from django import forms
from functools import partial
from .models import Asado, User, Assignment, Supply, Invitation
from datetimewidget.widgets import DateTimeWidget
from django.utils import timezone
from django.core.exceptions import ValidationError


class AddAsadoForm(forms.ModelForm):
    class Meta:
        model = Asado
        dateTimeOptions = {
            'autoclose': True,
            'showMeridian': True,
            'clearBtn': True,
            'startDate': timezone.now().strftime('0%w/%d/%Y %H:%M:00')
        }
        widgets = {
            # Use localization and bootstrap 3
            'datetime': DateTimeWidget(
                attrs={'id': "yourdatetimeid"},
                bootstrap_version=3,
                usel10n=True,
                options=dateTimeOptions)
        }
        labels = {
            'organizer': 'Organizador',
            'datetime': 'Fecha',
            'attendee': 'Invitados',
            'place': 'Lugar'
        }

        fields = ['organizer', 'datetime', 'attendee', 'place']

    class Media:
        js = ('asados/javascript/asado-form.js',)

    def save(self, *args, **kwargs):
        print(timezone.now().strftime('0%w/%d/%Y %H:%M:00'))
        if self.is_valid():
            new_asado = super().save(*args, **kwargs, commit=False)
            new_asado.save()
            for user_name in self.cleaned_data['attendee'].all():
                user = User.objects.get(name=user_name)
                invitation = Invitation.objects.create(
                    invite=user,
                    asado=new_asado
                )
            return new_asado


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        labels = {
            'name': 'Nombre'
        }
        fields = ['name']


class AddAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        labels = {
            'required_supply': 'Insumo',
            'designated_user': 'Invitado designado',
            'comment': 'Comentarios',
            'required_quantity': 'Cantidad'
        }

        fields = [
            'designated_user',
            'required_supply',
            'required_quantity',
            'comment'
            ]
