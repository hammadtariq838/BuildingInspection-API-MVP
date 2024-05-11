from django.urls import path
from .views import AssetViewSet

urlpatterns = [
  path('', AssetViewSet.as_view({'get': 'list', 'post': 'create'})),
  path('<int:pk>/', AssetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
  path('<int:pk>/result/', AssetViewSet.as_view({'get': 'results'})),
]