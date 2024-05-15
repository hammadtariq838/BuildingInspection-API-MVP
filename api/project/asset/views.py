import time
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import AssetSerializer, AssetResultSerializer
from .models import Asset, AssetResult, ChildAsset
from api.project.models import Project
from api.action.models import Action
from api.project.models import ProjectTemplate
from api.project.serializers import ProjectSerializer
from api.response import ErrorResponse
from api.project.asset.response import AssetResponse, AssetListResponse
from api.action.tasks import concrete_crack_classification_image, concrete_crack_classification_video, crack_detection_basic_image, crack_detection_basic_video, crack_detection_yolo_v8_image, crack_detection_yolo_v8_video, before_after_image


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
  'before_after_image': before_after_image,
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
      
      # get project template
      project_template = project.template
      if not project_template:
        return ErrorResponse('Project template not found', status=status.HTTP_404_NOT_FOUND)
      
      for field in project_template.form_file_fields:
        if field['name'] not in request.FILES:
          return ErrorResponse(f'{field["name"]} is required', status=status.HTTP_400_BAD_REQUEST)
        
        for file in request.FILES.getlist(field['name']):
          # valid_types = ['image', 'video']
          file_type = 'image' if file.content_type in IMAGE_MIME_TYPES else None
          file_type = 'video' if file.content_type in VIDEO_MIME_TYPES else file_type
          if not file_type:
            return ErrorResponse(f'Invalid file type {file.content_type}', status=status.HTTP_400_BAD_REQUEST)
          
          if field['valid_types'].index(file_type) == -1:
            return ErrorResponse(f'Invalid file type {file.content_type}', status=status.HTTP_400_BAD_REQUEST)

      if project_template.interlinked_assets is False:


        for field in project_template.form_file_fields:
          for file in request.FILES.getlist(field['name']):
            file_type = 'image' if file.content_type in IMAGE_MIME_TYPES else None
            file_type = 'video' if file.content_type in VIDEO_MIME_TYPES else file_type
            file_name = file.name
            field_name = field['name']
            # attach timestamp and file type to the file name
            file.name = f'{str(int(time.time()))}_{field_name}_{file_name}'
            asset = Asset(project=project, asset_type=file_type, name=file_name, file=file)
            asset.save()
            for action in project_template.actions.all():
              asset_result = AssetResult(asset=asset, action=action)
              asset_result.save()
              function = SWITCHER.get(action.function + '_' + asset.asset_type, None)
              if function:
                function.delay(asset_result.id)
              else:
                asset_result.status = 'failed'
                asset_result.error = 'Action not found'
                asset_result.save()
            serialized_assets = AssetSerializer(asset).data
            return AssetResponse(True, 'Asset uploaded successfully', serialized_assets, status=status.HTTP_201_CREATED)
          
      else:
        # get the parent field
        parent_field = None
        for field in project_template.form_file_fields:
          if field['isParent']:
            parent_field = field
            break
        
        if not parent_field:
          return ErrorResponse('Parent field is required', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        parent_file = request.FILES.getlist(parent_field['name'])
        if len(parent_file) != 1:
          return ErrorResponse('Only 1 Parent File', status=status.HTTP_400_BAD_REQUEST)
        
        parent_file = parent_file[0]
        parent_file_type = 'image' if parent_file.content_type in IMAGE_MIME_TYPES else None
        parent_file_type = 'video' if parent_file.content_type in VIDEO_MIME_TYPES else parent_file_type
        if not parent_file_type:
          return ErrorResponse(f'Invalid file type {parent_file.content_type}', status=status.HTTP_400_BAD_REQUEST)
        
        parent_file_name = parent_file.name
        parent_field_name = parent_field['name']
        # attach timestamp and file type to the file name
        parent_file.name = f'{str(int(time.time()))}_{parent_field_name}_{parent_file_name}'
        parent_asset = Asset(project=project, asset_type=parent_file_type, name=parent_file_name, file=parent_file)
        parent_asset.save()

        # create child assets
        child_assets = []
        for field in project_template.form_file_fields:
          if field['isParent']:
            continue
          for file in request.FILES.getlist(field['name']):
            file_type = 'image' if file.content_type in IMAGE_MIME_TYPES else None
            file_type = 'video' if file.content_type in VIDEO_MIME_TYPES else file_type
            file_name = file.name
            field_name = field['name']
            # attach timestamp and file type to the file name
            file.name = f'{str(int(time.time()))}_{field_name}_{file_name}'
            child_asset = ChildAsset(parent=parent_asset, asset_type=file_type, name=file_name, file=file)
            child_asset.save()
            child_assets.append(child_asset)
        
        for action in project_template.actions.all():

          # create parent asset result
          parent_asset_result = AssetResult(asset=parent_asset, action=action)
          parent_asset_result.save()

          print('Function:', action.function + '_' + parent_asset.asset_type)
          function = SWITCHER.get(action.function + '_' + parent_asset.asset_type, None)
          if function:            
            function.delay(parent_asset_result.id)
          else:
            parent_asset_result.status = 'failed'
            parent_asset_result.error = 'Action not found'
            parent_asset_result.save()


        serialized_assets = AssetSerializer(parent_asset).data
        return AssetResponse(True, 'Assets uploaded successfully', serialized_assets, status=status.HTTP_201_CREATED)
    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    




  def list(self, request, project_id=None):
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
      
      query = Asset.objects.filter(project=project)
      serialized_assets = AssetSerializer(query, many=True).data
      return AssetListResponse(True, 'Assets retrieved successfully', serialized_assets, status=status.HTTP_200_OK)

    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # return ErrorResponse('Not implemented', status=status.HTTP_501_NOT_IMPLEMENTED)

  def retrieve(self, request, project_id=None, pk=None):
    try:
      if not project_id:
        return ErrorResponse('Project ID is required', status=status.HTTP_400_BAD_REQUEST)
      if not pk:
        return ErrorResponse('Asset ID is required', status=status.HTTP_400_BAD_REQUEST)
      project_id = int(project_id)
      pk = int(pk)
      try:
        project = Project.objects.get(id=project_id)
      except Project.DoesNotExist:
        return ErrorResponse(f'Project with id {project_id} not found', status=status.HTTP_404_NOT_FOUND)
      if project.user != request.user:
        return ErrorResponse('You do not have access to this project', status=status.HTTP_403_FORBIDDEN)

      try:
        asset = Asset.objects.get(id=pk)
      except Asset.DoesNotExist:
        return ErrorResponse(f'Asset with id {pk} not found', status=status.HTTP_404_NOT_FOUND)
      if asset.project != project:
        return ErrorResponse('Asset does not belong to this project', status=status.HTTP_403_FORBIDDEN)
      
      serialized_asset = AssetSerializer(asset).data
      return AssetResponse(True, 'Asset retrieved successfully', serialized_asset, status=status.HTTP_200_OK)

    except Exception as e:
      return ErrorResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
  def update(self, request, project_id=None, pk=None):
    return ErrorResponse('Not implemented', status=status.HTTP_501_NOT_IMPLEMENTED)

  def destroy(self, request, project_id=None, pk=None):
    return ErrorResponse('Not implemented', status=status.HTTP_501_NOT_IMPLEMENTED)

  def results(self, request, project_id=None, pk=None):
    return ErrorResponse('Not implemented', status=status.HTTP_501_NOT_IMPLEMENTED)