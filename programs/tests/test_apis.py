from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# from myproject.apps.core.models import Account
from programs.models import Activity,Option,Program,Section


class ProgramTests(APITestCase):
    def test_get_programs(self):
        # Set up data
        program1 = Program(name="program name 1", description="program description 1")
        program2 = Program(name="program name 2", description="program description 2")
        program1.save()
        program2.save()

        # GET /programs
        url = reverse("program-list")
        response = self.client.get(url, format="json")

        assert len(response.data) == Program.objects.count()

        program_names = [program1.name, program2.name]
        for program in response.data:
            assert program["name"] in program_names

        assert response.status_code == status.HTTP_200_OK

    def test_get_one_program(self):
        # Set up data
        program1 = Program(name="program name 1", description="program description 1")
        program2 = Program(name="program name 2", description="program description 2")
        program3 = Program(name="program name 2", description="program description 2")

        program1.save()
        program2.save()
        program3.save()

        # GET /programs
        url = reverse("program-detail", args=[program2.id])
        response = self.client.get(url, format="json")

        assert response.data["name"] == program2.name
        assert response.status_code == status.HTTP_200_OK
