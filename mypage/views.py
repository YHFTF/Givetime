import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from account.models import CustomUser

# 내 마이페이지
@login_required
def my_page(request):
    user = request.user
    context = {
        'nickname': user.nickname,
        'email': user.email,
        'location': user.location,
        'about': user.about or '소개를 작성해주세요!',
        'skills': user.skills or '스킬을 입력해주세요!',
        'services': user.services or '서비스를 입력해주세요!',
        'profile_image': user.profile_image.url if user.profile_image else None,
        'is_owner': True,
        'isAdmin': user.isAdmin,
    }
    return render(request, 'mypage/mypage.html', context)

# 검색으로 타인 프로필 보기
@login_required
def view_profile(request, nickname):
    user_obj = get_object_or_404(CustomUser, nickname=nickname)
    context = {
        'nickname': user_obj.nickname,
        'email': user_obj.email,
        'location': user_obj.location,
        'about': user_obj.about or '소개를 작성해주세요!',
        'skills': user_obj.skills or '스킬을 입력해주세요!',
        'services': user_obj.services or '서비스를 입력해주세요!',
        'profile_image': user_obj.profile_image.url if user_obj.profile_image else None,
        'is_owner': (request.user.id == user_obj.id),
        'isAdmin': user_obj.isAdmin,
    }
    return render(request, 'mypage/mypage.html', context)

# 닉네임 기반 검색 처리
@login_required
def search_user(request):
    query = request.GET.get('q')
    if query:
        try:
            user_obj = CustomUser.objects.get(nickname=query)
            return redirect('mypage:view_profile', nickname=user_obj.nickname)
        except CustomUser.DoesNotExist:
            # mypage.html에 오류 메시지를 전달
            return render(request, 'mypage/mypage.html', {
                'nickname': request.user.nickname,
                'email': request.user.email,
                'location': request.user.location,
                'about': request.user.about or '소개를 작성해주세요!',
                'skills': request.user.skills or '스킬을 입력해주세요!',
                'services': request.user.services or '서비스를 입력해주세요!',
                'profile_image': request.user.profile_image.url if request.user.profile_image else None,
                'is_owner': True,
                'error': '존재하지 않는 사용자입니다.'
            })
    return redirect('mypage:my_page')


# 내 프로필 수정 (ID 기준)
@csrf_exempt
@login_required
def update_profile(request, user_id):
    if request.method == 'POST':
        if request.user.id != user_id:
            return JsonResponse({'success': False, 'error': '권한이 없습니다.'}, status=403)

        try:
            user = request.user
            data_json = request.POST.get('data')
            if data_json:
                data = json.loads(data_json)
                user.nickname = data.get('nickname', user.nickname)
                user.location = data.get('location', user.location)
                user.about = data.get('about', user.about)
                user.skills = data.get('skills', user.skills)
                user.services = data.get('services', user.services)

            image_file = request.FILES.get('profile_image')
            if image_file:
                user.profile_image = image_file

            user.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@login_required
def register_admin(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == '0000':
            user = request.user
            user.isAdmin = True
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': '비밀번호가 올바르지 않습니다.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
