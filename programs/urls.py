from django.urls import path

from . import views
from django.urls import include, path
from rest_framework_nested import routers
from programs import views

router = routers.SimpleRouter()
router.register(r"programs", views.ProgramViewSet)


programs_router = routers.NestedSimpleRouter(router, r'programs', lookup='program')
programs_router.register(r'sections', views.SectionViewSet, basename='program-sections')


urlpatterns = [
    path('', include(programs_router.urls)),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
