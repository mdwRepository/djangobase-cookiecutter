# -*- coding: UTF-8 -*-

import traceback

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

#  pre-populate database with initial data from the following files (no full data migration)
file_list = ["sites.json", ]
fixtures_path = str(settings.BASE_DIR) + "/webpage/fixtures/"


class Command(BaseCommand):
    help = "Create initial django site."
    args = "n/a"

    def handle(self, *args, **options):
        try:
            # find fixtures files, run call command in list comprehension
            for f in file_list:
                call_command("loaddata", fixtures_path + f, verbosity=0)
        except Exception as error:
            self.stdout.write(f"Error: {error}, {traceback.format_exc()}")
