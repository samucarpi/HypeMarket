from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "utente"

urlpatterns = [
    path('login', loginForm, name='Login'),
    path('logout', logoutAction, name='Logout'),
    path('registrazione', registrazione, name='Registrazione'),
    path('account', account, name='Account'),
    path('account/modifica-informazioni', modificaInformazioni, name='Modifica'),
    path('account/modifica-indirizzo-spedizione', modificaIndirizzoSpedizione, name='Modifica'),
    path('account/modifica-indirizzo-fatturazione', modificaIndirizzoFatturazione, name='Modifica'),
    path('account/modifica-banca', modificaBanca, name='Modifica'),
    path('account/modifica-carta', modificaCarta, name='Modifica'),
]