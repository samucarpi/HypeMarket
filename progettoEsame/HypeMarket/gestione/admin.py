from django.contrib import admin
from .models import *

class OffertaAdmin(admin.ModelAdmin):
    list_display = ['utente', 'prodotto', 'taglia', 'prezzo']

class PropostaAdmin(admin.ModelAdmin):
    list_display = ['utente', 'prodotto', 'taglia', 'prezzo']

class AcquistoAdmin(admin.ModelAdmin):
    list_display = ['utente', 'prodotto', 'taglia', 'prezzo']

class VenditaAdmin(admin.ModelAdmin):
    list_display = ['utente', 'prodotto', 'taglia', 'prezzo']

class RecensioneAdmin(admin.ModelAdmin):
    list_display = ['acquisto', 'voto', 'testo']

admin.site.register(Offerta, OffertaAdmin)
admin.site.register(Proposta, PropostaAdmin)
admin.site.register(Acquisto, AcquistoAdmin)
admin.site.register(Vendita, VenditaAdmin)
admin.site.register(Recensione, RecensioneAdmin)