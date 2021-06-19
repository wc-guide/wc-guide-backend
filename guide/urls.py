from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from guide.wc import views

schema_view = get_schema_view(
    openapi.Info(
        title="WC-Guide-Backend API",
        default_version='v1',
        description="WC-Guide-Backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'area', views.AreaViewSet, basename='area')
router.register(r'toilets', views.ToiletViewSet, basename='toilets')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('overpass/', views.Overpass.as_view(), name='overpass'),
    path('swagger<format>[.json|.yaml]',
         schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
]
