# your_app/management/commands/seed_db.py
import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Seed the database with data from an SQL file'

    def handle(self, *args, **kwargs):
        # Get the current directory where this file (seed_db.py) is located
        seed_file = os.path.join(os.path.dirname(__file__), 'seed.sql')

        with open(seed_file, 'r') as file:
            sql = file.read()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
