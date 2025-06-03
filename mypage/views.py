import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import CustomUser

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
        'is_owner': True,  # 내 페이지이므로 True
    }
    return render(request, 'mypage/mypage.html', context)

@login_required
def view_profile(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)
    context = {
        'nickname': user_obj.nickname,
        'email': user_obj.email,
        'location': user_obj.location,
        'about': user_obj.about or '소개를 작성해주세요!',
        'skills': user_obj.skills or '스킬을 입력해주세요!',
        'services': user_obj.services or '서비스를 입력해주세요!',
        'profile_image': user_obj.profile_image.url if user_obj.profile_image else None,
        'is_owner': (request.user.id == user_obj.id),
    }
    return render(request, 'mypage/mypage.html', context)

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
