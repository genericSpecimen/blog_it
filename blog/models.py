from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

from datetime import date


# Create your models here.

class BlogAuthor(models.Model):
    """
    Model representing an author of a blog.
    An author can have 0 or more blog posts.
    
    https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#extending-the-existing-user-model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=200, null=True, blank=True, help_text="Write a few words about yourself here...")
    location = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['user', 'bio']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance.
        Reverses the author-detail URL mapping to get the URL for
        displaying an individual author.
        """
        # author detail url
        #return reverse('author-detail', args=[str(self.id)])
        pass
    
    def __str__(self):
        return f'{self.user.username} ({self.user.last_name}, {self.user.first_name})'

class BlogPost(models.Model):
    """
    Model representing a single blog post.
    A post can have only one author.
    """
    title = models.CharField(max_length=100, help_text="Enter a short and crisp title here.")
    description = models.TextField(max_length=2000, help_text="Write your thoughts in detail here.")
    
    # set the value of the posts's author field to NULL if the associated author record is deleted.
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
    
    post_date = models.DateField(default=date.today)
    
    class Meta:
        ordering = ["-post_date"]
    
    def get_absolute_url(self):
        # blog detail url
        return reverse('blogpost-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.title

class BlogComment(models.Model):
    """
    A model representing a comment on a blog post.
    """
    text = models.TextField(max_length=1000, help_text="Post your thoughts on this blog post here...")
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
    
    # auto_now_add updates the value with the time and date of creation of record.
    comment_date = models.DateTimeField(auto_now_add=True)
    
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["comment_date"]
    
    def __str__(self):
        max_len = 50
        if (len(self.text) > max_len):
            return self.text[:max_len] + "..."
        return self.text
 
