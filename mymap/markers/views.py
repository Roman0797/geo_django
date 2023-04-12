from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunc
from rest_framework.filters import SearchFilter
from .models import Polygon, LineString, Point
from .serializers import PolygonSerializer, LineStringSerializer, PointSerializer
from rest_framework.response import Response
from rest_framework import views, response, status, viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
import gpxpy

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if isinstance(serializer.data, list):
            data = [self.get_serializer(point).data for point in serializer.data]
        else:
            data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)



class PolygonViewSet(viewsets.ModelViewSet):
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        radius = self.request.query_params.get('radius', None)
        point = self.request.query_params.get('point', None)
        if radius and point:
            lon, lat = point.split(',')
            point = GeoPoint(x=float(lon), y=float(lat), srid=4326)
            queryset = queryset.annotate(distance=DistanceFunc('geometry', point)).filter(distance__lte=float(radius))
        return queryset.prefetch_related('points')

class LineStringViewSet(viewsets.ModelViewSet):
    queryset = LineString.objects.all()
    serializer_class = LineStringSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class UploadGpxView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        name = request.POST.get('name')
        geom_type = request.POST.get('geom_type')
        gpx_file = request.FILES.get('gpx')

        if geom_type not in ['Polygon', 'LineString', 'MultiPoint']:
            return Response({'error': 'Invalid geometry type'})

        gpx = gpxpy.parse(gpx_file)
        if geom_type == 'Polygon':
            polygon = Polygon.objects.create(name=name, geom=gpx.get_polygon())
            serializer = PolygonSerializer(polygon)
            return Response(serializer.data)
        elif geom_type == 'LineString':
            linestring = LineString.objects.create(name=name, geom=gpx.get_linestring())
            serializer = LineStringSerializer(linestring)
            return Response(serializer.data)
        else:
            points = []
            for i, waypoint in enumerate(gpx.waypoints):
                point_name = f'{name} {i+1}'
                point = Point.objects.create(name=point_name, geom=waypoint.to_geometry())
                points.append(point)
            serializer = PointSerializer(points, many=True)
            return Response(serializer.data)