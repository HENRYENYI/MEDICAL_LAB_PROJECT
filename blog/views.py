from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost, BlogCategory

def blog_home(request):
    """Blog home page with featured posts and recent posts"""
    featured_posts = BlogPost.objects.filter(status='published', is_featured=True)[:3]
    recent_posts = BlogPost.objects.filter(status='published')[:6]
    categories = BlogCategory.objects.all()
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
    }
    return render(request, 'blog/blog_home.html', context)

def blog_list(request):
    """List all blog posts with pagination and search"""
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category')
    
    posts = BlogPost.objects.filter(status='published')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        )
    
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = BlogCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'current_category': category_slug,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    """Individual blog post detail"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    related_posts = BlogPost.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/blog_detail.html', context)

def blog_category(request, slug):
    """Posts by category"""
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = BlogPost.objects.filter(status='published', category=category)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/blog_category.html', context)