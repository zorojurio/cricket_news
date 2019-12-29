from category.models import Category
from subcategory.models import SubCategory
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    """Model definition for Post."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    main_title = models.CharField(max_length=200)
    slug = models.SlugField()
    news_pic = models.ImageField(upload_to='news_pics', blank=True, null=True)
    video_link = models.CharField(max_length=200, blank=True, null=True)
    short_description = models.TextField()
    long_description = RichTextUploadingField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.CASCADE)

    sub_category = models.ForeignKey(
        SubCategory, verbose_name="sub_category", on_delete=models.CASCADE, blank=True, null=True)

    featured = models.BooleanField(default=False)
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

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

    def get_update_url(self):
        return reverse('post:update',  kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('post:delete',  kwargs={'pk': self.pk})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    class Meta:
        ordering = ["-published_date"]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
