from django.urls import path
from .views import LoginView, RefreshView, SignUpView, UserViewSet

urlpatterns = [
  path('login', LoginView.as_view(), name='login'),
  path('refresh', RefreshView.as_view(), name='refresh'),
  path('register', SignUpView.as_view(), name='register'),
  path('user', UserViewSet.as_view({'get': 'list'}), name='user'),
]