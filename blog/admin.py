from django.contrib import admin

# Register your models here.

from .models import BlogAuthor, BlogPost, BlogComment

admin.site.register(BlogAuthor)
admin.site.register(BlogPost)
admin.site.register(BlogComment)
