from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .forms import AdminPostForm, CommentForm, PostForm, RegistrationForm, UserProfileForm
from .models import Comment, Like, Post, UserProfile
from .permissions import get_manageable_posts, is_site_admin, user_can_delete_post, user_can_manage_post

POST_GALLERY_IMAGES = {
    'easy-one-pot-cooking-ideas': [
        'blog/images/cooking-photo-1.png',
        'blog/images/recipe-1.png',
        'blog/images/cooking-photo-2.png',
    ],
    'weekend-brunch-recipes': [
        'blog/images/recipe-2.png',
        'blog/images/brunch.svg',
        'blog/images/recipe-3.png',
    ],
    'sheet-pan-comfort-foods': [
        'blog/images/recipe-1.png',
        'blog/images/sheet-pan.svg',
    ],
    'the-joy-of-home-baking': [
        'blog/images/home-baking.svg',
        'blog/images/cooking-photo-2.png',
    ],
    'weekend-travel-essentials': [
        'blog/images/travel-photo-1.png',
        'blog/images/travel-packing.svg',
    ],
    'minimalist-lifestyle-habits': [
        'blog/images/lifestyle-photo-1.png',
        'blog/images/minimalist-routine.svg',
    ],
    'morning-routines-for-better-focus': [
        'blog/images/lifestyle-photo-2.png',
        'blog/images/morning-focus.svg',
    ],
    'home-theater-setup-guide': [
        'blog/images/home-theater.svg',
        'blog/images/entertainment-photo-1.png',
    ],
    'streaming-service-show-reviews': [
        'blog/images/streaming.svg',
        'blog/images/entertainment-photo-1.png',
    ],
    'tech-gadgets-for-home-entertainment': [
        'blog/images/entertainment-gadgets.svg',
        'blog/images/tech-photo-1.png',
    ],
    'top-kitchen-gadgets-reviewed': [
        'blog/images/kitchen-gadget-review.svg',
        'blog/images/reviews-photo-1.png',
    ],
}

CATEGORY_GALLERY_IMAGES = {
    'cooking': [
        'blog/images/cooking-photo-1.png',
        'blog/images/cooking-photo-2.png',
        'blog/images/recipe-1.png',
    ],
    'lifestyle': [
        'blog/images/lifestyle-photo-1.png',
        'blog/images/lifestyle-photo-2.png',
        'blog/images/lifestyle.svg',
    ],
    'entertainment': [
        'blog/images/entertainment-photo-1.png',
        'blog/images/streaming.svg',
    ],
    'reviews': [
        'blog/images/reviews-photo-1.png',
        'blog/images/reviews.svg',
    ],
    'technology': [
        'blog/images/tech-photo-1.png',
        'blog/images/technology.svg',
    ],
    'travel': [
        'blog/images/travel-photo-1.png',
        'blog/images/travel-packing.svg',
    ],
}


def _get_post_form(user):
    if is_site_admin(user):
        return AdminPostForm
    return PostForm


def _redirect_after_login(user):
    if is_site_admin(user):
        return redirect('blog:admin_dashboard')
    return redirect('blog:user_dashboard')


def _increment_view_count(request, post):
    session_key = f'viewed_post_{post.pk}'
    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(view_count=post.view_count + 1)
        post.view_count += 1
        request.session[session_key] = True


def index(request):
    published_posts = Post.objects.filter(published=True)
    recent_posts = published_posts.select_related('author')[:3]
    author_count = published_posts.values('author').distinct().count()
    return render(request, 'blog/index.html', {
        'recent_posts': recent_posts,
        'post_count': published_posts.count(),
        'author_count': author_count,
    })


def post_list(request):
    posts = Post.objects.filter(published=True).select_related('author')
    # Dynamically get all unique categories from posts
    unique_categories = posts.values_list('category', flat=True).distinct().order_by('category')
    category_groups = []
    for category_slug in unique_categories:
        category_posts = posts.filter(category=category_slug)
        if category_posts.exists():
            category_groups.append({
                'slug': category_slug,
                'label': category_slug.title(),
                'posts': category_posts,
                'count': category_posts.count(),
            })
    return render(request, 'blog/post_list.html', {
        'category_groups': category_groups,
        'posts': posts,
    })


def detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author'), pk=post_id)
    if not post.published and not user_can_manage_post(request.user, post):
        raise Http404('Post not found')

    if post.published:
        _increment_view_count(request, post)

    hero_image = post.image.url if post.image else '/static/blog/images/default.svg'
    
    # Get comments and likes
    comments = post.comments.select_related('user').all()
    like_count = post.likes.count()
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(user=request.user).exists()
    
    comment_form = CommentForm() if request.user.is_authenticated else None

    return render(request, 'blog/detail.html', {
        'post': post,
        'hero_image': hero_image,
        'can_manage_post': user_can_manage_post(request.user, post),
        'comments': comments,
        'like_count': like_count,
        'is_liked': is_liked,
        'comment_form': comment_form,
    })


def author_list(request):
    authors = (
        User.objects
        .filter(posts__published=True)
        .annotate(post_count=Count('posts'))
        .order_by('username')
        .distinct()
    )
    return render(request, 'blog/author_list.html', {'authors': authors})


def author_detail(request, user_id):
    author = get_object_or_404(User, pk=user_id)
    posts = author.posts.filter(published=True).select_related('author')
    return render(request, 'blog/author_detail.html', {
        'author': author,
        'posts': posts,
    })


def category_list(request):
    # Dynamically fetch all unique categories from published posts
    categories_data = (
        Post.objects
        .filter(published=True)
        .values('category')
        .annotate(count=Count('id'))
        .order_by('category')
    )
    
    categories = [
        {'slug': item['category'], 'label': item['category'].title(), 'count': item['count']}
        for item in categories_data
    ]
    
    return render(request, 'blog/category_list.html', {'categories': categories})


def category_detail(request, category_slug):
    # Check if category exists in published posts
    if not Post.objects.filter(published=True, category=category_slug).exists():
        raise Http404('Category not found')
    
    category_label = category_slug.title()
    posts = Post.objects.filter(published=True, category=category_slug).select_related('author')
    
    return render(request, 'blog/category_detail.html', {
        'category_label': category_label,
        'category_slug': category_slug,
        'posts': posts,
    })


def user_login(request):
    if request.user.is_authenticated:
        return _redirect_after_login(request.user)

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None:
            error = 'Invalid username or password.'
        elif is_site_admin(user):
            error = 'Admin accounts must sign in through the admin portal.'
        else:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            next_url = request.GET.get('next') or reverse('blog:user_dashboard')
            return redirect(next_url)

    return render(request, 'blog/login.html', {'error': error})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('blog:index')


@login_required(login_url='blog:user_login')
def profile(request, username):
    """View user profile."""
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    posts = user.posts.filter(published=True).select_related('author')
    
    is_own_profile = request.user == user
    
    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_own_profile': is_own_profile,
    })


@login_required(login_url='blog:user_login')
def edit_profile(request):
    """Edit user profile."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'blog/edit_profile.html', {'form': form})


@login_required(login_url='blog:user_login')
@require_POST
def like_post(request, post_id):
    """Like or unlike a post via AJAX."""
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # User already liked, so unlike
        like.delete()
        liked = False
    else:
        liked = True
    
    like_count = post.likes.count()
    
    return JsonResponse({
        'liked': liked,
        'like_count': like_count
    })


@login_required(login_url='blog:user_login')
@require_POST
def add_comment(request, post_id):
    """Add a comment to a post."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        messages.success(request, 'Your comment has been added.')
    else:
        messages.error(request, 'There was an error adding your comment.')
    
    return redirect('blog:detail', post_id=post_id)


