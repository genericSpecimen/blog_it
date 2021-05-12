from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import BlogAuthor, BlogPost, BlogComment
from .forms import UserSignUpForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from django.urls import reverse, reverse_lazy

import random

def index(request):
    """
    View function for the home page of the website.
    """
    
    items = list(BlogPost.objects.all())
    #print(items)
    featured_blogposts = random.sample(items, 2)
    #print(featured_blogposts)
    
    num_blogauthors = BlogAuthor.objects.all().count()
    num_blogposts = BlogPost.objects.all().count()
    num_blogcomments = BlogComment.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'featured_blogposts': featured_blogposts,
        'num_blogauthors'   : num_blogauthors,
        'num_blogposts'     : num_blogposts,
        'num_blogcomments'  : num_blogcomments,
        'num_visits'        : num_visits
    }
    
    return render(request, 'index.html', context=context)

class BlogPostListView(generic.ListView):
    model = BlogPost
    paginate_by = 10

class BlogPostDetailView(generic.DetailView):
    model = BlogPost

class BlogAuthorListView(generic.ListView):
    model = BlogAuthor
    paginate_by = 10

class BlogAuthorDetailView(generic.DetailView):
    model = BlogAuthor

class BlogCommentCreateView(LoginRequiredMixin, CreateView):
    """
    A form for commenting on a blog post.
    This action requires login.
    """
    model = BlogComment
    fields = ['text']
    
    def form_valid(self, form):
        """
        Add the author and associated blog info
        to the form data before setting it as valid
        and saving the form instance.
        """
        
        # the author of the comment is simply the logged in user who makes this request
        form.instance.author = BlogAuthor.objects.get(user=self.request.user)
        
        # set the blog post on which the comment is made
        form.instance.blog = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
        Adds the blog post information to display it
        in the form template.
        """
        
        # get base implementation context
        context = super().get_context_data(**kwargs)
        # get the blog post and add it to the context
        context['blogpost'] = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
        
        return context
    
    def get_success_url(self):
        return reverse('blogpost-detail', kwargs={'pk' : self.kwargs['pk']})

class UserSignUpCreateView(CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserSignUpForm
    
