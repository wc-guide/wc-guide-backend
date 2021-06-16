from django.http import Http404
from rest_framework import permissions, viewsets
from rest_framework.request import clone_request
from rest_framework_gis.filters import InBBoxFilter

from guide.wc.models import Toilet, Area
from guide.wc.serializers import ToiletSerializer, AreaSerializer


class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk is not None:
            request.data.update({'name':  pk})
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
