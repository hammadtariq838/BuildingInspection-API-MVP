from django.contrib import admin
# from api.auth.models import User
from api.action.models import Action
from api.project.models import Project, ProjectTemplate
from api.project.asset.models import Asset, AssetResult, ChildAsset

# Register your models here.
admin.site.register(Action)
admin.site.register(Project)
admin.site.register(ProjectTemplate)
admin.site.register(Asset)
admin.site.register(ChildAsset)
admin.site.register(AssetResult)
# admin.site.register(User)