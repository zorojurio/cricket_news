from django.urls import path
from blog import views


app_name = 'post'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.search, name='search'),
    # crud
    path('explore/', views.PostListView.as_view(), name='list'),
    path('article/<slug:slug>', views.PostDetailView.as_view(), name='detail'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('article/<slug:slug>/update/',
         views.PostUpdateView.as_view(), name='update'),
    path('article/<slug:slug>/delete/',
         views.PostDeleteView.as_view(), name='delete'),
    # publish
    path('article/<slug:slug>/publish/', views.publish, name='publish'),
    path('article/<slug:slug>/unpublish/', views.unpublish, name='unpublish'),
    path('publish/', views.publish_now, name='publish_now'),
    # categories
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('category/<slug:slug>/<slug:sub_slug>',
         views.SubCategoryListView.as_view(), name='sub_category'),
    path('ajax/load_subcategories/', views.load_subcategories,
         name='ajax_load_subcategories'),
]
