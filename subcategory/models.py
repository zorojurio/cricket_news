from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

from category.models import Category


class SubCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    sub_title = models.CharField(max_length=255, verbose_name="Title")
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.CASCADE)
    sub_slug = models.SlugField(max_length=100, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"
        ordering = ['sub_title']

    def __str__(self):
        return self.category.title + " " + self.sub_title

    # def save(self, *args, **kwargs):
    #     self.sub_slug = slugify(self.sub_title)
    #     super().save(*args, **kwargs)


def slug_post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.sub_slug:
        slug = slugify(instance.sub_title, allow_unicode=True)
        instance.sub_slug = slug
        instance.save()


post_save.connect(slug_post_save_receiver, sender=SubCategory)
