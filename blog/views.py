from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, Category, Comment, Newsletter

_HOME_TTL     = 60 * 5    # 5 minutes
_LIST_TTL     = 60 * 5
_DETAIL_TTL   = 60 * 10   # 10 minutes
_CAT_TTL      = 60 * 10


def home(request):
    """Public homepage with featured posts."""
    featured_posts = cache.get('blog:featured_posts')
    if featured_posts is None:
        featured_posts = list(Post.objects.filter(status='published', featured=True)[:3])
        cache.set('blog:featured_posts', featured_posts, _HOME_TTL)

    recent_posts = cache.get('blog:recent_posts')
    if recent_posts is None:
        recent_posts = list(Post.objects.filter(status='published')[:6])
        cache.set('blog:recent_posts', recent_posts, _HOME_TTL)

    categories = cache.get('blog:categories')
    if categories is None:
        categories = list(Category.objects.all())
        cache.set('blog:categories', categories, _CAT_TTL)

    return render(request, 'blog/home.html', {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
    })


def post_list(request):
    """List all published posts."""
    query        = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    page         = request.GET.get('page', '1')

    # Only cache unfiltered first page
    cache_key = None
    if not query and not category_slug and page == '1':
        cache_key = 'blog:post_list:p1'
        cached = cache.get(cache_key)
        if cached:
            return render(request, 'blog/post_list.html', cached)

    posts = Post.objects.filter(status='published')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    paginator = Paginator(posts, 9)
    posts_page = paginator.get_page(page)

    categories = cache.get('blog:categories') or list(Category.objects.all())

    ctx = {
        'posts': posts_page,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    }
    if cache_key:
        cache.set(cache_key, ctx, _LIST_TTL)
    return render(request, 'blog/post_list.html', ctx)


def post_detail(request, slug):
    """View a single post — not page-cached (view counter + comments are live)."""
    post = get_object_or_404(Post, slug=slug, status='published')
    post.increment_views()

    # Cache related posts and comments (not the view counter)
    related_key  = f'blog:related:{post.id}'
    comments_key = f'blog:comments:{post.id}'

    related_posts = cache.get(related_key)
    if related_posts is None:
        related_posts = list(
            Post.objects.filter(status='published', category=post.category)
            .exclude(id=post.id)[:3]
        )
        cache.set(related_key, related_posts, _DETAIL_TTL)

    comments = cache.get(comments_key)
    if comments is None:
        comments = list(post.comments.filter(is_approved=True))
        cache.set(comments_key, comments, 60 * 2)   # 2 min — comments update quickly

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
    })


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
