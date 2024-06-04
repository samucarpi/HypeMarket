from django.urls import path
from .views import *

app_name = 'utente'

urlpatterns = [
    path('login', loginForm, name='Login'),
    path('logout', logoutAction, name='Logout'),
    path('registrazione', registrazioneForm, name='Registrazione'),
    path('account', account, name='Account'),
    path('account/modifica/<str:tipo>', modifica, name='Modifica'),
    path('account/elimina/<str:tipo>', elimina, name='Modifica'),
    path('preferiti/<str:idModello>', aggiungiPreferiti, name='Aggiunta ai preferiti'),
    path('wishlist', wishlist, name='Preferiti'),
    path('vendite', vendite, name='Vendite'),
    path('acquisti', acquisti, name='Acquisti'),
]