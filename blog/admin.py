from django.contrib import admin

# Register your models here.

from .models import BlogAuthor, BlogPost, BlogComment, BlogCategory

class BlogPostInline(admin.TabularInline):
    model = BlogPost
    extra = 0

class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0

class BlogCategoryInline(admin.TabularInline):
    model = BlogPost.categories.through
    extra = 0

@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'date_of_birth')
    list_filter = ('location',)
    
    inlines = [BlogPostInline, BlogCommentInline]

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'post_date')
    list_filter = ('author', 'post_date')
    
    inlines = [BlogCommentInline, BlogCategoryInline]
    exclude = ('categories',)

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'comment_date', 'blog')
    list_filter = ('comment_date', 'blog')
    
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    
    inline = [BlogCategoryInline]
