from rest_framework import serializers
from .models import Project, ProjectAction
from api.action.serializers import ActionSerializer
from api.project.asset.models import Asset
from api.project.asset.serializers import AssetSerializer

class ProjectSerializer(serializers.ModelSerializer):

  def to_representation(self, instance):
    data = super().to_representation(instance)
    # retrieve all the related actions
    action_query = ProjectAction.objects.filter(project=instance)
    data['actions'] = [ActionSerializer(action.action).data for action in action_query]
    asset_query = Asset.objects.filter(project=instance)
    data['assets'] = [AssetSerializer(asset).data for asset in asset_query]
    return data


  class Meta:
    model = Project
    fields = ['id', 'name']
    extra_kwargs = {"user": {"read_only": True}}

  def create(self, user, name):
    print('user id', user.id)
    project = Project.objects.create(user=user, name=name)
    return project
  

  
class ProjectActionSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProjectAction
    fields = '__all__'
    extra_kwargs = {"project": {"read_only": True}, "action": {"read_only": True}}
