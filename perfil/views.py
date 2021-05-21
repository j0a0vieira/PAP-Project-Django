from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required
def my_profile_view(request):
    profile = Profile.objects.get(username=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    friends_qs = Profile.get_friends(request.user)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'friendlist': friends_qs,
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'perfil/myprofile.html', context)



@login_required
def profile_search(request):

    if request.method == 'POST':
        searched = request.POST['searched_name']
        people_match = Profile.objects.filter( #usar Q para criar uma queryset complexa
            Q(first_name=searched) | Q(last_name=searched)
        ).exclude(username=request.user)
        print(people_match)

        context = {
            'searched': searched,
            'matched_people': people_match,
        }



        return render(request, 'perfil/profile_search.html', context)
    else:
        return render(request, 'perfil/profile_search.html')



@login_required
def invites_received_view(request):
    profile = Profile.objects.get(username=request.user)
    qs = Relationship.objects.invitations_received(profile)
    result = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(result) == 0:
        is_empty = True

    context = {
        'qs': result,
        'is_empty': is_empty,
        }

    return render(request, 'perfil/my_invites.html', context)


@login_required
def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(username=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == "send":
            rel.status = 'accepted'
            rel.save()
    return redirect('perfil:my-invites-view')


@login_required
def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(username=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('perfil:my-invites-view')



@login_required
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'perfil/to_invite_list.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'perfil/detail.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

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
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False

        return context
          



class ProfileListView(LoginRequiredMixin, ListView):
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
@login_required
def send_invitation(request):
    if request.method=='POST': #verificar se o request é POST, ou seja, submissão de um formulário, neste caso, envio de pedido de amizade
        pk = request.POST.get('profile_pk') #pegar a pk da conta que receberá o convite, submetida no template
        user = request.user #user logado
        sender = Profile.objects.get(username=user) #definir quem envia o pedido, user logado
        receiver = Profile.objects.get(pk=pk) #definir o utilizador que recebe o pedido, através da pk

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send') #criar relacao entre sender e receiver no estado 'send'

        return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect('perfil:my-profile-view')


@login_required
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


