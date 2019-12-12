from django.contrib import admin
from blog.models import Post, Comment, Category, SubCategory


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(SubCategory)
