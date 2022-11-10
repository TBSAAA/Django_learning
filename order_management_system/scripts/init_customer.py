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

# Create level
# level_object = models.Level.objects.create(title="VIP", percent=90)

models.Customer.objects.create(
    username='jack',
    password=md5("jack"),
    mobile='2222222222',
    level_id=1,
    creator_id=1
)
