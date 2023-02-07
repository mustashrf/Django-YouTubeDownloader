import os
from celery import Celery
from environs import Env as env

env.__setattr__('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')
