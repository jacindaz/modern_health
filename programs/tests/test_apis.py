from django.urls import reverse
from rest_framework import status
from django.test import TestCase, Client
from programs.models import Activity,Option,Program,Section
import pytest


@pytest.fixture
def program_objects():
    """
    In real life, I would use factory_boy and set up
    factories so that I could easily add associated
    objects, and then test that the associated objects
    show up in my APIs.

    ex: Program has_many Sections
        Section has_many Activities

    For now, I'm just using a fixture to re-use to
    create Program objects.
    """
    Program(name="program name 1", description="program description 1").save()
    Program(name="program name 2", description="program description 2").save()
    Program(name="program name 2", description="program description 2").save()


@pytest.mark.django_db
def test_get_programs(program_objects):
    url = reverse("program-list")
    client = Client()
    response = client.get(url, format="json")

    programs = Program.objects.all()
    program_names = [p.name for p in programs]

    assert len(response.data) == len(programs)
    for program in response.data:
        assert program["name"] in program_names
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_one_program(program_objects):
    program = Program.objects.first()
    url = reverse("program-detail", args=[program.id])
    client = Client()
    response = client.get(url, format="json")

    assert response.data["name"] == program.name
    assert response.status_code == status.HTTP_200_OK
