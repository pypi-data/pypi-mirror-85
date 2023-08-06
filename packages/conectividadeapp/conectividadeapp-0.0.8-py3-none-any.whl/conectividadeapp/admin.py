from django.contrib import admin
from .models import InstalacaoAtivo


@admin.register(InstalacaoAtivo)
class InstalacaoativoAdmin(admin.ModelAdmin):
   list_display = ('id', 'comments')
