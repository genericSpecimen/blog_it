from django.test import TestCase

from django.contrib.auth.models import User
from blog.models import BlogAuthor, BlogPost, BlogComment

from datetime import date

class BlogAuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
       user = User.objects.create_user(username='john',
                                       email='john@mail.com',
                                       password='testjopassword')
       
       user.blogauthor.bio = 'I like books.'
       user.blogauthor.location = 'Canada'
       user.blogauthor.date_of_birth = date(1994, 10, 1)
       user.save()
       #BlogAuthor.objects.create(user=user,
                                 #bio='I like books.',
                                 #location='Canada',
                                 #date_of_birth=date(1994, 10, 1))
       
    def test_bio_label(self):
        blogger = BlogAuthor.objects.get(id=1)
        field_label = blogger._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'bio')
    
    def test_location_label(self):
        blogger = BlogAuthor.objects.get(id=1)
        field_label = blogger._meta.get_field('location').verbose_name
        self.assertEqual(field_label, 'location')
    
    def test_date_of_birth_label(self):
        blogger = BlogAuthor.objects.get(id=1)
        field_label = blogger._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')
    
    def test_date_of_death_label(self):
        blogger = BlogAuthor.objects.get(id=1)
        field_label = blogger._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'date of death')
    
    def test_bio_max_length(self):
        blogger = BlogAuthor.objects.get(id=1)
        max_length = blogger._meta.get_field('bio').max_length
        self.assertEqual(max_length, 200)
        
    def test_location_max_length(self):
        blogger = BlogAuthor.objects.get(id=1)
        max_length = blogger._meta.get_field('location').max_length
        self.assertEqual(max_length, 30)
    
    def test_object_name_is_last_name_comma_first_name(self):
        blogger = BlogAuthor.objects.get(id=1)
        expected_object_name = f'{blogger.user.last_name}, {blogger.user.first_name}'
        self.assertEqual(expected_object_name, str(blogger))
    
    def test_get_absolute_url(self):
        blogger = BlogAuthor.objects.get(id=1)
        self.assertEqual(blogger.get_absolute_url(), '/blog/blogger/1')

class BlogPostModelTest(TestCase):
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
       
    def test_title_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')
    
    def test_description_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')
    
    def test_author_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')
    
    def test_post_date_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('post_date').verbose_name
        self.assertEqual(field_label, 'post date')  
    
    def test_title_max_length(self):
        blogpost = BlogPost.objects.get(id=1)
        max_length = blogpost._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)
    
    def test_description_max_length(self):
        blogpost = BlogPost.objects.get(id=1)
        max_length = blogpost._meta.get_field('description').max_length
        self.assertEqual(max_length, 2000)
    
    def test_title_help_text(self):
        blogpost = BlogPost.objects.get(id=1)
        help_text = blogpost._meta.get_field('title').help_text
        self.assertEqual(help_text, 'Enter a short and crisp title here.')

    def test_description_help_text(self):
        blogpost = BlogPost.objects.get(id=1)
        help_text = blogpost._meta.get_field('description').help_text
        self.assertEqual(help_text, 'Write your thoughts in detail here.')
    
    def test_get_absolute_url(self):
        blogpost = BlogPost.objects.get(id=1)
        self.assertEqual(blogpost.get_absolute_url(), '/blog/blog/1')
    
    def test_object_name_is_blogpost_title(self):
        blogpost = BlogPost.objects.get(id=1)
        expected_object_name = f'{blogpost.title}'
        self.assertEqual(expected_object_name, str(blogpost))

class BlogCommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
       user = User.objects.create_user(username='john',
                                       email='john@mail.com',
                                       password='testjopassword')
       
       user.blogauthor.bio = 'I like books.'
       user.blogauthor.location = 'Canada'
       user.blogauthor.date_of_birth = date(1994, 10, 1)
       user.save()
       
       blogpost = BlogPost.objects.create(title='Hello World!',
                                          description='This is a test description.',
                                          author=user.blogauthor)
       
       blogcomment = BlogComment.objects.create(text='Thank you for the kind words. I hope you\'re doing well.',
                                                author=user.blogauthor,
                                                blog=blogpost)
    
    def test_text_label(self):
        blogcomment = BlogComment.objects.get(id=1)
        field_label = blogcomment._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_author_label(self):
        blogcomment = BlogComment.objects.get(id=1)
        field_label = blogcomment._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')
    
    def test_comment_date_label(self):
        blogcomment = BlogComment.objects.get(id=1)
        field_label = blogcomment._meta.get_field('comment_date').verbose_name
        self.assertEqual(field_label, 'comment date')
    
    def test_blog_label(self):
        blogcomment = BlogComment.objects.get(id=1)
        field_label = blogcomment._meta.get_field('blog').verbose_name
        self.assertEqual(field_label, 'blog')

    def test_text_max_length(self):
        blogcomment = BlogComment.objects.get(id=1)
        max_length = blogcomment._meta.get_field('text').max_length
        self.assertEqual(max_length, 1000)
    
    def test_text_help_text(self):
        blogcomment = BlogComment.objects.get(id=1)
        help_text = blogcomment._meta.get_field('text').help_text
        self.assertEqual(help_text, 'Post your thoughts on this blog post here...')
    
    def test_object_name_is_LE_53_chars(self):
        blogcomment = BlogComment.objects.get(id=1)
        # 50 + 3 for the "..."
        self.assertTrue(len(str(blogcomment)) <= 53)
