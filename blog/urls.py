from django.urls import path, re_path
from . import views as blog_views

app_name = 'blog'  # Namespace.

urlpatterns = [
    path('', blog_views.PostList.as_view(), name='post_view'),
    path('draft/', blog_views.DraftPostList.as_view(), name='draft_post_view'),
    path('published/', blog_views.PublishedPostList.as_view(), name='published_post_view'),
    path('post/<year>/<month>/<day>/<slug:slug>/', blog_views.DetailsPostView.as_view(), name='post_details_view'),
    path('post/add/', blog_views.PostCreate.as_view(), name='post_add'),
    path('post/<int:pk>/edit/', blog_views.PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/published/', blog_views.PostPublish.as_view(), name='post_published'),
    path('post/<int:pk>/delete/', blog_views.PostDelete.as_view(), name='post_delete'),
    path('comment/approve/<int:post_pk>/<int:comment_pk>/', blog_views.ApprovedComment.as_view(), name='comment_approve'),
    path('comment/remove/<int:post_pk>/<int:comment_pk>/', blog_views.RemoveComment.as_view(), name='comment_remove'),
]
