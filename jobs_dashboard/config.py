import os

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'jobs_aggregator.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobs_aggregator.settings")

application = get_wsgi_application()
