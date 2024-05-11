from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer
from .models import Project, ProjectAction
from api.response import ErrorResponse
from api.project.response import ProjectResponse, ProjectListResponse
from api.action.models import Action
from api.action.serializers import ActionSerializer

class ProjectViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticated]

  def create(self, request):
    try:
      user = request.user
      name = request.data['name']
      # name is a non empty string
      if not name or not name.strip():
        return ErrorResponse('Name is required', status=status.HTTP_400_BAD_REQUEST)
      
      actions = request.data.get('actions')
      if not actions or not isinstance(actions, list) or len(actions) == 0:
        return ErrorResponse('1 or more actions are required', status=status.HTTP_400_BAD_REQUEST)
      for action_id in actions:
        action = Action.objects.filter(id=action_id).first()
        if not action:
          return ErrorResponse(f'Action with id {action_id} not found', status=status.HTTP_404_NOT_FOUND)
      
      project = ProjectSerializer().create(user, name)
      serialized_project = ProjectSerializer().to_representation(project)
      
      serialized_actions = []
      for action_id in actions:
        action = Action.objects.get(id=action_id)
        ProjectAction.objects.create(project=project, action=action)
        serialized_actions.append(ActionSerializer().to_representation(action))
      serialized_project['actions'] = serialized_actions

      return ProjectResponse(True, 'Project created successfully', serialized_project, status=status.HTTP_201_CREATED)
    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  def list(self, request):
    try:
      user = request.user

      projects = Project.objects.filter(user=user)
      serialized_projects = []
      for project in projects:
        serialized_project = ProjectSerializer().to_representation(project)
        actions = ProjectAction.objects.filter(project=project)
        serialized_actions = []
        for project_action in actions:
          action = project_action.action
          serialized_actions.append(ActionSerializer().to_representation(action))
        serialized_project['actions'] = serialized_actions
        serialized_projects.append(serialized_project)
      return ProjectListResponse(True, 'Projects retrieved successfully', serialized_projects, status=status.HTTP_200_OK)
    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  def retrieve(self, request, pk=None):
    try:
      user = request.user
      try:
        project = Project.objects.get(id=pk)
      except Project.DoesNotExist:
        return ErrorResponse('Project not found', status=status.HTTP_404_NOT_FOUND)
      
      if project.user != user:
        return ErrorResponse('Project not found', status=status.HTTP_404_NOT_FOUND)


      serialized_project = ProjectSerializer().to_representation(project)
      actions = ProjectAction.objects.filter(project=project)
      serialized_actions = []
      for project_action in actions:
        action = project_action.action
        serialized_actions.append(ActionSerializer().to_representation(action))
      serialized_project['actions'] = serialized_actions
      return ProjectResponse(True, 'Project retrieved successfully', serialized_project, status=status.HTTP_200_OK)
    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
