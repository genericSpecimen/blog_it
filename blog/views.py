from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

# Create your views here.
from .models import BlogAuthor, BlogPost, BlogComment, BlogCategory, UserFollowing
from .forms import UserSignUpForm, UserUpdateForm

from datetime import date

import random

def index(request):
    """
    View function for the home page of the website.
    """
    
    items = list(BlogPost.objects.all())
    #print(items)
    
    featured_blogposts = None
    try:
        featured_blogposts = random.sample(items, 2)
        #print(featured_blogposts)
    except ValueError as err:
        print("ValueError: ", err)
    
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
    
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        if filter_val:
            return BlogPost.objects.filter(categories__name__icontains=filter_val)
        return BlogPost.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context
        
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

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """
    A form for creating a blog post.
    This action requires login.
    """
    model = BlogPost
    # author and post_date will be automatically set
    # author = current user
    # post_date = date.today()
        
    fields = ['title', 'categories', 'description']
    
    def form_valid(self, form):
        """
        Add the author and the date info
        to the form data before setting it
        as valid and saving the form instance.
        """
        
        # the author of the blogpost is simply the logged in user who makes this request
        form.instance.author = BlogAuthor.objects.get(user=self.request.user)
        
        form.instance.post_date = date.today()
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
        Adds the blog author information to
        display it in the form template.
        """
        
        # get base implementation context
        context = super().get_context_data(**kwargs)
        # get the blog post and add it to the context
        context['blogauthor'] = BlogAuthor.objects.get(user=self.request.user)
        
        return context
    
    def get_success_url(self):
        return reverse('blogpost-detail', args=(self.object.id,))

class BlogCategoryCreateView(LoginRequiredMixin, CreateView):
    model = BlogCategory
    fields = ['name']
    
    def get_success_url(self):
        return reverse('blogpost-create')

class BlogCategoryPostsListView(generic.ListView):
    paginate_by = 10
    
    def get_queryset(self):
        return BlogPost.objects.filter(categories__name__icontains=self.kwargs['category'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context
    
class UserSignUpCreateView(CreateView):
    template_name = 'registration/signup.html'
    # We have to use reverse_lazy() instead of reverse(), as the urls are not loaded when the file is imported.
    success_url = reverse_lazy('login')
    form_class = UserSignUpForm

class BlogAuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogAuthor
    fields = ['bio', 'location', 'date_of_birth']
    
    def get_object(self):
        return self.request.user.blogauthor
    
    def get_success_url(self):
        return reverse('blogger-detail', kwargs={'pk' : self.request.user.blogauthor.id})
    
class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    
    def get_success_url(self):
        return reverse('blogger-detail', kwargs={'pk' : self.request.user.blogauthor.id})

@login_required
def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, _('Account information successfully updated!'))
            
            return redirect('blogger-detail', pk=request.user.blogauthor.id)
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request,
                  'registration/update.html', {
                        'form' : form
                    })

class BlogAuthorFollowersListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    
    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        #print(user.followers.all())
        #for object1 in user.followers.all():
        #    print(object1.following_user_id)
        return user.followers.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'followers'
        user = User.objects.get(id=self.kwargs['pk'])
        context['user'] = user
        #print(context)
        return context

class BlogAuthorFollowingListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        #print(user.following.all())
        #for object1 in user.following.all():
        #    print(object1.following_user_id.blogauthor.get_absolute_url())
        return user.following.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'following'
        user = User.objects.get(id=self.kwargs['pk'])
        context['user'] = user
        print(context)
        return context

class UserFollowingCreateView(LoginRequiredMixin, CreateView):
    model = UserFollowing
    fields = ['follower_user_id', 'following_user_id']
    
    def get_initial(self):
        initial = super().get_initial()
        initial['follower_user_id'] = self.request.user
        initial['following_user_id'] = self.kwargs['pk']
        return initial
    
    def get_success_url(self):
        return reverse('blogger-detail', kwargs={'pk' : self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertofollow'] = User.objects.get(id=self.kwargs['pk'])
        return context

class UserFollowingBlogPostListView(LoginRequiredMixin, generic.ListView):
    model = BlogPost
    paginate_by = 10

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        if filter_val:
            return BlogPost.objects.filter(author__user__followers__follower_user_id=self.request.user,
                                                categories__name__icontains=filter_val)
        return BlogPost.objects.filter(author__user__followers__follower_user_id=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userfeed'] = True
        return context
