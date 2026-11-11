"""
WSGI config for CyberShield AI project.
Exposes 'application' and 'app' for Vercel Serverless Python runtime.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Alias for Vercel serverless deployment
app = application
