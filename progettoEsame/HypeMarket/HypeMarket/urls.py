from django.contrib import admin
from django.urls import path, include, re_path
from .init_db import *
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ricerca/<str:stringa>', ricerca, name='Ricerca'),
    path('utente/', include('utente.urls')),
    path('sneakers/', include('prodotto.urls')),
    path('gestione/', include('gestione.urls')),
    re_path(r'.*$', home, name='Home'),
]
 
#erase_db()
#init_db()
#Recensione.objects.all().delete()