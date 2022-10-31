import django
import pydoc
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'api_yamdb.settings'
django.setup()
pydoc.cli()