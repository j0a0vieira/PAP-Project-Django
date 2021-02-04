
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from perfil.models import Profile

def home_view(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'main/home.html', context)


            

