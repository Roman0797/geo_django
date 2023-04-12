from rest_framework import serializers
from .models import Polygon, LineString, Point
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'


class PolygonSerializer(serializers.ModelSerializer):
    points = serializers.StringRelatedField(many=True)

    class Meta:
        model = Polygon
        fields = '__all__'


class LineStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineString
        fields = '__all__'


