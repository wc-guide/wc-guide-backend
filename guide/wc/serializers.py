from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from guide.wc.models import Toilet, Area


class ToiletSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Toilet
        geo_field = 'geometry'
        fields = ['geometry', 'properties']

    def get_properties(self, instance, fields):
        if type(instance) == Toilet:
            return instance.properties
        else:
            return instance.get('properties')

    def unformat_geojson(self, feature):
        attrs = {
            self.Meta.geo_field: feature["geometry"],
            "properties": feature["properties"]
        }
        return attrs


class AreaSerializer(serializers.ModelSerializer):
    features = ToiletSerializer(many=True, required=False)  # Attention: ToiletSerializer has to names as features!

    class Meta:
        model = Area
        fields = ['name', 'features', 'toilets']
        depth = 3

    def create(self, validated_data):
        features_data = validated_data.pop('features')
        area = Area.objects.create(**validated_data)
        for feature_data in features_data:
            Toilet.objects.create(area=area, **feature_data)
        return area

    def update(self, instance, validated_data):
        instance.delete()
        return self.create(validated_data)
