# -*- coding: UTF-8 -*-

import traceback

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

#  pre-populate database with initial data from the following files (no full data migration)
# please note: admin/admin user should definitely not used in production ;-)
file_list = ["users.json", "tous.json", ]
fixtures_path = str(settings.BASE_DIR) + "/users/fixtures/"


class Command(BaseCommand):
    help = "Create initial django terms of use."
    args = "n/a"

    def handle(self, *args, **options):
        try:
            # find fixtures files, run call command in list comprehension
            for f in file_list:
                call_command("loaddata", fixtures_path + f, verbosity=0)
        except Exception as error:
            self.stdout.write(f"Error: {error}, {traceback.format_exc()}")
