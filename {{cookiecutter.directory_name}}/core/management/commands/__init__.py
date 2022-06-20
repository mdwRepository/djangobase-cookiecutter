# -*- coding: UTF-8 -*-

import os
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Backup PostgreSQL database.'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--database', dest='conf_db')
        parser.add_argument('--outfile', dest='out')
        parser.add_argument('--backupdir', dest='dir')

    def handle(self, *args, **options):

        try:
            if not options["out"]:
                outfile = 'backup_%s.dump' % time.strftime('%y%m%d%S')
            else:
                outfile = options["out"]
            if not options["dir"]:
                backup_dir = (str(settings.BASE_DIR) + '/backups'),
            else:
                backup_dir = options["dir"]
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            backupfile = os.path.join(backup_dir, outfile)
            if not options["conf_db"]:
                options["conf_db"] = 'default'
                print('No database config provided. Using default config.')
            db_settings = settings.DATABASES[options["conf_db"]]
            if db_settings["ENGINE"] != 'django.db.backends.postgresql_psycopg2':
                print(f"Other database engine configured: %s", db_settings["ENGINE"])
                print('Change engine to PostgreSQL...')
                sys.exit(1)
            else:
                print('Postgresql backup of database %s into %s' % (db_settings["NAME"], backupfile))
                pg_password = "PGPASSWORD='" + db_settings["PASSWORD"] + "'"
                args = [pg_password]
                args += ['pg_dump', '-Fc']
                args += ["-O", db_settings["USER"]]
                args += ["-h", db_settings["HOST"]]
                args += ["-p", db_settings["PORT"]]
                args += [db_settings["NAME"]]
                args += [">", backupfile]
                print('%s' % (' '.join(args)))
                #  check_call should raise an error if the command doesn't exit cleanly
                subprocess.check_call(args)
                #subprocess.call([(' '.join(args))], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True,
                #                shell=True)
        except Exception as error:
            self.stdout.write(f"Error: {error}, {traceback.format_exc()}")
