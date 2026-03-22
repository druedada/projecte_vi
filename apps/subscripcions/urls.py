from django.urls import path
from . import views

app_name = 'subscripcions'

urlpatterns = [
    path('', views.index, name='index'),
]
