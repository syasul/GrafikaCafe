from operator import mod
from django.db import models
from pegawai.models import Pegawai


TERSEDIA = "Tersedia"
TIDAK_TERSEDIA = "Tidak Tersedia"


class Menu(models.Model):
    stocks = (
        (TERSEDIA, 'Tersedia'),
        (TIDAK_TERSEDIA, 'Tidak Tersedia'),
    )
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to="upload/menu/")
    desc = models.CharField(max_length=100)
    stok = models.CharField(max_length=100, choices=stocks, default=TERSEDIA)
    author = models.ForeignKey(Pegawai, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
