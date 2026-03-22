from django.urls import path
from . import views

app_name = 'comandes'

urlpatterns = [
    path('', views.index, name='index'),
]
