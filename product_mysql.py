import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monawe.settings")
django.setup()

from product.models import Fields, Categories, Groups, Products

CSV_PATH_FIELD = 'csv_data/field.csv'
CSV_PATH_CATEGORY = 'csv_data/category.csv'
CSV_PATH_GROUP = 'csv_data/group.csv'
CSV_PATH_PRODUCT = 'csv_data/product.csv'

with open(CSV_PATH_FIELD) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Fields.objects.create(name = row[0])

with open(CSV_PATH_CATEGORY) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Categories.objects.create(name = row[1], field = row[0])

with open(CSV_PATH_GROUP) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Groups.objects.create(name = row[1], category = row[0])

with open(CSV_PATH_PRODUCT) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Products.objects.create(name = row[1], group = row[0], price = row[2], origin = row[3], company = [4], stock =[5], date = [6] attribute = [7], gift = [8])