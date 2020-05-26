from django.urls import path

from . import views
from django.urls import include, path
from rest_framework import routers
from programs import views

router = routers.DefaultRouter()
router.register(r"programs", views.ProgramViewSet)
router.register(r"sections", views.SectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
