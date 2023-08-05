from django.db import models

# Create your models here.

# class Categoria(models.Model):
#    nome = models.CharField(max_length=100)#define o tipo de registro
#    data_cricao = models.DateTimeField(auto_now_add=True)

#    def __str__(self):
#        return self.nome


class Instalacaoativo(models.Model):

    descricao = models.CharField(max_length=200)    # descricao
    # atv_data = models.DateField(default=date.today)
    # reg_atv= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao
