import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# Use DATABASE_URL if set, else fall back to a local Postgres instance.
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres@localhost:5432/fyyur'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
