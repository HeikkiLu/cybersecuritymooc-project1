from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import connection
from django.http import HttpResponse

from .forms import CommentForm, CreateBlogForm
from .models import Post


# Create your views here.

def frontpage(request):
    posts = Post.objects.all()
    query = request.GET.get('search')
    if query:
        posts = Post.objects.raw("SELECT * FROM blog_post WHERE title LIKE '%{}%'".format(query))
    # FIX FLAW 1:
    #    posts = Post.objects.filter(title__icontains=query)


    return render(request, 'blog/frontpage.html', {'posts': posts})


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = request.user
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def createblog(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.created_by = request.user
            blog.save()
            return redirect('/')
    else:
        form = CreateBlogForm()

    return render(request, 'blog/create_blog.html', {'form': form})

    
