from django.db import models

from pegawai.models import Pegawai
from menu.models import Menu

from django.conf import settings



class Pesanan(models.Model):
    kasir = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    no_meja = models.IntegerField(default=0)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True, null=True, auto_created=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date']