from django.urls import path

from . import views


urlpatterns = [
    path('', views.pesanan, name='pesanan'),
    path('tambah-pesanan/', views.tambahPesanan, name='tambah-pesanan'),
    path('update-pesanan/', views.updateTransaksi, name='update-pesanan'),
    path('delete-transaksi/', views.deleteTransaksi, name='delete-transaksi'),
    path('transaksi/', views.transaksi, name='transaksi'),
    # path('pembayaran/', views.pembayaran, name='pembayaran'),
    path('riwayat/<str:name>/', views.riwayat, name='riwayat'),
    path('laporan/', views.laporan, name='laporan')
]
