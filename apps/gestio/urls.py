from django.urls import path

from . import views

app_name = 'gestio'

urlpatterns = [
    path('vins/', views.vins, name='vins'),
    path('vins/crear/', views.crear_vi, name='crear_vi'),
    path('vins/<int:vi_id>/editar/', views.editar_vi, name='editar_vi'),
    path('vins/<int:vi_id>/eliminar/', views.eliminar_vi, name='eliminar_vi'),
]
