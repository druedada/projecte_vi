from django.urls import path

from . import views

app_name = 'comandes'

urlpatterns = [
    path('carret/', views.carret, name='carret'),
]
