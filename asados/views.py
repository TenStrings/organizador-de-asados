from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from datetime import datetime
from .models import (
    Asado,
    User,
    Invitation,
    Assignment,
    AssignmentValidationError
)
from .forms import AddAsadoForm, AddUserForm, AddAssignmentForm
from django.core.exceptions import ValidationError
from django.urls import reverse


def homepage(request):
    template = get_template('homepage.html')
    if request.method == 'POST':
        form = AddAsadoForm(request.POST)
        new_asado = form.save()
        return HttpResponseRedirect('')
    else:
        form = AddAsadoForm()

    asados = Asado.objects.all()
    return HttpResponse(
        template.render(
            request=request,
            context={
                'lista_de_asados': asados,
                'form': form
            }
        )
    )


def asado_id(request, a_valid_id):
    template = get_template('asado.html')
    asado = Asado.objects.get(id=a_valid_id)
    invites = asado.attendee.all()

    if request.method == 'POST':
        form = AddAssignmentForm(request.POST)
        new_assignment = form.save(commit=False)
        new_assignment.asado = asado
        new_assignment.save()
        return HttpResponseRedirect('')
    else:
        form = AddAssignmentForm()
        form.fields["designated_user"].queryset = asado.attendee.all()

    items_to_buy = asado.shop_list.all()
    estimated_by_items = sum(
        [item.estimated_cost() for item in items_to_buy]
    )

    estimated_cost = asado.estimated_cost

    return HttpResponse(
                template.render(
                    request=request,
                    context={
                        'lista_de_invitados': invites,
                        'items_a_comprar': items_to_buy,
                        'form': form,
                        'estimated_cost': estimated_cost
                    }
                )
            )


def personal_page(request, username):
    user = User.objects.get(name=username)
    template = get_template('personal-page.html')

    invites = Invitation.objects.filter(invite=user)
    asados = [invite.asado for invite in invites]
    return HttpResponse(
        template.render(
            request=request,
            context={
                'username': user.name,
                'asados': asados,
            }
        )
    )


def add_user(request):
    template = get_template('user-creation.html')
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        new_user = form.save()
        return HttpResponseRedirect('')
    else:
        form = AddUserForm()

    return HttpResponse(template.render(
        request=request,
        context={
            'form': form,
            'users': User.objects.all()
        }
    ))


def select_user(request):
    template = get_template('user-select.html')

    if request.method == "GET":
        if 'username' in request.GET:
            return HttpResponseRedirect('/'+request.GET['username']+'/')

    return HttpResponse(template.render(
        request=request,
        context={
            'users': User.objects.all()
        }
    ))


def pending_list(request, asado_id, username):
    template = get_template("shopping-list.html")
    asado = Asado.objects.get(id=asado_id)
    user = User.objects.get(name=username)
    shopping_list = asado.shop_list.filter(
        designated_user=user,
        fullfilled=False
    )

    return HttpResponse(
        template.render(
            request=request,
            context={
                'shopping_list': shopping_list
            }
        )
    )


def commit_assignment(request, assignment_id):
    template = get_template("commit-assignment.html")
    assignment = Assignment.objects.get(id=assignment_id)
    error_message = ''

    if request.method == 'POST':
        try:
            quantity = int(request.POST['quantity'])
        except ValueError:
            raise ValidationError("Se esperaba un número")

        try:
            assignment.finished_with(quantity)
            return redirect(
                reverse(
                    'encargos',
                    args=[
                        assignment.asado.id,
                        assignment.designated_user.name
                    ]
                )
            )
        except AssignmentValidationError as e:
            error_message = e.message

    return HttpResponse(
        template.render(
            request=request,
            context={
                'assignment': assignment,
                'error_message': error_message
            }
        )
    )
