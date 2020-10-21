import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monawe.settings")
django.setup()

from product.models import Field, Category, Subcategory, Product

CSV_PATH_FIELDS = 'csv_data/field.csv'
CSV_PATH_CATEGORIES = 'csv_data/category.csv'
CSV_PATH_SUBCATEGORIES = 'csv_data/subcategory.csv'
CSV_PATH_PRODUCTS = 'csv_data/product.csv'

with open(CSV_PATH_FIELDS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Field.objects.create(name = row[0])

with open(CSV_PATH_CATEGORIES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Category.objects.create(name = row[1], field_id = row[0])

with open(CSV_PATH_SUBCATEGORIES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Subcategory.objects.create(name = row[1], category_id = row[0])

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Product.objects.create(
            name            = row[1],
            subcategory_id  = row[0],
            price           = row[2],
            origin          = row[3],
            company         = row[4],
            created_at      = row[5],
            updated_at      = row[6],
            description     = row[7],
            sales_amount    = row[8])