from django.db import models
from datetime import date
from dcim.models import Device


class ActivityOptions(models.TextChoices):
    INSTALACAO = 'IN', 'Instalação'
    REMOCAO = 'RE', 'Remoção'


class InstalacaoAtivo(models.Model):

    comments = models.CharField(max_length=200)
    atv_data = models.DateField(default=date.today)
    reg_atv = models.DateTimeField(auto_now_add=True)
    actor_id = models.ManyToManyField('Actor')
    options = models.CharField(
        max_length=2,
        choices=ActivityOptions.choices,
        default=ActivityOptions.INSTALACAO,
    )

    def __str__(self):
        return self.comments


class Actor(models.Model):

    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.PROTECT
    )
    actor = models.ManyToManyField(Actor)
    type = models.CharField(max_length=50, null=False, blank=False)
    when = models.DateField(default=date.today)
    description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.description
