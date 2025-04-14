"""
WSGI config for DjangoHUD project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
import logging

from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set up logging
logging.basicConfig(stream=sys.stderr)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoHUD.settings')

try:
    application = get_wsgi_application()
except Exception as e:
    logging.error("Error loading WSGI application: %s", str(e))
    raise
