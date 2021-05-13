from django.urls import path
from .views import ( 
        my_profile_view, 
        invites_received_view, 
        invite_profiles_list_view, 
        ProfileListView,
        ProfileDetailView,
        send_invitation,
        remove_friend,
        accept_invitation,
        reject_invitation,
        profile_search,
)

app_name = 'perfil'

urlpatterns = [
    path('myprofile/', my_profile_view, name="my-profile-view"),
    path('profile_search/', profile_search, name="profile-search"),
    path('my_invites/', invites_received_view, name="my-invites-view"),
    path('', ProfileListView.as_view(), name="all-profiles-view"),
    path('to_invite/', invite_profiles_list_view, name="invite-profiles-view"),
    path('send_invite/', send_invitation, name="send_invite"),
    path('remove_friend/', remove_friend, name="remove_friend"),
    path('<slug>/', ProfileDetailView.as_view(), name="profile_detail_view"),
    path('my_invites/accept', accept_invitation, name="accept_invitation"),
    path('my_invites/reject', reject_invitation, name="reject_invitation"),
]
