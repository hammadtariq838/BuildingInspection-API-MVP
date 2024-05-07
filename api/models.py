from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    project_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name


class Asset(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='assets')
    asset_image = models.ImageField(
        upload_to='assets/')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asset_image.url


class Result(models.Model):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name='results')
    result_image = models.ImageField(
        upload_to='results/')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result_image.url
