from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from markers.models import  Point, LineString, Polygon


@admin.register(Point)
class PointAdmin(OSMGeoAdmin):
    list_display = ("name", "geometry")
    list_filter = ("polygons",)


@admin.register(LineString)
class LineStringAdmin(OSMGeoAdmin):
    list_display = ("name", "geometry")


@admin.register(Polygon)
class PolygonAdmin(OSMGeoAdmin):
    list_display = ("name", "geometry")


# Register your models here.