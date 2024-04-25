"""
Settings for the production server
"""
from .base import *


DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = [
    os.environ.get('VIRTUAL_HOST'),
]
