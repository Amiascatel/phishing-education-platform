from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, Category, Comment, Newsletter


def home(request):
    """Public homepage with featured posts."""
    featured_posts = Post.objects.filter(status='published', featured=True)[:3]
    recent_posts = Post.objects.filter(status='published')[:6]
    categories = Category.objects.all()

    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    """List all published posts."""
    posts = Post.objects.filter(status='published')

    # Search functionality
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Pagination
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """View a single post."""
    post = get_object_or_404(Post, slug=slug, status='published')
    post.increment_views()

    # Get approved comments
    comments = post.comments.filter(is_approved=True)

    # Related posts
    related_posts = Post.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def add_comment(request, slug):
    """Add a comment to a post."""
    post = get_object_or_404(Post, slug=slug, status='published')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')

        if name and email and content:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                content=content
            )
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
        else:
            messages.error(request, 'Please fill in all fields.')

    return redirect('blog:post_detail', slug=slug)


def category_posts(request, slug):
    """View posts by category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='published', category=category)

    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category_posts.html', context)


def subscribe_newsletter(request):
    """Subscribe to newsletter."""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            newsletter, created = Newsletter.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed.')
        else:
            messages.error(request, 'Please provide a valid email.')

    return redirect(request.META.get('HTTP_REFERER', 'blog:home'))


def about(request):
    """About page."""
    return render(request, 'blog/about.html')


def contact(request):
    """Contact page."""
    if request.method == 'POST':
        # Handle contact form submission
        messages.success(request, 'Thank you for your message. We will get back to you soon!')
        return redirect('blog:contact')

    return render(request, 'blog/contact.html')
