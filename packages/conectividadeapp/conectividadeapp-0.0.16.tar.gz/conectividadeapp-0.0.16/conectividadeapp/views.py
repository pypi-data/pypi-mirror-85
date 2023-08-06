from django.shortcuts import render, redirect, get_object_or_404
from .models import InstalacaoAtivo
from django.http import HttpResponse
import datetime
from django.views.generic import View
from dcim.models import Device


class ListConectividadeView(View):
    """
    List all reg in the database.
    """
    def get(self, request):

        rg = InstalacaoAtivo.objects.all()
        dv = Device.objects.all()
        return render(request, 'conectividadeapp/listagem.html', {
            'registro': rg,
            'device': dv,

        })
