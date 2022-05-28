from django.db import models

from django.contrib.auth.models import AbstractUser

ADMIN = "Admin"
MANAGER = "Manager"
KASIR = "Kasir"
class Pegawai(AbstractUser):
    role_list = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (KASIR, 'Kasir')
    )
    role = models.CharField(max_length=100, choices=role_list, default=ADMIN)
    text_password = models.CharField(max_length=100, blank=True, null=True)
