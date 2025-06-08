# posts/models.py
from django.db import models
from django.conf import settings

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('donation', '재능 기부'),
        ('request', '재능 요청'),
        ('story', '따뜻한 이야기'),
        ('announcement', '공지사항'),
    ]

    CATEGORY_CHOICES = [
        ('education', '교육'),
        ('it', 'IT/개발'),
        ('design', '디자인'),
        ('etc', '기타'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    # 사용자가 선택한 위치 정보 (시/동 단위)
    address = models.CharField(max_length=100, blank=True, null=True)

    # 공지사항에서 상단 고정 여부
    is_fixed = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.get_post_type_display()}] {self.title}"

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.nickname} on {self.post.title}"
