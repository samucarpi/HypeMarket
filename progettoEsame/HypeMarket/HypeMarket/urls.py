from django.contrib import admin
from django.urls import path, include, re_path
from .initProdotti import *
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ricerca/<str:stringa>', ricerca, name='Ricerca'),
    path('utente/', include('utente.urls')),
    path('sneakers/', include('prodotto.urls')),
    path('gestione/', include('gestione.urls')),
    re_path(r'home', home, name='Home'),
]

initProdotti()