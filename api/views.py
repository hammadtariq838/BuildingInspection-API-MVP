from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from .serializers import UserSerializer, ProjectSerializer, AssetSerializer, ResultSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Project, Asset, Result
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .tasks import process_image_with_otsu
from rest_framework.decorators import api_view, permission_classes
from django.core.files.base import ContentFile


class ProjectAssetsWithResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            # Ensure the project belongs to the logged-in user
            project = Project.objects.get(
                id=project_id, project_owner=request.user)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found or does not belong to you'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch assets with prefetched related results
        assets = Asset.objects.filter(
            project=project).prefetch_related('results')
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_project_assets(request, project_id):
    try:
        project = Project.objects.get(
            id=project_id, project_owner=request.user)
    except Project.DoesNotExist:
        return Response({'message': 'Project not found or does not belong to you'}, status=status.HTTP_404_NOT_FOUND)

    assets = Asset.objects.filter(project=project)
    for asset in assets:
        processed_image = process_image_with_otsu(asset.asset_image.path)
        # Save the processed image as a new Result
        Result.objects.create(asset=asset, result_image=ContentFile(
            processed_image.read(), name='processed.jpg'))

    # return the processed results
    results = Result.objects.filter(asset__project=project)
    serializer = ResultSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class BulkAssetUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(
                id=project_id, project_owner=request.user)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found or does not belong to you'}, status=status.HTTP_404_NOT_FOUND)

        print('request.FILES:', request.FILES)
        files = request.FILES.getlist('asset_images')
        assets = []

        for file in files:
            asset = Asset(project=project, asset_image=file)
            asset.save()
            assets.append(asset)

        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(project_owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(project_owner=self.request.user)


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return Asset.objects.filter(project=project_id)
        return Asset.objects.filter(project__project_owner=self.request.user)

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        if not project_id:
            return Response({'message': 'Project ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            project = Project.objects.get(
                id=project_id, project_owner=self.request.user)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found or does not belong to you'}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(project=project)


class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        asset_id = self.request.query_params.get('asset')
        if asset_id:
            return Result.objects.filter(asset=asset_id, asset__project__project_owner=self.request.user)
        return Result.objects.filter(asset__project__project_owner=self.request.user)

    def perform_create(self, serializer):
        asset_id = self.request.data.get('asset')
        if not asset_id:
            return Response({'message': 'Asset ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            asset = Asset.objects.get(
                id=asset_id, project__project_owner=self.request.user)
        except Asset.DoesNotExist:
            return Response({'message': 'Asset not found or does not belong to you'}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(asset=asset)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
