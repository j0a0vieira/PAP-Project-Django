from django.urls import path
from .views import post_comment_create_and_list_view, like_unlike_post, PostDeleteView, PostUpdateView, detailed_user_comment

app_name = "posts"

urlpatterns = [
    path('detail_comment/', detailed_user_comment, name="detail-comment"),
    path('', post_comment_create_and_list_view, name="main-post-view"),
    path('liked', like_unlike_post, name="like-post-view"),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
]
