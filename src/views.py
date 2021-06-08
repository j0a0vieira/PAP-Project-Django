
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from perfil.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

def home_view(request):
    user = request.user
    uc_form = SignUpForm()
    registration_error = False

    if 'user_registration' in request.POST:
        uc_form = SignUpForm(request.POST)
        if uc_form.is_valid():
            uc_form.save()
            new_user = authenticate(username=uc_form.cleaned_data['username'],
                                    password=uc_form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect("/timeline/")
        else: 
            registration_error = True   

    context = {
        'r_error': registration_error,
        'uc_form': uc_form,
        'user': user,
    }

    if request.user.is_authenticated:
        return redirect('posts:main-post-view')        
    else:
        return render(request, 'main/home.html', context)


