from django.urls import path
from blog import views


app_name = 'post'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.search, name='search'),
    # crud
    path('explore/', views.PostListView.as_view(), name='list'),
    path('story/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('story/<int:pk>/update/', views.PostUpdateView.as_view(), name='update'),
    path('story/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    # publish
    path('story/<int:pk>/publish/', views.publish, name='publish'),
    path('story/<int:pk>/unpublish/', views.unpublish, name='unpublish'),
    path('publish/', views.publish_now, name='publish_now'),
    # categories
    path('category/<str:title>', views.CategoryListView.as_view(), name='category'),
    path('category/<str:title>/<str:sub_title>',
         views.SubCategoryListView.as_view(), name='sub_category'),
    path('ajax/load_subcategories/', views.load_subcategories,
         name='ajax_load_subcategories'),
]
