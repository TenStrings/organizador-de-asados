from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from datetime import datetime
from .models import Asado,User,Invitation
from .forms import AddAsadoForm,AddUserForm,AddItemForm

def homepage(request):
    template = get_template('homepage.html')
    if request.method == 'POST':
        form = AddAsadoForm(request.POST)
        new_asado = form.save(commit=False)
        new_asado.save()
        if form.is_valid():
            for user_name in form.cleaned_data['attendee'].all():
                user = User.objects.get(name=user_name)
                invitation = Invitation.objects.create( invite=user,
                                                        asado=new_asado)
    else:
        form = AddAsadoForm()

    asados = Asado.objects.all()
    return HttpResponse(template.render( request = request,
                                         context = {'lista_de_asados' : asados,
                                          'form' : form
                                         }))

def asado_de(request,an_organizer):
    template = get_template('asado-de.html')
    organizer = User.objects.get(name=an_organizer)
    asado = Asado.objects.get(organizer=organizer)
    invites = asado.attendee.all()

    if request.method == 'POST':
        form = AddItemForm(request.POST)
        new_item = form.save(commit=False)
        new_item.asado = asado
        new_item.save()
    else:
        form = AddItemForm()
        form.fields["designated_user"].queryset = asado.attendee.all()

    items_to_buy = asado.items.all()
    return HttpResponse(template.render(request = request,
                                        context = {'lista_de_invitados' : invites,
                                                    'items_a_comprar' : items_to_buy,
                                                    'form' : form
                                        }))

def personal_page(request,username):
    user = User.objects.get(name=username)
    template = get_template('personal-page.html')
    if request.method == 'POST':
        pass
    else:
        pass
    invites = Invitation.objects.filter(invite=user)
    return HttpResponse(template.render(request=request,
                                        context= {
                                            'username' : user.name,
                                            'invites' : invites,
                                        }))

def add_user(request):
    template = get_template('user-creation.html')
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        new_user = form.save()
    else:
        form = AddUserForm()

    return HttpResponse(template.render(
        request = request,
        context = {'form' : form}
    ))
