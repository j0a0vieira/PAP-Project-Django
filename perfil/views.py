from django.shortcuts import render, redirect
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q


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



def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'perfil/to_invite_list.html', context)


class ProfileListView(ListView):
    model = Profile
    template_name = 'perfil/profiles_list.html'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(username=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.username)
        for item in rel_s:
            rel_sender.append(item.sender.username)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


#o sender envia um pedido de amizade para o receiver
def send_invitation(request):
    if request.method=='POST': #verificar se o request é POST, ou seja, submissão de um formulário, neste caso, envio de pedido de amizade
        pk = request.POST.get('profile_pk') #pegar a pk da conta que receberá o convite, submetida no template
        user = request.user #user logado
        sender = Profile.objects.get(username=user) #definir quem envia o pedido, user logado
        receiver = Profile.objects.get(pk=pk) #definir o utilizador que recebe o pedido, através da pk

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send') #criar relacao entre sender e receiver no estado 'send'

        return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect('perfil:my-profile-view')


def remove_friend(request):
    if request.method=='POST': 
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(username=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('perfil:my-profile-view')