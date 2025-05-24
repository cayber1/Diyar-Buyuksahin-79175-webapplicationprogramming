from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import viewsets
from .models import Post
from .forms import PostForm, ProfileForm
from .serializers import PostSerializer
from .tasks import send_post_notification  # <-- Celery görevi eklendi

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'core/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'core/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            send_post_notification.delay(post.id)  # <-- Celery görevi burada çağrılıyor
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'core/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'core/post_form.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'core/post_confirm_delete.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile_detail(request):
    return render(request, 'core/profile_detail.html', {'user': request.user})

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/profile_form.html', {'form': form})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
