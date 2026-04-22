from django.urls import path

from . import views

app_name = 'comandes'

urlpatterns = [
    path('carret/', views.carret, name='carret'),
    path('afegir/<int:vi_id>/', views.afegir_al_carret, name='afegir_al_carret'),
    path('eliminar/<int:vi_id>/', views.eliminar_del_carret, name='eliminar_del_carret'),
    path('actualitzar/<int:vi_id>/', views.actualitzar_quantitat, name='actualitzar_quantitat'),
    path('confirmar/', views.confirmar_comanda, name='confirmar_comanda'),
]

