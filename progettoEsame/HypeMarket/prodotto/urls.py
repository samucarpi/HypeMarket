from django.urls import path, include
from .views import *

app_name = 'prodotto'

urlpatterns = [
    path('catalogo/', catalogo, name='catalogo'),
    path('<str:idModello>/', prodotto, name='Prodotto'),
]
