"""
Production settings for product_listing project.
This file imports all settings from settings.py and overrides settings for production.
"""

import os
from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
# You should set this as an environment variable in production
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your PythonAnywhere subdomain or custom domain here
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Configure static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configure media files for production
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Use whitenoise for serving static files (optional)
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
