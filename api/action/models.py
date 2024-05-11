from django.db import models

class Action(models.Model):
  name = models.CharField(max_length=255)
  function = models.CharField(max_length=255)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
  