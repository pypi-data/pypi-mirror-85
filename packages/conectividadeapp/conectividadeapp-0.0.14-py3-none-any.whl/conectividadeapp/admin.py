from django.contrib import admin
from .models import Activity, Actor, InstalacaoAtivo


@admin.register(InstalacaoAtivo)
class InstalacaoAtivoAdmin(admin.ModelAdmin):
    list_display = ['id', 'comments']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'device']
