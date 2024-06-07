from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

class IndirizzoSpedizioneAdmin(admin.TabularInline):
    model = IndirizzoSpedizione
    extra = 0

class IndirizzoFatturazioneAdmin(admin.TabularInline):
    model = IndirizzoFatturazione
    extra = 0

class DatiBancariAdmin(admin.TabularInline):
    model = DatiBancari
    extra = 0

class CartaCreditoAdmin(admin.TabularInline):
    model = CartaCredito
    extra = 0

class UtenteAdmin(admin.ModelAdmin):
    list_display = ('username', 'nome', 'cognome', 'email')
    search_fields = ('username', 'nome', 'cognome', 'email')
    inlines = [IndirizzoSpedizioneAdmin, IndirizzoFatturazioneAdmin, DatiBancariAdmin, CartaCreditoAdmin]

admin.site.register(Utente, UtenteAdmin)
admin.site.unregister(Group)