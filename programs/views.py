from django.shortcuts import render
from django.http import HttpResponse

from programs.models import Activity,Option,Program,Section

from rest_framework import viewsets
from rest_framework import permissions
from programs.serializers import ProgramSerializer, SectionSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Program.objects.all().prefetch_related('sections')
    serializer_class = ProgramSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = []


class SectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = []
