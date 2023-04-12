from django.contrib.gis.db import models


class Polygon(models.Model):
    name = models.CharField(max_length=255)
    geometry = models.PolygonField()


class LineString(models.Model):
    name = models.CharField(max_length=255)
    geometry = models.LineStringField()


class Point(models.Model):
    name = models.CharField(max_length=255)
    geometry = models.PointField()
    polygons = models.ManyToManyField(Polygon, related_name='points', blank=True)