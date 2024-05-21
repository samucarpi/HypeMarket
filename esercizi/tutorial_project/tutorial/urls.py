"""
URL configuration for tutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^home/$", homepage, name="homepage"),
    path('welcome/',utente_welcome,name='utente_welcome'),
    path('welcome/<str:nome>/<int:eta>/',utente_welcome,name='utente_welcome'),
    path('listaparametri/',lista_parametri,name='lista_parametri'),
    path('infoparametri/<str:nome>/<int:eta>/', info_parametri, name='alias'),
    path('static/',visualizza_static,name='visualizza_static'),
    path('persona-create/',PersonaCreate.as_view(),name='persona-create')

]
