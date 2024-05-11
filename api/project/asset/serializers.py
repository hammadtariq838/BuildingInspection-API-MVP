from rest_framework import serializers
from api.project.asset.models import Asset, AssetResult

class AssetSerializer(serializers.ModelSerializer):

  def to_representation(self, instance):
    data = super().to_representation(instance)
    results = instance.results.all()
    data['results'] = AssetResultSerializer(results, many=True).data
    return data

  class Meta:
    model = Asset
    fields = '__all__'
    extra_kwargs = {"project": {"read_only": True}}

class AssetResultSerializer(serializers.ModelSerializer):
  class Meta:
    model = AssetResult
    fields = '__all__'
    extra_kwargs = {"asset": {"read_only": True}}
