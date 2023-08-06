from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import datetime
from django.views.generic import View
from dcim.models import Device


class ListConectividadeView(View):

    def get(self, request):

        device = Device.objects.all()

        return render(request, 'conectividadeapp/listagem.html', {
            'Device': device,
        })
