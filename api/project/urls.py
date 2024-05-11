from django.urls import path, include
from .views import ProjectViewSet

# base url: /api/project/
urlpatterns = [
  path('', ProjectViewSet.as_view({
    'get': 'list', 
    'post': 'create' 
  })),
  path('<int:pk>/', ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
  })),
  path('<int:project_id>/asset/', include('api.project.asset.urls')),
  # path('<int:project_id>/asset/'),
]