from django.db import models
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    slug = models.SlugField(max_length=100, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def get_latest(self):
        return self.post_set.filter(featured=True).order_by('-published_date')[:3]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
