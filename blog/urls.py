from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('blogs/', views.BlogPostListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.BlogPostDetailView.as_view(), name='blogpost-detail'),
    
    path('bloggers/', views.BlogAuthorListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>/', views.BlogAuthorDetailView.as_view(), name='blogger-detail'),
    path('blogger/update/', views.BlogAuthorUpdateView.as_view(), name='blogger-update'),
    
    path('blog/<int:pk>/create/', views.BlogCommentCreateView.as_view(), name='blogcomment-create'),
    path('blog/category/<category>/', views.BlogCategoryPostsListView.as_view(), name='blogcategoryposts-list'),
    path('blog/category-create/', views.BlogCategoryCreateView.as_view(), name='blogcategory-create'),
    path('blog/create/', views.BlogPostCreateView.as_view(), name='blogpost-create')
]
