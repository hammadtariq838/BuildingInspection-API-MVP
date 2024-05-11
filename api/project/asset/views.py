import time
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import AssetSerializer, AssetResultSerializer
from .models import Asset, AssetResult
from api.project.models import Project
from api.action.models import Action
from api.project.models import ProjectAction
from api.project.serializers import ProjectSerializer
from api.response import ErrorResponse
from api.project.asset.response import AssetResponse, AssetListResponse
from api.action.tasks import concrete_crack_classification_image, concrete_crack_classification_video, crack_detection_basic_image, crack_detection_basic_video, crack_detection_yolo_v8_image, crack_detection_yolo_v8_video


IMAGE_MIME_TYPES = [
  'image/jpeg', 
  'image/jpg',
  'image/png'
]
VIDEO_MIME_TYPES = [
  'video/mp4',
  'video/mpeg',
]

SWITCHER = {
  'crack_detection_basic_image': crack_detection_basic_image,
  'crack_detection_basic_video': crack_detection_basic_video,
  'crack_detection_yolo_v8_image': crack_detection_yolo_v8_image,
  'crack_detection_yolo_v8_video': crack_detection_yolo_v8_video,
  'concrete_crack_classification_image': concrete_crack_classification_image,
  'concrete_crack_classification_video': concrete_crack_classification_video,
}

class AssetViewSet(viewsets.ModelViewSet):  
  parser_classes = [MultiPartParser, FormParser]
  permission_classes = [IsAuthenticated]

  def create(self, request, project_id=None):
    try:
      if not project_id:
        return ErrorResponse('Project ID is required', status=status.HTTP_400_BAD_REQUEST)
      project_id = int(project_id)
      try:
        project = Project.objects.get(id=project_id)
      except Project.DoesNotExist:
        return ErrorResponse(f'Project with id {project_id} not found', status=status.HTTP_404_NOT_FOUND)
      if project.user != request.user:
        return ErrorResponse('You do not have access to this project', status=status.HTTP_403_FORBIDDEN)
      
      files = request.FILES.getlist('files')
      images = []
      videos = []
      if not files or len(files) == 0:
        return ErrorResponse('Files are required', status=status.HTTP_400_BAD_REQUEST)
      for file in files:
        if file.content_type in IMAGE_MIME_TYPES:
          images.append(file)
        elif file.content_type in VIDEO_MIME_TYPES:
          videos.append(file)
        else:
          return ErrorResponse(f'Invalid file type {file.content_type}', status=status.HTTP_400_BAD_REQUEST)
        

      query = ProjectAction.objects.filter(project=project)
      actions = [action.action for action in query]

      # create assets
      assets = []
      for image in images:
        image_name = image.name
        image.name = f'{str(int(time.time()))}_{image_name}'
        asset = Asset(project=project, asset_type='image', name=image_name, file=image)
        asset.save()
        assets.append(asset)
        for action in actions:
          asset_result = AssetResult(asset=asset, action=action)
          asset_result.save()
          function = SWITCHER.get(action.function + '_' + asset.asset_type, None)
          if function:
            function.delay(asset_result.id)
          else:
            asset_result.status = 'failed'
            asset_result.error = 'Action not found'
            asset_result.save()
          
      for video in videos:
        asset = Asset(project=project, asset_type='video', name=video.name, file=video)
        asset.save()
        assets.append(asset)
        for action in actions:
          asset_result = AssetResult(asset=asset, action=action)
          asset_result.save()
          function = SWITCHER.get(action.function + '_' + asset.asset_type, None)
          if function:
            function.delay(asset_result.id)
          else:
            asset_result.status = 'failed'
            asset_result.error = 'Action not found'
            asset_result.save()

      serialized_assets = AssetSerializer(assets, many=True).data
      return AssetListResponse(True, 'Assets uploaded successfully', serialized_assets, status=status.HTTP_201_CREATED)
    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def list(self, request, project_id=None):
    return ErrorResponse('Not implemented', status=status.HTTP_501_NOT_IMPLEMENTED)

  def retrieve(self, request, project_id=None, pk=None):
    return ErrorResponse('Not implemented', status=status.HTTP_501_NOT_IMPLEMENTED)

  def update(self, request, project_id=None, pk=None):
    return ErrorResponse('Not implemented', status=status.HTTP_501_NOT_IMPLEMENTED)

  def destroy(self, request, project_id=None, pk=None):
    return ErrorResponse('Not implemented', status=status.HTTP_501_NOT_IMPLEMENTED)

  def results(self, request, project_id=None, pk=None):
    return ErrorResponse('Not implemented', status=status.HTTP_501_NOT_IMPLEMENTED)