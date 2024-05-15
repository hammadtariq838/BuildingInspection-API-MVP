from rest_framework import serializers
from .models import Project, ProjectTemplate
from api.action.serializers import ActionSerializer
from api.project.asset.models import Asset
from api.project.asset.serializers import AssetSerializer

class ProjectTemplateSerializer(serializers.ModelSerializer):

  def to_representation(self, instance):
    data = super().to_representation(instance)
    # retrieve all the related actions
    actions = ActionSerializer(instance.actions.all(), many=True).data
    data['actions'] = actions
    return data

  class Meta:
    model = ProjectTemplate
    fields = '__all__'
    extra_kwargs = {"actions": {"read_only": True}}


class ProjectSerializer(serializers.ModelSerializer):

  def to_representation(self, instance):
    data = super().to_representation(instance)
    # retrieve all the related actions
    project_template = ProjectTemplateSerializer(instance.template).data
    data['template'] = project_template
    data['assets'] = AssetSerializer(instance.assets.all(), many=True).data
    
    return data


  class Meta:
    model = Project
    fields = ['id', 'name']
    extra_kwargs = {"user": {"read_only": True}}

  def create(self, user, name):
    print('user id', user.id)
    project = Project.objects.create(user=user, name=name)
    return project
  

  
# class ProjectActionSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = ProjectAction
#     fields = '__all__'
#     extra_kwargs = {"project": {"read_only": True}, "action": {"read_only": True}}
