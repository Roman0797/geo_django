from django.urls import path, include
from rest_framework import routers
from .views import PointViewSet, PolygonViewSet, LineStringViewSet, UploadGpxView
    # GPXUploadView

app_name = "markers"

router = routers.DefaultRouter()
router.register(r'points', PointViewSet)
router.register(r'polygons', PolygonViewSet)
router.register(r'lines', LineStringViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('gpx/', GPXUploadView.as_view()),
    path('upload_gpx/', UploadGpxView.as_view())
]