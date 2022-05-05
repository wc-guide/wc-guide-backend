from django.http import Http404, JsonResponse
from django.views import View
from rest_framework import permissions, viewsets
from rest_framework.request import clone_request
from rest_framework_gis.filters import InBBoxFilter
import overpass
import requests

from guide.wc.models import Toilet, Area, OtherArea, Other
from guide.wc.pagination import LargeResultsSetPagination, StandardResultsSetPagination
from guide.wc.serializers import ToiletSerializer, AreaSerializer, OtherAreaSerializer, OtherSerializer
from guide.wc.utils import transform_geojson


class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

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


class OtherAreaViewSet(AreaViewSet):
    serializer_class = OtherAreaSerializer
    queryset = OtherArea.objects.all()


class ToiletViewSet(viewsets.ModelViewSet):
    serializer_class = ToiletSerializer
    queryset = Toilet.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    bbox_filter_field = 'geometry'
    pagination_class = LargeResultsSetPagination
    filter_backends = (InBBoxFilter,)


class OtherViewSet(ToiletViewSet):
    serializer_class = OtherSerializer
    queryset = Other.objects.all()


class IpApi(View):
    def get(self, request, *args, **kwargs):
        ip = get_client_ip(request)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        return JsonResponse(response.json())


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class Overpass(View):
    def get(self, request, *args, **kwargs):
        if 'in_bbox' in request.GET:
            in_bbox = request.GET['in_bbox']
            bbox = in_bbox.split(",")
            if len(bbox) != 4:
                raise Http404('Missing valid bounding box')
            query = query_builder(bbox)
            # api = overpass.API(endpoint='https://overpass.kumi.systems/api/interpreter', timeout=600)
            api = overpass.API(endpoint='https://lz4.overpass-api.de/api/interpreter', timeout=600)
            response = api.get(query, responseformat="geojson")
            transformed_response = transform_geojson(response)
            return JsonResponse(transformed_response)
        else:
            raise Http404('Missing required parameters')


def query_builder(bbox):
    south, west, north, east = bbox[1], bbox[0], bbox[3], bbox[2]
    return f'(node["amenity"="toilets"]({south},{west},{north},{east});<;>;);'
