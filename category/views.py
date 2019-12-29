from django.shortcuts import render
from category.models import Category
from django.views.generic import ListView


class CategoryPostList(ListView):
    model = Category
