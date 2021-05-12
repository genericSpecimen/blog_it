from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from blog.models import BlogAuthor, BlogPost, BlogComment

from datetime import date

class BlogAuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_bloggers = 13
        
        for blogger_id in range(1, num_bloggers+1):
            user = User.objects.create_user(username=f'john{blogger_id}',
                                            email=f'john{blogger_id}@mail.com',
                                            password=f'testjopassword{blogger_id}')
        
            user.blogauthor.bio = f'I like books {blogger_id}.'
            user.blogauthor.location = f'Canada {blogger_id}'
            user.blogauthor.date_of_birth = date(1994, 10, 1)
            user.save()
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/bloggers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogauthor_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogauthor_list']) == 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('bloggers')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogauthor_list']) == 3)

class BlogAuthorDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
       user = User.objects.create_user(username='john',
                                       email='john@mail.com',
                                       password='testjopassword')
       
       user.blogauthor.bio = 'I like books.'
       user.blogauthor.location = 'Canada'
       user.blogauthor.date_of_birth = date(1994, 10, 1)
       user.save()
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blogger/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogger-detail', kwargs={'pk' : 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogger-detail', kwargs={'pk' : 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogauthor_detail.html')

class BlogPostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_blogposts = 13
        
        for blogpost_id in range(1, num_blogposts+1):
            user = User.objects.create_user(username=f'john {blogpost_id}',
                                            email=f'john{blogpost_id}@mail.com',
                                            password=f'testjopassword{blogpost_id}')
            
            user.blogauthor.bio = 'I like books.'
            user.blogauthor.location = 'Canada'
            user.blogauthor.date_of_birth = date(1994, 10, 1)
            user.save()
            
            BlogPost.objects.create(title=f'Hello World {blogpost_id}!',
                                description=f'This is a test description {blogpost_id}.',
                                author=user.blogauthor)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogpost_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogpost_list']) == 10)

    def test_lists_all_blogposts(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('blogs')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogpost_list']) == 3)

class BlogPostDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls): 
       user = User.objects.create_user(username='john',
                                       email='john@mail.com',
                                       password='testjopassword')
       
       user.blogauthor.bio = 'I like books.'
       user.blogauthor.location = 'Canada'
       user.blogauthor.date_of_birth = date(1994, 10, 1)
       user.save()
       
       BlogPost.objects.create(title='Hello World!',
                               description='This is a test description.',
                               author=user.blogauthor)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blog/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogpost-detail', kwargs={'pk' : 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogpost-detail', kwargs={'pk' : 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogpost_detail.html')

class BlogCommentCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls): 
       user = User.objects.create_user(username='john',
                                       email='john@mail.com',
                                       password='testjopassword')
       
       user.blogauthor.bio = 'I like books.'
       user.blogauthor.location = 'Canada'
       user.blogauthor.date_of_birth = date(1994, 10, 1)
       user.save()
       
       BlogPost.objects.create(title='Hello World!',
                               description='This is a test description.',
                               author=user.blogauthor)
    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='john', password='testjopassword')
        response = self.client.get('/blog/blog/1/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='john', password='testjopassword')
        response = self.client.get(reverse('blogcomment-create', kwargs={'pk' : 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='john', password='testjopassword')
        response = self.client.get(reverse('blogcomment-create', kwargs={'pk' : 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogcomment_form.html')
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('blogcomment-create', kwargs={'pk' : 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/blog/blog/1/create/')

    def test_form_blog_field(self):
        login = self.client.login(username='john', password='testjopassword')
        response = self.client.get(reverse('blogcomment-create', kwargs={'pk' : 1}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['blogpost'], BlogPost.objects.get(id=1))
