from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag, Like, Follow, Profile
from .forms import PostForm, CommentForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

# Home / list view with pagination
def post_list(request):
    qs = Post.objects.filter(status='published').select_related('author').prefetch_related('tags')[:]
    paginator = Paginator(qs, 8)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': categories, 'tags': tags})

def post_detail(request, pk, slug):
    post = get_object_or_404(Post, pk=pk, slug=slug)
    comment_form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            if request.user.is_authenticated:
                c.user = request.user
            c.save()
            messages.success(request, 'Comment added.')
            return redirect('post_detail', pk=post.pk, slug=post.slug)
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form, 'liked': liked})

@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        p = form.save(commit=False)
        p.author = request.user
        p.save()
        form.save_m2m()
        messages.success(request, 'Post created.')
        return redirect('post_detail', pk=p.pk, slug=p.slug)
    return render(request, 'blog/post_form.html', {'form': form, 'create': True})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        p = form.save()
        messages.success(request, 'Post updated.')
        return redirect('post_detail', pk=p.pk, slug=p.slug)
    return render(request, 'blog/post_form.html', {'form': form, 'create': False})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def category_posts(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    qs = cat.posts.filter(status='published')
    paginator = Paginator(qs, 8)
    posts = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': Category.objects.all(), 'tags': Tag.objects.all(), 'category': cat})

def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    qs = tag.posts.filter(status='published')
    paginator = Paginator(qs, 8)
    posts = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': Category.objects.all(), 'tags': Tag.objects.all(), 'tag': tag})

def search(request):
    q = request.GET.get('q', '')
    qs = Post.objects.filter(status='published').filter(Q(title__icontains=q) | Q(content__icontains=q))
    paginator = Paginator(qs, 8)
    posts = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/post_list.html', {'posts': posts, 'search_query': q, 'categories': Category.objects.all(), 'tags': Tag.objects.all()})

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Registration successful.')
        return redirect('post_list')
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('post_list')
    return render(request, 'blog/login.html', {'form': form})

def logout_user(request):
    # simple logout handler (works via GET too) - suitable for portfolio demo
    logout(request)
    return redirect('post_list')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('post_detail', pk=post.pk, slug=post.slug)

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.filter(status='published')
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'blog/profile.html', {'profile_user': user, 'posts': posts, 'following': following})

@login_required
def follow_view(request, username):
    target = get_object_or_404(User, username=username)
    if request.user == target:
        messages.error(request, 'You cannot follow yourself.')
        return redirect('profile_view', username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
    return redirect('profile_view', username=target.username)
