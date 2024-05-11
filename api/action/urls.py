from django.urls import path
from api.action.views import ActionViewSet

urlpatterns = [
  path('', ActionViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'delete'
  })),
]