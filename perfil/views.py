from django.shortcuts import render
from .models import Profile
from .forms import ProfileModelForm

# Create your views here.
def my_profile_view(request):
    obj = Profile.objects.get(username=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=obj)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'obj': obj,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'perfil/myprofile.html', context)
