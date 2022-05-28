import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Pesanan
from menu.models import Menu
from logaktifitas.models import Logaktifitas

from datetime import datetime, timedelta
import pytz
date_now = datetime.now(pytz.timezone('Asia/Jakarta'))


allow_role = ['Admin', 'Kasir']


@login_required
def pesanan(request):
    if request.user.role in allow_role:
        pass
    else:
        return HttpResponse('Anda bukan kasir')

    context = {
        'menu': Menu.objects.filter(stok="Tersedia")
    }
    return render(request, 'pesanan.html', context)


@login_required
def tambahPesanan(request):
    if request.user.role in allow_role:
        pass
    else:
        return HttpResponse('Anda bukan kasir')

    if request.method == "POST":
        menuID = request.POST.get('menuID')
        quantity = int(request.POST.get('quantity'))
        no_meja = request.POST.get('no_meja')
        if quantity < 1:
            return HttpResponse('Minimal pemesanan 1')
        kasir = request.user
        menu = Menu.objects.get(id=menuID)
        amount = menu.price * quantity
        date = datetime.now(pytz.timezone('Asia/Jakarta'))
        pesananDict = {
            "Id": menuID,
            "Quantity": quantity,
            "No Meja": no_meja,
            "Kasir": kasir.username,
            "Menu": menu.name,
            "amount": amount
        }

        try:
            Pesanan.objects.create(kasir=kasir,
                                   menu=menu,
                                   quantity=quantity,
                                   price=menu.price,
                                   amount=amount,
                                   no_meja=no_meja,
                                   date=date)
            Logaktifitas.objects.create(
                pegawai=request.user, activity="Membuat pesanan %s" % pesananDict, date=date_now)
            messages.success(request, 'Success pesanan dibuat')
        except:
            messages.error(request, 'Failed pesanan dibuat')

    return redirect('pesanan')


@login_required
def transaksi(request):
    context = {
        'transaksi': Pesanan.objects.all()
    }
    search_meja = request.GET.get('search')

    if search_meja:
        pesanan = Pesanan.objects.filter(
            no_meja=search_meja, kasir=request.user)
        for e in pesanan:
            print(e)

        li = []

        for p in pesanan:
            li.append(p.menu.price*p.quantity)
        total = sum(li)

        context = {
            'transaksi': pesanan,
            'total': total,
        }
        return render(request, 'transaksi1.html', context)
    return render(request, 'transaksi.html', context)


@login_required
def pembayaran(request):
    if request.method == "POST":
        pesanan = request.POST.get('pesanan')
        total = int(request.POST.get('total'))
        duit = int(request.POST.get('bayar'))
        print(pesanan, total, duit)
        semuanya = duit-total
        if semuanya < 0:
            return HttpResponse("mohon maaf duit nya kurang")
        else:
            # Relasi_Kasir_Pesanan.objects.create(kasir=request.user, pesanan=pesanan)
            return HttpResponse("Terimkasih, jangan lupa kembalian nya")


@login_required
def riwayat(request, name):
    result = Pesanan.objects.filter(kasir__username__contains=name).all()
    li = []
    for r in result:
        li.append(r)
    context = {
        'result': li,
        'total_item': result.count()
    }
    return render(request, 'riwayat.html', context)


@login_required
def updateTransaksi(request):
    if request.user.role in allow_role:
        pass
    else:
        return HttpResponse('Anda bukan kasir')

    if request.method == "POST":
        pesananID = request.POST.get('id')
        quantity = request.POST.get('quantity')
        if int(quantity) < 1:
            return HttpResponse('Minimal pemesanan 1')
        pesanan_obj = Pesanan.objects.get(id=pesananID)
        pesanan_obj.quantity = int(quantity)
        pesanan_obj.amount = pesanan_obj.price * int(quantity)

        pesananDict = {
            "Kasir": request.user.username,
            "Id Pesanan": pesananID,
            "Quantity": pesanan_obj.quantity,
            "Amount": pesanan_obj.amount
        }
        print(request.user)
        try:
            pesanan_obj.save()
            Logaktifitas.objects.create(
                pegawai=request.user, activity="Mengupdate pesanan %s" % pesananDict, date=date_now)
            messages.success(request, 'Success update')
        except:
            messages.error(request, 'Failed update')

    return redirect('transaksi')


@login_required
def deleteTransaksi(request):
    if request.user.role in allow_role:
        pass
    else:
        return HttpResponse('Anda bukan kasir')

    if request.method == "POST":
        try:
            id_pemesanan = Pesanan.objects.get(id=request.POST.get('id'))
            Pesanan.objects.filter(id=request.POST.get('id')).delete()
            Logaktifitas.objects.create(
                pegawai=request.user, activity="Mendelete pesanan dengan ID %s" % id_pemesanan, date=date_now)
            messages.success(request, 'Success delete transaksi')
        except:
            messages.error(request, 'Failed delete transaksi')

    return redirect('transaksi')


@login_required
def laporan(request):
    sekarang = datetime.now(pytz.timezone('Asia/Jakarta'))
    satu_bulan_lalu = sekarang - timedelta(days=30)
    penjualan_bulan_lalu = 0
    penjualan_harian = request.GET.get('harian')
    if penjualan_harian:
        for p in Pesanan.objects.filter(date__range=[penjualan_harian, sekarang]):
            penjualan_bulan_lalu += p.amount

        context = {
            'penjualan_bulan_lalu': penjualan_bulan_lalu
        }
        return render(request, 'laporan.html', context)
    # for p in Pesanan.objects.filter(date__range=[satu_bulan_lalu, sekarang]):
    #     penjualan_bulan_lalu += p.amount
    # context = {
    #     'penjualan_bulan_lalu': penjualan_bulan_lalu
    # }
    return render(request, 'laporan.html')
