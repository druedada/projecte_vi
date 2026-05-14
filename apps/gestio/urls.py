from django.urls import path

from . import views

app_name = 'gestio'

urlpatterns = [
    path('', views.vins, name='vins'),
    path('crear/', views.crear_vi, name='crear_vi'),
    path('<int:vi_id>/editar/', views.editar_vi, name='editar_vi'),
    path('<int:vi_id>/activar-desactivar/', views.activar_desactivar_vi, name='activar_desactivar_vi'),
    path('estadistiques/', views.estadistiques_redirect, name='estadistiques'),
    path('estadistiques/vins/', views.estadistiques_vins, name='estadistiques_vins'),
    path('estadistiques/vendes/', views.estadistiques_vendes, name='estadistiques_vendes'),
    path('estadistiques/usuaris/', views.estadistiques_usuaris, name='estadistiques_usuaris')

]
