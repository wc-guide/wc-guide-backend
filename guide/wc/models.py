from django.contrib.gis.db import models


class Area(models.Model):
    name = models.TextField(primary_key=True)


class Toilet(models.Model):
    properties = models.JSONField(default=None, blank=True, null=True)
    geometry = models.GeometryField(default=None, blank=True, null=True)
    area = models.ForeignKey(Area, related_name='toilets', on_delete=models.CASCADE)
