from django.urls import path

from . import views

app_name = 'gestio'

urlpatterns = [
    path('', views.vins, name='vins'),
    path('crear/', views.crear_vi, name='crear_vi'),
    path('<int:vi_id>/editar/', views.editar_vi, name='editar_vi'),
    path('<int:vi_id>/eliminar/', views.eliminar_vi, name='eliminar_vi'),
    path('estadistiques/', views.estadistiques, name='estadistiques')
]
