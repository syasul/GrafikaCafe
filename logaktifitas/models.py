from django.db import models

from django.conf import settings


class Logaktifitas(models.Model):
    pegawai = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    activity = models.CharField(max_length=200)
    date = models.DateTimeField()

    def __str__(self):
        return self.activity

    class Meta:
        ordering = ['-date']
