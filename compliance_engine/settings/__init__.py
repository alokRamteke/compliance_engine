import os

from dotenv import load_dotenv
load_dotenv()


if os.getenv('APP_ENV', '') == 'PROD':
    from .production import *
else:
    try:
        from .local import *
    except ImportError:
        from .base import *
