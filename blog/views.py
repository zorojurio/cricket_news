from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView,
    View)
from django.views.generic.list import MultipleObjectMixin

from blog.forms import CommentForm, PostForm, SearchForm
from blog.models import Comment, Post
from category.models import Category
from marketing.forms import EmailSignupForm
from marketing.models import Signup
from subcategory.models import SubCategory


class AboutView(TemplateView):
    template_name = "blog/about.html"


class HomeView(View):
    def get(self, *args, **kwargs):
        post_list = Post.objects.filter(
            featured=True, published_date__lte=timezone.now()).order_by('-published_date')[:3]
        latest = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('-published_date')[:3]
        pics = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('-published_date')[3:7]
        form = EmailSignupForm()
        context = {
            'post_list': post_list,
            'latest': latest,
            'pics': pics,
            'form': form,
        }
        return render(self.request, template_name='blog/home.html', context=context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")


# class CategoryListView(ListView):
#     model = Post
#     context_object_name = 'post_list'
#     paginate_by = 5

    # def get_queryset(self):
    #     cate = get_object_or_404(Category, title=self.kwargs.get('title'))
    #     return cate.post_set.filter(published_date__lte=timezone.now()).order_by('-published_date')


# class SubCategoryListView(ListView):
#     model = Post
#     context_object_name = 'post_list'
#     paginate_by = 5

#     def get_queryset(self):
#         sub_cate = get_object_or_404(
#             SubCategory, sub_title=self.kwargs.get('sub_title'))
#         return Post.objects.filter(sub_category=sub_cate, published_date__lte=timezone.now()).order_by('-published_date')


class PostListView(ListView):
    model = Post
    paginate_by = 3
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now())


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_draft.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['post_list'] = Post.objects.filter(
            published_date__isnull=True, author=user).order_by('-create_date')

        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        user_posts = Post.objects.filter(
            author=user, published_date__lte=timezone.now())
        p = Paginator(user_posts, 6)
        page = self.request.GET.get('page', 1)

        try:
            context['page_obj'] = p.page(page)
        except EmptyPage:
            context['page_obj'] = p.page(p.num_pages)
        context['author'] = user
        context['is_paginated'] = True
        return context


class CategoryListView(ListView):
    model = Post
    context_object_data = 'post_list'
    paginate_by = 4
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context['category_meta'] = cate
        context['category_list'] = Category.objects.all()
        context['most_recent'] = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('published_date')[:3]
        return context

    def get_queryset(self):
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return cate.post_set.filter(published_date__lte=timezone.now()).order_by('-published_date')


class SubCategoryListView(ListView):
    model = Post
    context_object_data = 'post_list'
    paginate_by = 4
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cate = get_object_or_404(
            SubCategory, sub_slug=self.kwargs.get('sub_slug'))
        context['sub_category_meta'] = cate
        context['category_list'] = Category.objects.all()
        context['most_recent'] = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('published_date')[:3]
        return context

    def get_queryset(self):
        cate = get_object_or_404(
            SubCategory, sub_slug=self.kwargs.get('sub_slug'))
        return cate.post_set.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    form = CommentForm()
    template_name = "blog/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        cate = post.category
        context['category_list'] = Category.objects.all()
        context['form'] = self.form
        context['most_recent'] = cate.post_set.filter(
            published_date__lte=timezone.now()).order_by('-published_date')[:3]
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post:detail", kwargs={
                'slug': post.slug
            }))


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm

    def test_func(self):
        return self.request.user.is_staff

    def get_initial(self):
        return {
            "author": self.request.user
        }


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author and self.request.user.is_staff:
            return True
        return False

    def get_initial(self):
        return {
            "author": self.request.user
        }


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post:list')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author and self.request.user.is_staff:
            return True
        return False


@login_required
def publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author and request.user.is_staff:
        post.publish()
        return redirect('post:detail', slug=slug)
    else:
        return redirect('post:list')


@login_required
def unpublish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author and request.user.is_staff:
        post.published_date = None
        post.save()
    return redirect('post:detail', slug=slug)


@login_required
def publish_now(request):
    # creating a form using request
    post = PostForm(request.POST, request.FILES)

    if post.is_valid():
        post_save = post.save(commit=False)
        # setting the published date
        post_save.publish()
        return redirect('post:detail', slug=post_save.slug)


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(
        category_id=category_id).order_by('sub_title')
    return render(request, template_name='blog/subcategory_drop_down_list.html', context={'subcategories': subcategories})


def search(request):

    if request.method == 'POST':
        print(request.POST.get('q'))
        form = SearchForm(request.POST)
        if form.is_valid():

            queryset = Post.objects.all()
            query = form.cleaned_data.get('q')
            if query:
                queryset = queryset.filter(
                    Q(main_title__icontains=query) |
                    Q(short_description__icontains=query)
                ).distinct()

            context = {
                'queryset': queryset,
            }
            return render(request, template_name='blog/search_results.html', context=context)
    return render(request, template_name='blog/search_results.html')
