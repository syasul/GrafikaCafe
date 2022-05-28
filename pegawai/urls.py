from django.urls import path

from . import views

urlpatterns = [
    path('', views.pegawai, name='pegawai'),
    path('tambah-pegawai/', views.tambahPegawai, name='tambah-pegawai'),
    path('update-pegawai/', views.updatePegawai, name='update-pegawai'),
    path('delete-pegawai/', views.deletePegawai, name='delete-pegawai')
]
