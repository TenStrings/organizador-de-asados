from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add-user/$', views.add_user, name='agregar usuario'),
    url(r'^(\d+)/$', views.asado_id, name='Asado'),
    url(r'^(\d+)/(.{1,99})/$', views.pending_list, name='encargos')
]
