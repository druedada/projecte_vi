from django.urls import path

from . import views

app_name = 'gestio'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('vins/', views.llistar_vins, name='llistar_vins'),
    path('vins/crear/', views.crear_vi, name='crear_vi'),
    path('vins/<int:vi_id>/editar/', views.editar_vi, name='editar_vi'),
    path('vins/<int:vi_id>/eliminar/', views.eliminar_vi, name='eliminar_vi'),
]
