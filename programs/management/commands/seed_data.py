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
    }
}

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_core_pillar_program()

    def create_options(self, options):
        for name in options:
            Option(name=name).save()

    def create_activities(self, activities, mult_choice_option_objects):
        for activity in activities:
            new_act = Activity(
                activity_type=activity["activity_type"],
                html_snippet=activity["html_snippet"],
                question=activity["question"],
            )
            new_act.save()

            if activity["activity_type"] == ActivityType.MULT_CHOICE.value:
                new_act.refresh_from_db()
                new_act.options.set(mult_choice_option_objects)
                new_act.save()

    def create_sections(self, sections, activity_objects):
        for section_desc, section in sections.items():
            new_sect = Section(
                description=section_desc,
                image_url=section["image_url"],
                order_index=section["order_index"],
            )
            new_sect.save()

            new_sect.activities.set(activity_objects)
            new_sect.save()

    def save_program(self, program, section_objects):
        new_prog = Program(
            name=program["name"],
            description=program["description"],
        )
        new_prog.save()
        new_prog.sections.set(section_objects)

    def create_core_pillar_program(self, ):
        program_name = "core_pillars"

        try:
            logging.info(f"Creating seed data for program {program_name}")
            options = PROGRAMS[program_name]["options"]
            self.create_options(options)
            logging.info("Created options")

            activities = PROGRAMS[program_name]["activities"]
            saved_options = Option.objects.all()
            self.create_activities(activities, saved_options)
            logging.info("Created activities")

            sections = PROGRAMS[program_name]["sections"]
            saved_activities = Activity.objects.all()
            self.create_sections(sections, saved_activities)
            logging.info("Created sections")

            program = PROGRAMS[program_name]["program"]
            saved_sections = Section.objects.all()
            self.save_program(program, saved_sections)
            logging.info("Created programs")
        except Exception as e:
            logging.warning(f"Seed data failed to save. Rolling back.\n{e}")
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
