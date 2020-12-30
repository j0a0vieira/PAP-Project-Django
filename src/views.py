from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request): #utilizadores

    return render(request, 'main/home.html')



def startpage_view(request): #nao utilizadores
    return render(request, 'main/index.html')



def login_view(request): #login
    return render (request, 'main/login.html')



def login_attempt(request): #tentativa de login + redirecionamento
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return render(request, 'main/home.html')
    else:
        return render(request, 'main/login.html')
