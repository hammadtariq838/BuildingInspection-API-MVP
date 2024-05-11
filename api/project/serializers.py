from rest_framework import serializers
from .models import Project, ProjectAction
from api.action.serializers import ActionSerializer

class ProjectSerializer(serializers.ModelSerializer):

  def to_representation(self, instance):
    data = super().to_representation(instance)
    # retrieve all the related actions
    actions = ProjectAction.objects.filter(project=instance)
    serialized_actions = []
    for project_action in actions:
      action = project_action.action
      serialized_actions.append(ActionSerializer().to_representation(action))
    data['actions'] = serialized_actions
    return data


  class Meta:
    model = Project
    fields = ['id', 'name', 'actions']
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
