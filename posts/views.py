from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse

from .models import Post, Comment, Participation
from notifications.models import Notification

VALID_POST_TYPES = ['donation', 'request', 'story', 'announcement']

# 게시판 목록 (공통)
def post_list(request, post_type):
    if post_type not in VALID_POST_TYPES:
        return render(request, '404.html')

    query = request.GET.get('q', '')  # 검색어 파라미터 (없으면 빈 문자열)
    posts = Post.objects.filter(post_type=post_type)

    if query:
        posts = posts.filter(title__icontains=query)  # 제목에 검색어 포함된 게시글만 필터

    if post_type == 'announcement':
        posts = posts.order_by('-is_fixed', '-created_at')
        popular_posts = Post.objects.filter(post_type='announcement', is_fixed=True).order_by('-created_at')[:5]
    else:
        posts = posts.order_by('-created_at')
        popular_posts = Post.objects.filter(post_type=post_type, views__gt=0).order_by('-views')[:5]

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/post_list.html', {
        'page_obj': page_obj,
        'popular_posts': popular_posts,
        'post_type': post_type,
        'query': query,  # 템플릿에서 입력값 유지
    })

# 게시글 상세 (공통)
def post_detail(request, post_type, post_id):
    if post_type not in VALID_POST_TYPES:
        return render(request, '404.html')

    post = get_object_or_404(Post, pk=post_id, post_type=post_type)

    session_key = f'viewed_post_{post_id}'
    if not request.session.get(session_key, False):
        post.views += 1
        post.save()
        request.session[session_key] = True

    user = request.user
    participated = False
    participation_complete = False
    is_author = False
    has_participants = False
    can_start_activity = False

    if user.is_authenticated:
        is_author = user == post.author
        participation_qs = post.participations.filter(user=user)
        participated = participation_qs.exists()

        if participated:
            participation = participation_qs.first()
            participation_complete = participation.is_completed

        has_participants = post.participations.exists()
        can_start_activity = (not post.activity_started) and has_participants and is_author

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'post_type': post_type,
        'participated': participated,
        'participation_complete': participation_complete,
        'is_author': is_author,
        'has_participants': has_participants,
        'can_start_activity': can_start_activity,
    })



# 게시글 작성
@login_required
def post_create(request, post_type):
    if post_type not in VALID_POST_TYPES:
        return render(request, '404.html')

    if not request.user.is_authenticated:
        messages.warning(request, "로그인이 필요한 기능입니다.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if post_type == 'announcement' and not (getattr(request.user, 'isAdmin', False) or request.user.is_superuser):
        return render(request, '403.html')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category') if post_type in ['donation', 'request'] else None
        address = request.POST.get('address')

        Post.objects.create(
            title=title,
            content=content,
            post_type=post_type,
            category=category,
            author=request.user,
            image=request.FILES.get('image'),
            address=address,
            is_fixed=bool(request.POST.get('is_fixed')),
        )
        return redirect(reverse('post_list', args=[post_type]))

    return render(request, 'posts/post_form.html', {'post_type': post_type})

# 게시글 수정
@login_required
def post_update(request, post_type, post_id):
    if post_type not in VALID_POST_TYPES:
        return render(request, '404.html')

    post = get_object_or_404(Post, id=post_id, post_type=post_type)

    if post.post_type == 'announcement':
        if not (getattr(request.user, 'isAdmin', False) or request.user.is_superuser):
            return render(request, '403.html')
    else:
        if post.author != request.user and not request.user.is_superuser:
            return render(request, '403.html')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.address = request.POST.get('address')

        if post_type in ['donation', 'request']:
            post.category = request.POST.get('category')

        if request.POST.get('delete_image'):
            post.image.delete(save=False)
            post.image = None

        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        if post_type == 'announcement':
            post.is_fixed = bool(request.POST.get('is_fixed'))
        post.save()
        return redirect(reverse('post_detail', args=[post_type, post.id]))

    return render(request, 'posts/post_form.html', {
        'post': post,
        'mode': 'update',
        'post_type': post_type,
    })

# 게시글 삭제
@login_required
def post_delete(request, post_type, post_id):
    if post_type not in VALID_POST_TYPES:
        return render(request, '404.html')

    post = get_object_or_404(Post, id=post_id, post_type=post_type)

    if post.post_type == 'announcement':
        if not (getattr(request.user, 'isAdmin', False) or request.user.is_superuser):
            return render(request, '403.html')
    else:
        if post.author != request.user:
            return render(request, '403.html')

    if request.method == 'POST':
        post.delete()
        return redirect(reverse('post_list', args=[post_type]))

    return redirect(reverse('post_detail', args=[post_type, post.id]))

# 댓글 작성
@login_required
def add_comment(request, post_type, post_id):
    post = get_object_or_404(Post, id=post_id, post_type=post_type)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)

    return redirect(reverse('post_detail', args=[post_type, post.id]))

# 댓글 삭제
@login_required
def delete_comment(request, post_type, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post__id=post_id, post__post_type=post_type)

    if request.user != comment.author:
        return render(request, '403.html')

    if request.method == 'POST':
        comment.delete()

    return redirect(reverse('post_detail', args=[post_type, post_id]))


@login_required
def participate(request, post_id):
    post = get_object_or_404(Post, id=post_id, post_type='donation')
    Participation.objects.get_or_create(post=post, user=request.user)
    Notification.objects.create(
        user=post.author,
        message=f'{request.user.nickname}님이 참여했습니다.',
        url=reverse('post_detail', args=['donation', post.id])
    )
    return redirect(reverse('post_detail', args=['donation', post.id]))


@login_required
def start_activity(request, post_id):
    post = get_object_or_404(Post, id=post_id, post_type='donation', author=request.user)
    post.activity_started = True
    post.save()
    for p in post.participations.all():
        Notification.objects.create(
            user=p.user,
            message=f'{post.author.nickname}님이 활동을 시작했습니다.',
            url=reverse('post_detail', args=['donation', post.id])
        )
    return redirect(reverse('post_detail', args=['donation', post.id]))


@login_required
def complete_participation(request, post_id):
    post = get_object_or_404(Post, id=post_id, post_type='donation')
    part = get_object_or_404(Participation, post=post, user=request.user)
    if request.method == 'POST':
        # 여러 항목 점수 받아오기
        r1 = int(request.POST.get('rating_kindness', 0))
        r2 = int(request.POST.get('rating_punctuality', 0))
        r3 = int(request.POST.get('rating_satisfaction', 0))
        r4 = int(request.POST.get('rating_professionalism', 0))

        rating = r1 + r2 + r3 + r4  # 총합

        part.rating = rating
        part.is_completed = True
        part.save()

        post.author.exp += rating
        post.author.save()

        Notification.objects.create(
            user=post.author,
            message=f'{request.user.nickname}님이 참여를 완료했습니다. EXP {rating}점이 적립되었습니다.',
            url=reverse('post_detail', args=['donation', post.id])
        )
        return redirect(reverse('post_detail', args=['donation', post.id]))
    return render(request, 'posts/complete_modal.html', {'post': post})
