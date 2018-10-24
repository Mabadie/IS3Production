"""
WSGI config for sharebooks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
import os



from whitenoise import WhiteNoise

from django.core.wsgi import get_wsgi_application
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharebooks.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=BASE_DIR+'/media')
