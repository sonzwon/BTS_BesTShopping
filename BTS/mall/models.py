from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, mobile, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a name')
        if not mobile:
            raise ValueError('Users must have a mobile phone number')

        user = self.model(
            email=self.normalize_email(email),
            username=self.model.normalize_username(username),
            mobile=mobile,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, mobile, password):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
            mobile=mobile,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='user name',
        max_length=30
        )
    mobile = models.CharField(
        verbose_name='mobile phone number',
        max_length=11,
        unique=True
    )
    is_active = models.BooleanField(
        verbose_name='is active',
        default=True
        )
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
    )

    objects = MyUserManager()

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile']
    

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    @property
    def is_staff(self):
        return self.is_superuser















# class Product(models.Model):
#     name = models.CharField(max_length=30)
#     price = models.IntegerField()
#     stock = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)



# class UserDetail(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=20) #이름
#     phone_num = models.CharField(max_length=11) #핸드폰번호
#     address = models.CharField(max_length=30, null=True)   #주소
#     post_num = models.CharField(max_length=5, null=True)   #우편번호
#     agree_policy = models.BooleanField(default=False)      #약관동의(필수)
#     older_than_14 = models.BooleanField(default=False)     #14세이상(필수)
#     agree_marketing = models.BooleanField(default=False, null=True)   #마케팅수신동의(선택)