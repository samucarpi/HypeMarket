from django.urls import path
from .views import *
from django.conf.urls.static import static

app_name = 'utente'

urlpatterns = [
    path('login', loginForm, name='Login'),
    path('logout', logoutAction, name='Logout'),
    path('registrazione', registrazioneForm, name='Registrazione'),
    path('account', account, name='Account'),
    path('account/modifica/<str:tipo>', modifica, name='Modifica'),
    path('account/elimina/<str:tipo>', elimina, name='Modifica'),
    path('preferiti/<str:idModello>', aggiungiPreferiti, name='Aggiunta ai preferiti'),
    path('wishlist', wishlist, name='Wishlist'),
    path('vendite', vendite, name='Vendite'),
    path('acquisti', acquisti, name='Acquisti'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
