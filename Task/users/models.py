from django.db import models
import bcrypt
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from datetime import timedelta, datetime
from django.contrib.auth.hashers import make_password
import pytz

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, cellnumber, password=None, **kwargs):
        if not cellnumber:
            raise ValueError('The Cellnumber field must be set')
        user = self.model(cellnumber=cellnumber, **kwargs)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, cellnumber, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('roleId', 1)
        return self.create_user(cellnumber, password=password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    NORMAL_USER = 2

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (NORMAL_USER, 'Normal User'),
    )
    
    profilepic = models.ImageField(upload_to='profilepics/', null=True, blank=True)
    cellnumber = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    roleId = models.IntegerField(choices=ROLE_CHOICES, default=NORMAL_USER)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = 'cellnumber'

    def __str__(self):
        return self.cellnumber + ' - ' + self.ROLE_CHOICES[self.roleId-1][1]

    @property
    def is_admin(self):
        return self.roleId == User.ADMIN
    
    @property
    def is_logged_in(self):
        access_token = AccessToken.objects.filter(user=self).last()
        if access_token is None:
            return False
        return access_token.created + timedelta(seconds=access_token.ttl) > datetime.now().replace(tzinfo=pytz.UTC)


class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    ttl = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
