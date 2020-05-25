from enum import Enum

from django.db import models
import programs.helpers.date_fields as date_fields


class Option(date_fields.DefaultDateFields):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "options"


class ActivityType(Enum):
    HTML = "html"
    MULT_CHOICE = "multiple_choice"


class Activity(date_fields.DefaultDateFields):
    activity_type = models.CharField(max_length=100, choices=[(activity, activity.value) for activity in ActivityType])
    html_snippet = models.TextField(null=True)
    question = models.TextField(null=True)
    options = models.ManyToManyField(Option, related_name="activities_options")

    class Meta:
        db_table = "activities"


class Section(date_fields.DefaultDateFields):
    description = models.TextField()
    image_url = models.TextField(null=False, blank=False)
    order_index = models.IntegerField(default=0)
    activities = models.ManyToManyField(Activity, related_name="sections_activities")

    class Meta:
        db_table = "sections"


class Program(date_fields.DefaultDateFields):
    name = models.CharField(max_length=200)
    description = models.TextField()
    sections = models.ManyToManyField(Section, related_name="programs_sections")

    class Meta:
        db_table = "programs"
