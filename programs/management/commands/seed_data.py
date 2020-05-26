import logging
import sqlalchemy
from sqlalchemy import create_engine

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from programs.models import Activity,ActivityType,Program,Option,Section

logging.basicConfig(level=logging.INFO)

PROGRAMS = {
    "core_pillars": {
        "program": {
            "name": "Core Pillars",
            "description": "core pillars description",
        },
        "sections": {
            "Mindfulness": {
                "image_url": "mindfulness_s3_url",
                "order_index": 0,
            },
            "Core Pillars Section I": {
                "image_url": "core_pillars_section_I_s3_url",
                "order_index": 1,
            },
            "Core Pillars Section II": {
                "image_url": "core_pillars_section_II_s3_url",
                "order_index": 2,
            },
        },
        "activities": [
            {
                "activity_type": ActivityType.HTML.value,
                "html_snippet": "<html></html>",
                "question": "",
                "options": ""
            },
            {
                "activity_type": ActivityType.MULT_CHOICE.value,
                "html_snippet": "",
                "question": "How do you want to use mindfulness to improve your work?",
                "options": []
            },
        ],
        "options": ["Increase Focus", "Improve Concentration", "Mental Clarity", "Reduce Stress", "Respond With Kindness"]
    },
    "core_pillars 2": {
        "program": {
            "name": "Core Pillars",
            "description": "core pillars description",
        },
        "sections": {
            "Mindfulness": {
                "image_url": "mindfulness_s3_url",
                "order_index": 0,
            },
            "Core Pillars Section I": {
                "image_url": "core_pillars_section_I_s3_url",
                "order_index": 1,
            },
            "Core Pillars Section II": {
                "image_url": "core_pillars_section_II_s3_url",
                "order_index": 2,
            },
        },
        "activities": [
            {
                "activity_type": ActivityType.HTML.value,
                "html_snippet": "<html></html>",
                "question": "",
                "options": ""
            },
            {
                "activity_type": ActivityType.MULT_CHOICE.value,
                "html_snippet": "",
                "question": "How do you want to use mindfulness to improve your work?",
                "options": []
            },
        ],
        "options": ["Increase Focus", "Improve Concentration", "Mental Clarity", "Reduce Stress", "Respond With Kindness"]
    }
}

class Command(BaseCommand):
    help = "add seed data for testing and development."

    def handle(self, *args, **options):
        create_program_and_associated_objects()


def clear_data():
    logging.info("Removing all seed data")
    sql = f"""
    delete from {Activity.options.through._meta.db_table};
    delete from {Option._meta.db_table};
    delete from {Section.activities.through._meta.db_table};
    delete from {Activity._meta.db_table};
    delete from {Program.sections.through._meta.db_table};
    delete from {Section._meta.db_table};
    delete from {Program._meta.db_table};
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    logging.info("All seed data deleted/rolled back.")


def create_options(option_names):
    for name in option_names:
        Option.objects.get_or_create(name=name)


def create_activities(activities_data, mult_choice_option_objects):
    for activity in activities_data:
        new_act = Activity.objects.get_or_create(
            activity_type=activity["activity_type"],
            html_snippet=activity["html_snippet"],
            question=activity["question"],
        )[0]

        if activity["activity_type"] == ActivityType.MULT_CHOICE.value:
            new_act.refresh_from_db()
            new_act.options.set(mult_choice_option_objects)
            new_act.save()

def create_sections(section_data, activity_objects):
    for section_desc, section in section_data.items():
        new_sect = Section.objects.get_or_create(
            description=section_desc,
            image_url=section["image_url"],
            order_index=section["order_index"],
        )[0]
        new_sect.activities.set(activity_objects)
        new_sect.save()

def create_program(program, section_objects):
    new_prog = Program.objects.get_or_create(
        name=program["name"],
        description=program["description"],
    )[0]
    new_prog.sections.set(section_objects)
    new_prog.save()

def create_program_and_associated_objects(all_programs=PROGRAMS):
    for program_name,program_data in all_programs.items():
        try:
            logging.info(f"Creating seed data for program {program_name}")
            options = program_data["options"]
            create_options(options)
            logging.info("Created options")

            activities = program_data["activities"]
            saved_options = Option.objects.all()
            create_activities(activities, saved_options)
            logging.info("Created activities")

            sections = program_data["sections"]
            saved_activities = Activity.objects.all()
            create_sections(sections, saved_activities)
            logging.info("Created sections")

            program = program_data["program"]
            saved_sections = Section.objects.all()
            create_program(program, saved_sections)
            logging.info("Created programs")
        except Exception as e:
            logging.warning(f"Seed data failed to save. Rolling back.\n{e}")
            clear_data()
