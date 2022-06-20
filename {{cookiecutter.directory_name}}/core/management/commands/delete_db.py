# -*- coding: UTF-8 -*-

import subprocess
import traceback

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'drop PostgreSQL database'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--host', dest='db_host')
        parser.add_argument('--database', dest='db_db')
        parser.add_argument('--port', dest='db_port')
        parser.add_argument('--user', dest='db_user')
        parser.add_argument('--password', dest='db_pw')

    def handle(self, *args, **options):
        try:
            pg_password = "PGPASSWORD='" + options["db_pw"] + "'"
            args = [pg_password]
            args += ["dropdb"]
            args += ["-U", options["db_user"]]
            args += ["-h", options["db_host"]]
            args += ["-p", options["db_port"]]
            args.append(options["db_db"])
            print('Dropping database...')
            print('%s' % (' '.join(args)))
            subprocess.check_call(args)
        except Exception as error:
            self.stdout.write(f"Error: {error}, {traceback.format_exc()}")
