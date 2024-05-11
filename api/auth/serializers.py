from rest_framework import serializers
from .models import User
from api.project.models import Project
from api.project.serializers import ProjectSerializer

class UserSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		data = super().to_representation(instance)
		# retrieve all the related projects
		project_query = Project.objects.filter(user=instance)
		data['projects'] = [ProjectSerializer(project).data for project in project_query]
		return data
	
	
	class Meta:
		model = User
		fields = ["id", "username", "password"]
		extra_kwargs = {"password": {"write_only": True}}

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user
	