def user_register(request):
    if request.user.is_authenticated:
        return _redirect_after_login(request.user)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            messages.success(request, f'Welcome to Inkspire, {user.get_full_name() or user.username}!')
            return redirect('blog:user_dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'blog/register.html', {'form': form})


@login_required(login_url='blog:user_login')
def user_dashboard(request):
    if is_site_admin(request.user):
        return redirect('blog:admin_dashboard')

    posts = request.user.posts.all().order_by('-created_at')
    total_views = posts.aggregate(total=Sum('view_count'))['total'] or 0
    published_count = posts.filter(published=True).count()
    
    # Likes and comments analytics
    total_likes = posts.annotate(like_count=Count('likes')).aggregate(total=Sum('like_count'))['total'] or 0
    total_comments = posts.annotate(comment_count=Count('comments')).aggregate(total=Sum('comment_count'))['total'] or 0
    recent_comments = Comment.objects.filter(post__author=request.user).select_related('user', 'post').order_by('-created_at')[:5]

    return render(request, 'blog/dashboard.html', {
        'posts': posts,
        'analytics': {
            'total_posts': posts.count(),
            'published_posts': published_count,
            'draft_posts': posts.filter(published=False).count(),
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'top_post': posts.annotate(like_count=Count('likes')).order_by('-like_count', '-view_count').first(),
            'avg_views': round(total_views / posts.count(), 1) if posts.count() else 0,
        },
        'recent_comments': recent_comments,
    })


@login_required(login_url='blog:user_login')
def admin_dashboard(request):
    if not is_site_admin(request.user):
        return redirect('blog:user_dashboard')

    # Overall stats
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(published=True).count()
    total_views = Post.objects.aggregate(total=Sum('view_count'))['total'] or 0
    total_authors = User.objects.filter(posts__isnull=False).distinct().count()
    total_likes = Like.objects.count()
    total_comments = Comment.objects.count()

    # Author performance
    authors = (
        User.objects
        .filter(posts__isnull=False)
        .annotate(
            post_count=Count('posts'),
            total_views=Sum('posts__view_count'),
            published_count=Count('posts', filter=Q(posts__published=True)),
            total_likes=Count('posts__likes'),
            total_comments=Count('posts__comments')
        )
        .order_by('-total_views')
    )

    # Post performance
    posts = Post.objects.select_related('author').annotate(
        like_count=Count('likes'),
        comment_count=Count('comments')
    ).order_by('-view_count')
    
    # Recent comments across all posts
    recent_comments = Comment.objects.select_related('user', 'post', 'post__author').order_by('-created_at')[:10]

    return render(request, 'blog/admin_dashboard.html', {
        'overall_stats': {
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': total_posts - published_posts,
            'total_views': total_views,
            'total_authors': total_authors,
            'total_likes': total_likes,
            'total_comments': total_comments,
        },
        'authors': authors,
        'posts': posts,
        'recent_comments': recent_comments,
    })


@login_required(login_url='blog:user_login')
def create_post(request):
    if is_site_admin(request.user):
        messages.info(request, 'Admins cannot create posts. Use the admin dashboard to manage content.')
        return redirect('blog:admin_dashboard')

    form_class = _get_post_form(request.user)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created.')
            return redirect(post.get_absolute_url())
    else:
        form = form_class()

    return render(request, 'blog/post_form.html', {
        'form': form,
        'form_title': 'Create a new post',
        'form_subtitle': 'Publish a new article to Inkspire.',
        'submit_label': 'Publish post',
    })


@login_required(login_url='blog:user_login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not user_can_manage_post(request.user, post):
        return HttpResponseForbidden('You do not have permission to edit this post.')

    form_class = _get_post_form(request.user)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            if not is_site_admin(request.user):
                updated_post.author = request.user
            updated_post.save()
            messages.success(request, 'Post updated successfully.')
            return redirect(updated_post.get_absolute_url())
    else:
        form = form_class(instance=post)

    return render(request, 'blog/post_form.html', {
        'form': form,
        'post': post,
        'form_title': 'Edit post',
        'form_subtitle': f'Update "{post.title}".',
        'submit_label': 'Save changes',
    })


@login_required(login_url='blog:user_login')
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not user_can_delete_post(request.user, post):
        return HttpResponseForbidden('You do not have permission to delete this post.')

    title = post.title
    post.delete()
    messages.success(request, f'"{title}" has been deleted.')

    if is_site_admin(request.user):
        return redirect('blog:admin_dashboard')
    return redirect('blog:user_dashboard')


def old_url_redirect(request):
    return redirect(reverse('blog:new_url'))


def new_url_view(request):
    return HttpResponse('This is the new URL view.')
