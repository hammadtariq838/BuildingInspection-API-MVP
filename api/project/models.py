from django.db import models
from api.auth.models import User
from api.action.models import Action

class Project(models.Model):
  user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='projects')
  name = models.CharField(max_length=255)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
  
class ProjectAction(models.Model):
  project = models.ForeignKey(
    Project, on_delete=models.CASCADE, related_name='actions')
  action = models.ForeignKey(
    Action, on_delete=models.CASCADE, related_name='projects')
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.project.name} - {self.action.name}'
  
  class Meta:
    unique_together = ('project', 'action')
