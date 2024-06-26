from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('users/login/', login, name='login'),
] + router.urls