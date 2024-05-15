from typing import Any
from django.db import models
from api.project.models import Project
from api.action.models import Action

class Asset(models.Model):
  project = models.ForeignKey(
    Project, on_delete=models.CASCADE, related_name='assets')
  asset_type = models.CharField(max_length=255, default='image', choices=[
    ('image', 'Image'),
    ('video', 'Video'),
  ])
  name = models.CharField(max_length=255)
  file = models.FileField(upload_to='assets/', null=True, blank=True, default=None)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name + ' - ' + self.asset_type + ' - ' + self.project.name

class ChildAsset(models.Model):
  parent = models.ForeignKey(
    Asset, on_delete=models.CASCADE, related_name='children')
  asset_type = models.CharField(max_length=255, default='image', choices=[
    ('image', 'Image'),
    ('video', 'Video'),
  ])
  name = models.CharField(max_length=255)
  file = models.FileField(upload_to='assets/', null=True, blank=True, default=None)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name + ' - ' + self.asset_type + ' - ' + self.parent.name
  
    

class AssetResult(models.Model):

  asset = models.ForeignKey(
    Asset, on_delete=models.CASCADE, related_name='results')
  action = models.ForeignKey(
    Action, on_delete=models.CASCADE, related_name='results')
  result = models.FileField(upload_to='results/', null=True, blank=True, default=None)
  status = models.CharField(max_length=255, default='pending', choices=[
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
  ])
  error = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.asset.name + ' - ' + self.status
  
