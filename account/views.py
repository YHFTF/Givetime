from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_GET

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        location = request.POST.get('location')

        if not all([email, nickname, password1, password2, location]):
            return JsonResponse({'success': False, 'message': '모든 필드를 입력해주세요.'})

        if password1 != password2:
            return JsonResponse({'success': False, 'message': '비밀번호가 일치하지 않습니다.'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': '이미 존재하는 이메일입니다.'})

        try:
            user = User.objects.create_user(
                email=email,
                password=password1,
                nickname=nickname,
                location=location
            )
            # 자동 로그인 제거 - 회원가입만 완료
            return JsonResponse({'success': True, 'message': '회원가입이 완료되었습니다!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': '회원가입 중 오류가 발생했습니다.'})

    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})

def login_view(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            email = request.POST.get('username')
            password = request.POST.get('password')

            if not email or not password:
                return JsonResponse({'success': False, 'message': '이메일과 비밀번호를 모두 입력해주세요.'})

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': '로그인에 성공했습니다!'})
            else:
                return JsonResponse({'success': False, 'message': '이메일 또는 비밀번호가 올바르지 않습니다.'})

    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})

def logout_view(request):
    logout(request)
    return JsonResponse({
        'success': True,
        'message': '👋 로그아웃 되었습니다!',
        'redirect_url': '/'
    })

@require_GET
def check_nickname(request):
    nickname = request.GET.get('nickname', '').strip()
    exists = User.objects.filter(nickname=nickname).exists()
    return JsonResponse({'exists': exists})