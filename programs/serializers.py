from programs.models import Activity,Option,Program,Section
from rest_framework import serializers


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["name", "description", "sections"]


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["description", "image_url", "order_index", "activities"]
