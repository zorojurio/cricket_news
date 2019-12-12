from django.urls import path
from blog import views


app_name = 'post'
urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('user/<str:username>', views.UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/drafts/',
         views.DraftListView.as_view(), name='drafts'),
    path('story/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('publish/', views.publish_now, name='publish_now'),
    path('story/<int:pk>/update/', views.PostUpdateView.as_view(), name='update'),
    path('story/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('story/<int:pk>/publish/', views.publish, name='publish'),
    path('story/<int:pk>/unpublish/', views.unpublish, name='unpublish'),
    path('category/<str:title>', views.CategoryListView.as_view(), name='category'),
    path('category/<str:title>/<str:sub_title>',
         views.SubCategoryListView.as_view(), name='sub_category'),
]
