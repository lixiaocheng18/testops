# coding:utf-8
__author__ = 'lilx 14-12-29'
from django.core.wsgi import get_wsgi_application
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


application = get_wsgi_application()