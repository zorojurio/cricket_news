from django.shortcuts import render
from blog.models import Category, Post, SubCategory


def category_list(request):
    categories = Category.objects.all()

    return{
        'categories': categories
    }
