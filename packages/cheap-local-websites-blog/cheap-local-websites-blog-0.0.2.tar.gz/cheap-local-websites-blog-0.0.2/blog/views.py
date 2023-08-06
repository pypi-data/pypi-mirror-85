from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

def blog(request):
    latest_posts_list = Post.objects.order_by('-published')[:5]
    context = {'latest_posts_list': latest_posts_list}
    return render(request, 'blog/index.html', context)

def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post.html', {'post': post})
