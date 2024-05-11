# model view set for actions 
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from api.response import ErrorResponse
from api.action.response import ActionListResponse
from .models import Action
from .serializers import ActionSerializer


class ActionViewSet(viewsets.ModelViewSet):
  permission_classes = [AllowAny]

  def list(self, request):
    actions = Action.objects.all()
    serialized_actions = ActionSerializer(actions, many=True).data
    return ActionListResponse(True, 'Actions fetched successfully', serialized_actions, status=status.HTTP_200_OK)
  
  def create(self, request):
    # error response forbidden by default
    return ErrorResponse('Method not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def update(self, request):
    # error response forbidden by default
    return ErrorResponse('Method not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def delete(self, request):
    # error response forbidden by default
    return ErrorResponse('Method not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
  