import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monawe.settings")
django.setup()

from user.models import User, Address

CSV_PATH_USERS = 'csv_data/users/users.csv'