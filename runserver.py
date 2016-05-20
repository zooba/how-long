import os
import sys
import waitress

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HowLong.settings")

from HowLong.wsgi import application
waitress.serve(application, port=int(os.getenv("HTTP_PLATFORM_PORT", 8080)))
