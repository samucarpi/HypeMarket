from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "prodotto"

urlpatterns = [
    path('home', home, name='home'),
    path('<str:idModello>/', prodotto, name='Prodotto'),
    path('<str:idModello>/offerta', offerta, name='Offerta'),
    path('<str:idModello>/proposta', proposta, name='Proposta')
]
