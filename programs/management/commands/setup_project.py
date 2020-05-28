import logging
import os
import sqlalchemy
import time
from sqlalchemy import create_engine

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    help = "set up django project"

    def handle(self, *args, **options):
        """
        If I had more time, I'd build out installing brew,
        then using brew to install postgres and pyenv.

        For now, I'm assuming the user already has these tools and
        doing a more basic project setup script.
        """
        print("*********Note: this script assumes you have postgres and pyenv installed")
        print("To install postgres: https://www.postgresql.org/download/")
        print("To install pyenv: https://github.com/pyenv/pyenv#installation")

        time.sleep(5)

        os.system("pip install -r requirements.txt")
        os.system("python manage.py migrate programs")

        seed_data = input("Would you like to add seed data to your database? (y/n): ")
        if seed_data == "y":
            os.system("python manage.py seed_data")

        os.system("python manage.py runserver")
