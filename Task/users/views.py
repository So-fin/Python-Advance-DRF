from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
import bcrypt
import datetime
from .permissions import Check

# Create your views here

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.action == 'list':
            return [Check()]
        return [IsAuthenticated(), IsAdmin()]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token, created = Token.objects.get_or_create(user=User.objects.last())
        if created is False:
            token.delete()
            token = Token.objects.create(user=User.objects.last())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        if request.user.roleId != User.ADMIN:
            serializer =self.serializer_class(self.queryset.filter(id=request.user.id), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']

        token = bcrypt.gensalt().decode('utf-8')

        access_token = AccessToken.objects.create(
            user=user,
            token=token,
            ttl=300000000,
            created=datetime.datetime.now()
        )
        
        return Response({
            'token': token
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)