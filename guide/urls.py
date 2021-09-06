from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, permissions

from guide.wc import views

router = routers.DefaultRouter()
router.register(r'area', views.AreaViewSet, basename='area')
router.register(r'toilets', views.ToiletViewSet, basename='toilets')
router.register(r'otherarea', views.OtherAreaViewSet, basename='otherarea')
router.register(r'others', views.OtherViewSet, basename='others')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('overpass/', views.Overpass.as_view(), name='overpass'),
    path('ip-api/', views.IpApi.as_view(), name='ip-api'),
]
