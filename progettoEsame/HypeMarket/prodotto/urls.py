from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "prodotto"

urlpatterns = [
    path('catalogo/', catalogo, name='catalogo')
]