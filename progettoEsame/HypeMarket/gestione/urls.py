from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('offerta/<str:idModello>', offerta, name='Offerta'),
    path('proposta/<str:idModello>', proposta, name='Proposta'),
    path('vendita/<str:idModello>', vendita, name='Vendita'),
    path('acquisto/<str:idModello>', acquisto, name='Acquisto'),
    path('elimina/<str:tipo>/<str:id>', elimina, name='Elimina'),
    path('informazioni/<str:tipo>/<str:id>', informazioni, name='Informazioni'),
    path('recensione/<str:id>', recensione, name='Recensione'),
]
