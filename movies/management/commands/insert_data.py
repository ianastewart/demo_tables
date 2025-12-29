# myapp/management/commands/import_sql_data.py

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
from django.apps import apps


class Command(BaseCommand):
    help = 'Reads the SQL script insert_data.sql from the app directory and executes it on the database to insert data'

    def handle(self, *args, **kwargs):
        # Locate the app directory and the insert_data.sql file
        app_name = 'movies'
        app_config = apps.get_app_config(app_name)
        sql_script_path = os.path.join(app_config.path, 'insert_data.sql')

        # Check if the SQL script file exists
        if not os.path.exists(sql_script_path):
            self.stderr.write(f"Error: The file '{sql_script_path}' does not exist.")
            return

        # Check database connection
        try:
            connection = connections['default']
            cursor = connection.cursor()
        except OperationalError as e:
            self.stderr.write(f"Error: Could not connect to the database: {e}")
            return

        # Step 1: Read the SQL script
        with open(sql_script_path, 'r') as file:
            sql_script = file.read()

        # Step 2: Execute the SQL script
        try:
            cursor.executescript(sql_script)
            connection.commit()  # Commit the transaction
            self.stdout.write(self.style.SUCCESS(f"SQL script '{sql_script_path}' executed successfully"))
        except Exception as e:
            self.stderr.write(f"Error executing SQL script: {e}")
            return
        finally:
            # Close the cursor after executing
            cursor.close()

