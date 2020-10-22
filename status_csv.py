import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monawe.settings")
django.setup()

from order.models import Status

CSV_PATH_STATUS = 'csv_data/status.csv'

with open(CSV_PATH_STATUS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Status.objects.create(name = row[0])