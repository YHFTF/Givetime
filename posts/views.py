from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect  # redirect도 필요
from .models import Post

# 게시판 목록
def donation_list(request):
    postlist = Post.objects.filter(post_type='donation')
    return render(request, 'posts/donation_list.html', {'postlist': postlist})

def request_list(request):
    postlist = Post.objects.filter(post_type='request')
    return render(request, 'posts/request_list.html', {'postlist': postlist})

def story_list(request):
    postlist = Post.objects.filter(post_type='story')
    return render(request, 'posts/story_list.html', {'postlist': postlist})

def announcement_list(request):
    postlist = Post.objects.filter(post_type='announcement')
    return render(request, 'posts/announcement_list.html', {'postlist': postlist})

# 게시글 상세 보기
def donation_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id, post_type='donation')
    return render(request, 'posts/donation_detail.html', {'post': post})

def request_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id, post_type='request')
    return render(request, 'posts/request_detail.html', {'post': post})

def story_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id, post_type='story')
    return render(request, 'posts/story_detail.html', {'post': post})

def announcement_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id, post_type='announcement')
    return render(request, 'posts/announcement_detail.html', {'post': post})

# 게시글 작성
@login_required
def create_post(request, post_type):
    
    VALID_POST_TYPES = ['donation', 'request', 'story', 'announcement']
    if post_type not in VALID_POST_TYPES:
        return render(request, '404.html')

    # 공지사항은 관리자만 작성 가능
    if post_type == 'announcement' and not request.user.is_superuser:
        return render(request, '403.html')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category') if post_type in ['donation', 'request'] else None

        Post.objects.create(
            title=title,
            content=content,
            post_type=post_type,
            category=category,
            author=request.user
        )

        return redirect(f'/posts/{post_type}/')

    return render(request, 'posts/post_form.html', {'post_type': post_type})