from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "utente"

urlpatterns = [
    path('login', loginForm, name='Login'),
    path('registrazione', registrazione, name='Registrazione'),
    path('account', account, name='Account'),
    path('account/modifica-indirizzo', modificaIndirizzo, name='Modifica'),
]
