from django.shortcuts import render,redirect,get_object_or_404
from .models import Instalacaoativo
from django.http import HttpResponse
import datetime
from django.views.generic import View
from dcim.models import Device

class LisConectividadeView(View):
    """
    List all reg in the database.
    """
    def get(self, request):
 
        rg = Instalacaoativo.objects.all()
        dv = Device.objects.all()
        return render(request, 'conectividadeapp/listagem.html', {
            'registro': rg,
            'device': dv,
           
        })




# Create your views here.
#def listagem(request):
#    data={}
#data2={}
#   data['registro']= Registro.objects.all() 
#    data2['categoria']= Registro.objects.all() 
#  return render (request, 'dnsapp/listagem.html', data)


