from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r"pets", views.PetsViewSet)

urlpatterns = [
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
