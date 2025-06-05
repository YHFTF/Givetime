🚀 프로젝트 실행 방법
1. 의존성 설치
bash
복사
편집
pip install -r requirements.txt
Django, channels, daphne, Pillow 등이 설치됩니다.

2. 데이터베이스 구조 동기화
bash
복사
편집
python manage.py makemigrations
python manage.py migrate
모델 변경사항을 반영해 DB 스키마를 생성합니다.

3. 장고 개발 서버 실행 (정적 파일/일반 요청)
bash
복사
편집
python manage.py runserver
기본적으로 8000번 포트에서 실행되며, 정적 파일 및 일반 페이지 요청을 처리합니다.

4. Daphne ASGI 서버 실행 (웹소켓 전용)
bash
복사
편집
daphne -p 8001 Givetime.asgi:application
실시간 채팅 등 웹소켓 기능은 daphne 서버를 통해 처리됩니다.
프론트엔드에서는 ws://localhost:8001/... 주소로 연결됩니다.