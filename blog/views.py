from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment, Category, SubCategory
from django.utils import timezone
from blog.forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


class AboutView(TemplateView):
    template_name = "blog/about.html"


class CategoryListView(ListView):
    model = Post
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        cate = get_object_or_404(Category, title=self.kwargs.get('title'))
        return Post.objects.filter(category=cate, published_date__lte=timezone.now()).order_by('-published_date')


class SubCategoryListView(ListView):
    model = Post
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        sub_cate = get_object_or_404(
            SubCategory, sub_title=self.kwargs.get('sub_title'))
        return Post.objects.filter(sub_category=sub_cate, published_date__lte=timezone.now()).order_by('-published_date')


class PostListView(ListView):
    model = Post
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('-published_date')
        context['carousel_list'] = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('-published_date')[:3]
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['posts'] = Post.objects.filter(
            author=user).order_by('-published_date')
        context['author'] = user
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['object']
        cate = post.category
        context['post_detail_list'] = cate.post_set.filter(
            published_date__lte=timezone.now()).order_by('-published_date')[:5]
        return context


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


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_draft.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['post_list'] = Post.objects.filter(
            published_date__isnull=True, author=user).order_by('-create_date')

        return context


@login_required
def publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author and request.user.is_staff:
        post.publish()
        return redirect('post:detail', pk=pk)
    else:
        return redirect('post:list')


@login_required
def unpublish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author and request.user.is_staff:
        post.published_date = None
        post.save()
    return redirect('post:detail', pk=pk)


@login_required
def publish_now(request):
    # creating a form using request
    post = PostForm(request.POST, request.FILES)

    if post.is_valid():
        post_save = post.save(commit=False)
        # setting the published date
        post_save.publish()
        return redirect('post:detail', pk=post_save.pk)
