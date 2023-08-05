from django.contrib import admin
from .models import Instalacaoativo

@admin.register(Instalacaoativo)
class InstalacaoativoAdmin(admin.ModelAdmin):
   list_display = ('id','descricao')

 
#admin.site.register(Categoria)
#admin.site.register(Registroo)

#admin.site.register()

# Register your models here.


