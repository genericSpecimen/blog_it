from django.shortcuts import render

# Create your views here.

from .models import BlogAuthor, BlogPost, BlogComment

def index(request):
    """
    View function for the home page of the website.
    """
    
    num_blogauthors = BlogAuthor.objects.all().count()
    num_blogposts = BlogPost.objects.all().count()
    num_blogcomments = BlogComment.objects.all().count()
    
    context = {
        'num_blogauthors' : num_blogauthors,
        'num_blogposts' : num_blogposts,
        'num_blogcomments': num_blogcomments,
    }
    
    return render(request, 'index.html', context=context)
