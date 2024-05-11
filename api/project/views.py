from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer
from .models import Project, ProjectAction
from api.response import ErrorResponse, Response
from api.project.response import ProjectResponse, ProjectListResponse
from api.action.models import Action

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
      
      project = Project(user=user, name=name)
      project.save()
      for action_id in actions:
        action = Action.objects.get(id=action_id)
        project_action = ProjectAction(project=project, action=action)
        project_action.save()

      serialized_project = ProjectSerializer().to_representation(project)

      return ProjectResponse(True, 'Project created successfully', serialized_project, status=status.HTTP_201_CREATED)
    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  def list(self, request):
    try:
      user = request.user
      projects = Project.objects.filter(user=user)
      serialized_projects = ProjectSerializer(projects, many=True).data

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
        # return forbidden by default
        return ErrorResponse('Project does not belong to you', status=status.HTTP_403_FORBIDDEN)

      serialized_project = ProjectSerializer(project).data
      return ProjectResponse(True, 'Project retrieved successfully', serialized_project, status=status.HTTP_200_OK)
    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

  def update(self, request, pk=None):
    return ErrorResponse('You can not update the project once it has been created', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
  def destroy(self, request, pk=None):
    try:
      user = request.user
      try:
        project = Project.objects.get(id=pk)
      except Project.DoesNotExist:
        return ErrorResponse('Project not found', status=status.HTTP_404_NOT_FOUND)
      
      if project.user != user:
        return ErrorResponse('Project does not belong to you', status=status.HTTP_403_FORBIDDEN)
      
      project.delete()
      return Response(True, 'Project deleted successfully', None, status=status.HTTP_200_OK)
    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
