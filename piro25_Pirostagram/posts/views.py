from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Post, Like, Comment, Follow, Story
from .forms import PostForm, CommentForm, StoryForm

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    stories = Story.objects.all().order_by('-created_at')

    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'posts/home.html', {
        'posts': posts,
        'stories': stories,
        'liked_posts': liked_posts,
    })

@login_required(login_url='/admin/login/')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:home')
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form})

@login_required(login_url='/admin/login/')
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('posts:home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('posts:home')
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {
        'form': form,
        'post': post,
    })


@login_required(login_url='/admin/login/')
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user:
        post.delete()

    return redirect('posts:home')

@login_required(login_url='/admin/login/')
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()
        is_liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        is_liked = True

    like_count = post.likes.count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'is_liked': is_liked,
            'like_count': like_count,
        })

    return redirect('posts:home')
    
@login_required(login_url='/admin/login/')
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect('posts:home')


@login_required(login_url='/admin/login/')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author == request.user:
        comment.delete()

    return redirect('posts:home')



@login_required(login_url='/admin/login/')
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return redirect('posts:home')

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            return redirect('posts:home')
    else:
        form = CommentForm(instance=comment)

    return render(request, 'posts/comment_form.html', {
        'form': form,
        'comment': comment,
    })

@login_required(login_url='/admin/login/')
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    return render(request, 'posts/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })

@login_required(login_url='/admin/login/')
def user_search(request):
    keyword = request.GET.get('keyword', '')
    users = []

    if keyword:
        users = User.objects.filter(username__icontains=keyword).exclude(id=request.user.id)

    return render(request, 'posts/user_search.html', {
        'keyword': keyword,
        'users': users,
    })


@login_required(login_url='/admin/login/')
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user != target_user:
        follow = Follow.objects.filter(
            follower=request.user,
            following=target_user
        )

        if follow.exists():
            follow.delete()
        else:
            Follow.objects.create(
                follower=request.user,
                following=target_user
            )

    return redirect('posts:profile', username=username)



@login_required(login_url='/admin/login/')
def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)

        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('posts:home')
    else:
        form = StoryForm()

    return render(request, 'posts/story_form.html', {
        'form': form,
    })