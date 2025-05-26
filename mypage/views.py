from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def my_page(request):
    user = request.user

    context = {
        'username': user.username,
        'email': user.email,
        'location': getattr(user, 'location', '청주시'),  # User 모델에 location 필드가 없다면 기본값 제공
        'about': getattr(user, 'about', '소개를 작성해주세요!'),
        'skills': ['HTML', 'CSS', 'JavaScript'],  # 임시 데이터
        'services': ['재능 기부', '멘토링', '코드 리뷰'],  # 임시 데이터
    }

    return render(request, 'mypage/mypage.html', context)
