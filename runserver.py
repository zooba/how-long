import os
import sys
import waitress

if sys.platform == 'win32':
    import ctypes
    ctypes.WinDLL('kernel32').AddDllDirectory(os.path.join(os.path.abspath(__file__), '..', 'FreeTDS'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HowLong.settings")

from django.core.wsgi import get_wsgi_application
waitress.serve(get_wsgi_application(), port=int(os.getenv("HTTP_PLATFORM_PORT", 8080)))
