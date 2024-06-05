from django.contrib import admin

from .models import *

class TagliaAdmin(admin.TabularInline):
    model = Taglia
    extra=0

class ProdottoAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'idModello', 'taglie')
    inlines = [TagliaAdmin]

    def taglie(self, obj):
        return ", ".join([t.taglia for t in obj.taglie.all()])
    

admin.site.register(Prodotto, ProdottoAdmin)