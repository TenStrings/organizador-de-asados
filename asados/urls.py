from django.conf.urls import url

from . import views

urlpatterns = [
    url('add-user', views.add_user, name='agregar usuario'),
]
