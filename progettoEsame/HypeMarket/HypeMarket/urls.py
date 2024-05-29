from django.contrib import admin
from django.urls import path, include
from .init_db import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('utente/', include('utente.urls')),
    path('sneakers/', include('prodotto.urls')),
    path('gestione/', include('gestione.urls')),
]
 
#erase_db()
#init_db()