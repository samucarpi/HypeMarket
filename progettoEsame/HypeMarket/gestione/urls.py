from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('offerta/<str:idModello>', offerta, name='Offerta'),
    path('proposta/<str:idModello>', proposta, name='Proposta'),
    path('vendita/<str:idModello>', vendita, name='Vendita'),
    path('acquisto/<str:idModello>', acquisto, name='Acquisto'),
    path('elimina/proposta/<str:idModello>', eliminaProposta, name='EliminaProposta'),
    path('elimina/offerta/<str:idModello>', eliminaOfferta, name='EliminaOfferta'),
    path('informazioni/<str:tipo>/<str:idModello>', informazioni, name='Informazioni'),
]