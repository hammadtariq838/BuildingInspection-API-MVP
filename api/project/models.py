from django.db import models
from api.auth.models import User
from api.action.models import Action

class ProjectTemplate(models.Model):
  name = models.CharField(max_length=255)
  actions = models.ManyToManyField(Action, related_name='project_templates')
  interlinked_assets = models.BooleanField(default=False)
  form_file_fields = models.JSONField(null=True, blank=True, help_text='Form file fields', 
                                 default= [
                                   {
                                      'name': 'files',
                                      'valid_types': ['image', 'video'],
                                      'max_files': 1000000,
                                      'isParent': None,
                                   }
                                 ])
  # file_types = models.JSONField(null=True, blank=True, help_text='Allowed file types', default={'images': ['image/jpeg', 'image/png'], 'videos': ['video/mp4']})
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

class Project(models.Model):
  user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='projects')
  name = models.CharField(max_length=255)
  template = models.ForeignKey(
    ProjectTemplate, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
  

# class ProjectAction(models.Model):
#   project = models.ForeignKey(
#     Project, on_delete=models.CASCADE, related_name='actions')
#   action = models.ForeignKey(
#     Action, on_delete=models.CASCADE, related_name='projects')
#   updated_at = models.DateTimeField(auto_now=True)
#   created_at = models.DateTimeField(auto_now_add=True)

#   def __str__(self):
#     return f'{self.project.name} - {self.action.name}'
  
#   class Meta:
#     unique_together = ('project', 'action')
