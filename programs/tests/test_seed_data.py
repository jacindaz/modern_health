import pytest
import programs.management.commands.seed_data as seed
from programs.models import Activity,ActivityType,Option,Program,Section


@pytest.mark.django_db
def test_create_options():
    option_names = ["option 2", "option 1"]
    seed.create_options(option_names)

    options = Option.objects.all()
    saved_option_names = sorted([opt.name for opt in options])
    assert saved_option_names == sorted(option_names)


@pytest.mark.django_db
def test_create_activities():
    activities_data = [
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
    ]
    seed.create_activities(activities_data, [])

    activities = Activity.objects.all()
    saved_activities_types = [activity.activity_type for activity in activities]
    assert len(saved_activities_types) == 2
    assert ActivityType.HTML.value in saved_activities_types
    assert ActivityType.MULT_CHOICE.value in saved_activities_types


@pytest.mark.django_db
def test_create_sections():
    section_data = {
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
    }
    seed.create_sections(section_data, [])

    saved_sections = Section.objects.all()
    assert len(saved_sections) == 3
    assert sorted([s.description for s in saved_sections]) == sorted(section_data.keys())


@pytest.mark.django_db
def test_create_program():
    program_data = {
        "name": "Core Pillars",
        "description": "core pillars description",
    }
    seed.create_program(program_data, [])

    saved_program = Program.objects.all()
    assert len(saved_program) == 1
    assert saved_program[0].name == "Core Pillars"


@pytest.mark.django_db
def test_clear_data():
    Program(name="test 1", description="desc").save()
    Program(name="test 2", description="desc").save()
    assert Program.objects.count() == 2

    seed.clear_data()

    assert Program.objects.count() == 0


@pytest.mark.django_db
def test_create_program_and_associated_objects():
    seed.clear_data()
    seed.create_program_and_associated_objects(seed.PROGRAMS)

    programs = Program.objects.all()
    assert len(programs) == len(seed.PROGRAMS.keys())

    for program in programs:
        program_data = seed.PROGRAMS[program.name]

        section_descriptions = sorted(list(program_data["sections"].keys()))
        assert section_descriptions == sorted([section.description for section in program.sections.all()])
