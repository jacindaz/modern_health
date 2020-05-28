from programs.models import Activity,Option,Program,Section
from rest_framework import serializers


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "name"]


class ActivitySerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ["id", "activity_type", "html_snippet", "question", "options"]


class SectionWithActivitySerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ["id", "description", "image_url", "order_index", "activities"]


class SectionWithoutActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "description", "image_url", "order_index", "activities"]


class ProgramSerializer(serializers.ModelSerializer):
    sections = SectionWithoutActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = ["id", "name", "description", "sections"]
