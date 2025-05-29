from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from .models import Post

# 게시판 목록
def donation_list(request):
    postlist = Post.objects.filter(post_type='donation').order_by('-created_at')
    paginator = Paginator(postlist, 10)  # 페이지당 게시글 수수
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    popular_posts = (
        Post.objects
            .filter(post_type='donation', views__gt=0)
            .order_by('-views')[:5]
    )   

    return render(request, 'posts/donation_list.html', {
        'page_obj': page_obj,
        'popular_posts': popular_posts
    })

def request_list(request):
    postlist = Post.objects.filter(post_type='request').order_by('-created_at')
    paginator = Paginator(postlist, 10)  # 페이지당 게시글 수수
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    popular_posts = (
        Post.objects
            .filter(post_type='donation', views__gt=0)
            .order_by('-views')[:5]
    )

    return render(request, 'posts/request_list.html', {
        'page_obj': page_obj,
        'popular_posts': popular_posts
    })


def story_list(request):
    postlist = Post.objects.filter(post_type='story').order_by('-created_at')
    paginator = Paginator(postlist, 10)  # 페이지당 게시글 수수
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    popular_posts = (
        Post.objects
            .filter(post_type='donation', views__gt=0)
            .order_by('-views')[:5]
    )
    
    return render(request, 'posts/story_list.html', {
        'page_obj': page_obj,
        'popular_posts': popular_posts
    })
def announcement_list(request):
    postlist = Post.objects.filter(post_type='announcement').order_by('-created_at')
    paginator = Paginator(postlist, 10)  # 페이지당 게시글 수수
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/announcement_list.html', {
        'page_obj': page_obj,
    })

# 게시글 상세 보기
def donation_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id, post_type='donation')
    
    session_key = f'viewed_post_{post_id}'

    if not request.session.get(session_key, False):
        post.views += 1
        post.save()
        request.session[session_key] = True  # 본 글이라고 표시

    return render(request, 'posts/donation_detail.html', {'post': post})


def request_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id, post_type='request')
    
    session_key = f'viewed_post_{post_id}'
    if not request.session.get(session_key, False):
        post.views += 1
        post.save()
        request.session[session_key] = True

    return render(request, 'posts/request_detail.html', {'post': post})

def story_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id, post_type='story')
    
    session_key = f'viewed_post_{post_id}'
    if not request.session.get(session_key, False):
        post.views += 1
        post.save()
        request.session[session_key] = True

    return render(request, 'posts/story_detail.html', {'post': post})

def announcement_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id, post_type='announcement')
    
    session_key = f'viewed_post_{post_id}'
    if not request.session.get(session_key, False):
        post.views += 1
        post.save()
        request.session[session_key] = True

    return render(request, 'posts/announcement_detail.html', {'post': post})

# 게시글 작성
def create_post(request, post_type):
    VALID_POST_TYPES = ['donation', 'request', 'story', 'announcement']
    if post_type not in VALID_POST_TYPES:
        return render(request, '404.html')

    # 1) 로그인 체크
    if not request.user.is_authenticated:
        messages.warning(request, "로그인이 필요한 기능입니다.")
        # 이전 페이지로 돌아가되, 없으면 메인으로
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # 2) 공지사항 권한 체크
    if post_type == 'announcement' and not request.user.is_superuser:
        return render(request, '403.html')

    if request.method == 'POST':
        title    = request.POST.get('title')
        content  = request.POST.get('content')
        category = request.POST.get('category') if post_type in ['donation','request'] else None

        Post.objects.create(
            title=title,
            content=content,
            post_type=post_type,
            category=category,
            author=request.user
        )
        return redirect(f'/posts/{post_type}/')

    return render(request, 'posts/post_form.html', {'post_type': post_type})

@login_required
def post_update(request, post_type, post_id):
    VALID_POST_TYPES = ['donation', 'request', 'story', 'announcement']
    if post_type not in VALID_POST_TYPES:
        return render(request, '404.html')

    post = get_object_or_404(Post, id=post_id, post_type=post_type)

    # 권한 확인
    if post.author != request.user:
        return render(request, '403.html')

    if post_type == 'announcement' and not request.user.is_superuser:
        return render(request, '403.html')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')

        if post_type in ['donation', 'request']:
            post.category = request.POST.get('category')

        post.save()
        return redirect(reverse(f'{post_type}_detail', args=[post.id]))

    return render(request, 'posts/post_form.html', {
        'post': post,
        'mode': 'update',
        'post_type': post_type
    })

@login_required
def post_delete(request, post_type, post_id):
    VALID_POST_TYPES = ['donation', 'request', 'story', 'announcement']
    if post_type not in VALID_POST_TYPES:
        return render(request, '404.html')

    post = get_object_or_404(Post, id=post_id, post_type=post_type)

    # 권한 확인
    if post.post_type == 'announcement':
        if not request.user.is_superuser:
            return render(request, '403.html')
    else:
        if post.author != request.user:
            return render(request, '403.html')

    if request.method == 'POST':
        post.delete()
        return redirect(reverse(f'{post_type}_list'))

    return redirect(reverse(f'{post_type}_detail', args=[post.id]))
