"""Manager script for running the app and utility tasks."""

import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app


app = create_app(config_name=os.getenv('APP_SETTINGS', 'development'))
migrate = Migrate(app, db)
manager = Manager(app)

# Define the migration command to always be preceded by the word "db"
# Example usage: python manage.py db init
manager.add_command('db', MigrateCommand)

# TODO: test command

if __name__ == '__main__':
    manager.run()
