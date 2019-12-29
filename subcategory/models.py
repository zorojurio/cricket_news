from django.db import models
from category.models import Category


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
