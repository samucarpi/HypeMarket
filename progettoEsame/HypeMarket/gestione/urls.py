from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('offerta/<str:idModello>', offerta, name='Offerta'),
    path('proposta/<str:idModello>', proposta, name='Proposta'),
    path('vendita/<str:idModello>', vendita, name='Vendita'),
]

