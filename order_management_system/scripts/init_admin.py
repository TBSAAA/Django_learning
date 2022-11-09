# start Django project
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_management_system.settings')
django.setup()  # Let django start

from web import models
from utils.encrypt import md5

models.Administrator.objects.create(
    username='admin',
    password=md5('admin'),
    mobile='12345678901'
)
