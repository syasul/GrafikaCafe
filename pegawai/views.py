import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as login_pegawai, logout as logout_pegawai
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session


from pegawai.models import Pegawai
from logaktifitas.models import Logaktifitas
date_now = datetime.datetime.now()
print(date_now)



def login(request):
    if request.user.is_authenticated:
        return redirect('pegawai')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == "Admin":
            login_pegawai(request, user)
            Logaktifitas.objects.create(pegawai=request.user, activity="Login" , date=date_now)
            messages.success(request, 'Success login')
            return redirect('pegawai')
        elif user is not None and user.role == "Manager":
            login_pegawai(request, user)
            Logaktifitas.objects.create(pegawai=request.user, activity="Login" , date=date_now)
            messages.success(request, 'Success login')
            return redirect('menu')
        elif user is not None and user.role == "Kasir":
            login_pegawai(request, user)
            Logaktifitas.objects.create(pegawai=request.user, activity="Login" , date=date_now)
            messages.success(request, 'Success login')
            return redirect('pesanan')
        else:
            messages.error(request, 'Invalid credential')
    return render(request, 'home.html')


@login_required
def pegawai(request):
    if request.user.role != 'Admin':
        return HttpResponse('Anda bukan admin')

    s = Session.objects.all()

    context = {
        'pegawai': Pegawai.objects.all()
    }

    return render(request, 'pegawai.html', context)


@login_required
def tambahPegawai(request):
    print(request.user)
    print(date_now)
    
    if request.user.role != 'Admin':
        return HttpResponse('Adnda bukan admin')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        hash_password = make_password(password)

        try:
            Pegawai.objects.create(
                username=username, password=hash_password, text_password=password, role=role)
            Logaktifitas.objects.create(pegawai=request.user, activity="Menambahkan user baru dengan nama %s"%username , date=date_now)
            messages.success(request, 'Success membuat pegawai baru')
        except:
            messages.error(request, 'Failed membuat pegawai baru')

    return redirect('pegawai')


@login_required
def updatePegawai(request):
    if request.user.role != 'Admin':
        return HttpResponse('Anda bukan admin')
    if request.method == "POST":
        pegawaiID = request.POST.get('id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        hash_password = make_password(password)

        pegawai_obj = Pegawai.objects.get(id=pegawaiID)
        pegawai_obj.username = username
        pegawai_obj.password = hash_password
        pegawai_obj.text_password = password
        pegawai_obj.role = role

        try:
            pegawai_obj.save()
            Logaktifitas.objects.create(pegawai=request.user, activity="Mengupdate user %s"%username , date=date_now)
            messages.success(request, 'Success update pegawai')
        except:
            messages.error(request, 'Failed update pegawai')

    return redirect('pegawai')


@login_required
def deletePegawai(request):
    if request.user.role != 'Admin':
        return HttpResponse('Anda bukan admin')

    if request.method == "POST":
        try:
            userName = Pegawai.objects.get(id=request.POST.get('id'))
            Pegawai.objects.filter(id=request.POST.get('id')).delete()
            Logaktifitas.objects.create(pegawai=request.user, activity="Mendelete user %s"%userName , date=date_now)
            messages.success(request, 'Success delete pegawai')
        except:
            messages.error(request, 'Failed delete pegawai')

    return redirect('pegawai')


def logout(request):
    logout_pegawai(request)
    return redirect('login')
