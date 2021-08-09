from django.http import Http404, JsonResponse
from django.views import View
from rest_framework import permissions, viewsets
from rest_framework.request import clone_request
from rest_framework_gis.filters import InBBoxFilter
import overpass

from guide.wc.models import Toilet, Area
from guide.wc.serializers import ToiletSerializer, AreaSerializer
from guide.wc.utils import transform_geojson


class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk is not None:
            request.data.update({'name': pk})
        instance = self.get_object_or_none()
        if instance is None:
            return super().create(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                raise


class ToiletViewSet(viewsets.ModelViewSet):
    serializer_class = ToiletSerializer
    queryset = Toilet.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    bbox_filter_field = 'geometry'
    filter_backends = (InBBoxFilter,)


class Overpass(View):

    def get(self, request, *args, **kwargs):
        if 'in_bbox' in request.GET:
            in_bbox = request.GET['in_bbox']
            bbox = in_bbox.split(",")
            if len(bbox) != 4:
                raise Http404('Missing valid bounding box')
            query = query_builder(bbox)
            api = overpass.API()
            response = api.get(query, responseformat="geojson")
            transformed_response = transform_geojson(response)
            print('transformed_response', transformed_response)
            return JsonResponse(transformed_response)
        else:
            raise Http404('Missing required parameters')


def query_builder(bbox):
    south, west, north, east = bbox[1], bbox[0], bbox[3], bbox[2]
    return f'(node["amenity"="toilets"]({south},{west},{north},{east});<;>;);'
