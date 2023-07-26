"""
WSGI config for techmax project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techmax.settings")
app = application = get_wsgi_application()
# app = get_wsgi_application()

# https://www.youtube.com/watch?v=ZjVzHcXCeMU
# wird für die .vercel.app benötigt
# app = application




