from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    title = models.CharField(max_length=255, verbose_name="Title")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['created_at']

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    sub_title = models.CharField(max_length=255, verbose_name="Title")
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"
        ordering = ['sub_title']

    def __str__(self):
        return self.category.title + " " + self.sub_title


class Post(models.Model):
    """Model definition for Post."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    main_title = models.CharField(max_length=200)
    news_pic = models.ImageField(upload_to='news_pics', blank=True, null=True)
    video_link = models.CharField(max_length=200, blank=True, null=True)
    short_description = models.TextField()
    long_description = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.CASCADE)

    sub_category = models.ForeignKey(
        SubCategory, verbose_name="sub_category", on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_approved_comments_list(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        """Unicode representation of Post."""
        return self.main_title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ["-published_date"]

        
class Comment(models.Model):
    """Model definition for Comment."""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comments = models.BooleanField(default=False)

    def approve(self):
        self.approved_comments = True
        self.save()

    def __str__(self):
        """Unicode representation of Comment."""
        return self.text
