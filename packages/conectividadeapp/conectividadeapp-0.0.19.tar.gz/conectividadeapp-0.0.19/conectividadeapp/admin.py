from django.contrib import admin
from .models import Activity, Actor, OldDevice


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'device']


@admin.register(OldDevice)
class OldDevice(admin.ModelAdmin):
    list_display = ['id']
