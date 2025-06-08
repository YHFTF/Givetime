from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, location=None):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        if not location:
            location = '기본 위치'  # 기본값 지정
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, location=location)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        default_location = '기본 위치'  # 슈퍼유저 생성 시 location 기본값
        user = self.create_user(email, nickname, password, location=default_location)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique = True) # 닉네임 중복 불가
    location = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    about = models.TextField(blank=True, null=True)  # 소개글
    skills = models.TextField(blank=True, null=True)  # 기술 목록
    services = models.TextField(blank=True, null=True)  # 서비스 목록

    last_message_read_time = models.DateTimeField(null=True, blank=True)

    # 관리자가 공지사항을 작성할 수 있는지 여부
    isAdmin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

    def get_skills_list(self):
        return self.skills.split(',') if self.skills else []
