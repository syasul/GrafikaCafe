from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Logaktifitas

allow_role = ['Admin', 'Manager']


@login_required
def logaktifitas(request):
    if request.user.role in allow_role:
        pass
    else:
        return HttpResponse('Anda bukan manager')
    log = Logaktifitas.objects.all()
    return render(request, 'logaktifitas.html', {'log': log})
