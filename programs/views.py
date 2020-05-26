from django.shortcuts import render
from django.http import HttpResponse

from programs.models import Activity,Option,Program,Section

from rest_framework import viewsets
from rest_framework import permissions
from programs.serializers import ProgramSerializer, SectionSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all().prefetch_related('sections')
    serializer_class = ProgramSerializer
    permission_classes = []


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = []

    def get_queryset(self):
        program_id = self.kwargs['program_pk']
        sections_for_program = Section.objects.all() \
                               .prefetch_related('programs')\
                               .filter(programs=program_id)

        return sections_for_program
