from django.shortcuts import render
from .models import Profile
# Create your views here.
def my_profile_view(request):
    obj = Profile.objects.get(username=request.user)

    context = {
        'obj': obj,
    }

    return render(request, 'perfil/myprofile.html', contex)
