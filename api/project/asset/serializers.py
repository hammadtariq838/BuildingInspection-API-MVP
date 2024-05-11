from rest_framework import serializers
from api.project.asset.models import Asset, AssetResult
from api.action.serializers import ActionSerializer

class AssetSerializer(serializers.ModelSerializer):

  def to_representation(self, instance):
    data = super().to_representation(instance)
    results = instance.results.all()
    data['project_name'] = instance.project.name
    data['results'] = AssetResultSerializer(results, many=True).data
    return data

  class Meta:
    model = Asset
    fields = ['id', 'asset_type', 'name', 'file']
    extra_kwargs = {"project": {"read_only": True}}

class AssetResultSerializer(serializers.ModelSerializer):

  def to_representation(self, instance):
    data = super().to_representation(instance)
    data['action'] = ActionSerializer(instance.action).data
    return data

  class Meta:
    model = AssetResult
    fields = ['id', 'result', 'status', 'error']
    extra_kwargs = {"asset": {"read_only": True}}
