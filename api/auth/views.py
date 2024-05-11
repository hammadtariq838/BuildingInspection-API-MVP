from rest_framework import generics, status # type: ignore
from rest_framework.response import Response 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from django import Request
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny
from .response import UserResponse, TokenResponse
from api.response import ErrorResponse
from django.http import HttpRequest
# from rest_framework.request import Request


class LoginView(TokenObtainPairView):

  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)
    
    user = User.objects.get(username=request.data['username'])
    # get user serializer
    user_serializer = UserSerializer(user)
    return UserResponse(True, 'User logged in successfully', user_serializer.data, response.data, status=status.HTTP_200_OK)
    

class RefreshView(TokenRefreshView):

  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)
    return TokenResponse(True, 'Token refreshed successfully', response.data, status=status.HTTP_200_OK)

class SignUpView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = [AllowAny]
  
  def post(self, request, *args, **kwargs):
    # get username and password from request
    try:
      username = request.data['username']
      password = request.data['password']
      # check if username and password are not empty
      if not username or not username.strip():
        return ErrorResponse('Username is required', status=status.HTTP_400_BAD_REQUEST)
      if not password or not password.strip():
        return ErrorResponse('Password is required', status=status.HTTP_400_BAD_REQUEST)
      
      if User.objects.filter(username=username).exists():
        return ErrorResponse('Username already exists', status=status.HTTP_400_BAD_REQUEST)
      

      new_user = self.create(request, *args, **kwargs)

      return UserResponse(True, 'User created successfully', new_user.data, None, status=status.HTTP_201_CREATED)
    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# model viewset
from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

  # permission_classes = [IsAuthenticated]
  
  def get_queryset(self):
    return User.objects.all()
  
  # def perform_create(self, serializer):
  #   serializer.save(user=self.request.user)
  
  # def perform_update(self, serializer):
  #   serializer.save(user=self.request.user)
  
  # def perform_destroy(self, instance):
  #   instance.delete()
  
  # def get_object(self):
  #   return self.request.user
  
  