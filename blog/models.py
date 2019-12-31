from category.models import Category
from subcategory.models import SubCategory
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from django.template.defaultfilters import slugify


class Post(models.Model):
    """Model definition for Post."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    main_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200)
    news_pic = models.ImageField(upload_to='news_pics')
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

    def __str__(self):
        """Unicode representation of Post."""
        return self.main_title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post:update',  kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post:delete',  kwargs={'slug': self.slug})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    def get_category_list_url(self):
        return reverse('post:category', kwargs={
            'slug': self.category.slug,

        })

    def subcat(self):
        if self.sub_category:
            return self.sub_category.sub_slug

    def get_sub_category_list_url(self):
        return reverse('post:sub_category', kwargs={
            'slug': self.category.slug,
            'sub_slug': self.subcat(),


        })

    def get_user_post(self):
        return reverse('user-posts', kwargs={
            'username': self.author.username
        })

    class Meta:
        ordering = ["-published_date"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.main_title)
        super().save(*args, **kwargs)

        img = Image.open(self.news_pic.path)

        if img.height > 800 or img.width > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            img.save(self.news_pic.path)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_commented_user_post(self):
        return reverse('user-posts', kwargs={
            'username': self.user.username
        })
