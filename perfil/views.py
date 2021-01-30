from django.shortcuts import render
from .models import Profile, Relationship
from .forms import ProfileModelForm


# Create your views here.
def my_profile_view(request):
    profile = Profile.objects.get(username=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'perfil/myprofile.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(username=request.user)
    qs = Relationship.objects.invitations_received(profile)

    context = {'qs': qs}

    return render(request, 'perfil/my_invites.html', context)



def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}

    return render(request, 'perfil/profiles_list.html', context)


def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'perfil/to_invite_list.html', context)   