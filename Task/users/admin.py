from django.contrib import admin
from .models import *
from rest_framework.authtoken.models import Token, TokenProxy
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cellnumber', 'email', 'roleId', 'is_superuser']


class AuthTokenAdmin(TokenAdmin):
    list_display = ['key', 'user']
    list_filter = ['user__cellnumber']


admin.site.unregister(TokenProxy)
admin.site.register(User, UserAdmin)
admin.site.register(Token, AuthTokenAdmin)