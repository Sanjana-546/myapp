from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.urls import reverse

from .models import Post


def index(request):
    recent_posts = Post.objects.filter(published=True)[:3]
    return render(request, 'blog/index.html', {'recent_posts': recent_posts})


def post_list(request):
    posts = Post.objects.filter(published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id, published=True)
    return render(request, 'blog/detail.html', {'post': post})


def old_url_redirect(request):
    return redirect(reverse('blog:new_url'))


def new_url_view(request):
    return HttpResponse("This is the new URL view.")
