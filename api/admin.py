from django.contrib import admin
from .models import Project, Asset, Result

# Register your models here.
admin.site.register(Project)
admin.site.register(Asset)
admin.site.register(Result)
