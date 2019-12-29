from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import sign_up, update_profile
from blog import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('signup/', sign_up, name='signup'),
    path('update_profile/', update_profile, name='update_profile'),
    path('user/<str:username>', views.UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/drafts/',
         views.DraftListView.as_view(), name='drafts'),
    path('about/', views.AboutView.as_view(), name='about'),

]
