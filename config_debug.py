import os

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DOORBOT_DATABASE_URL',
    os.environ.get('DATABASE_URL')
)

if not SQLALCHEMY_DATABASE_URI:
    raise ValueError("DOORBOT_DATABASE_URL must be set")
