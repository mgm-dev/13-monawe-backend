import os
import django
import csv
import sys

from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monawe.settings")
django.setup()

from product.models import ProductOption, Color, Thickness, Tag, BodyColor, InkColor, ProductTag, ProductThickness

CSV_PATH_PRODUCTOPTIONS = 'csv_data/options/product_options.csv'
CSV_PATH_COLORS = 'csv_data/options/colors.csv'
CSV_PATH_THICKNESSES = 'csv_data/options/thicknesses.csv'
CSV_PATH_TAGS = 'csv_data/options/tags.csv'
CSV_PATH_BODYCOLORS = 'csv_data/options/body_colors.csv'
CSV_PATH_INKCOLORS = 'csv_data/options/ink_colors.csv'
CSV_PATH_PRODUCTTAGS = 'csv_data/options/product_tags.csv'
CSV_PATH_PRODUCTTHICKNESSES = 'csv_data/options/product_thickness.csv'

def option():
    with open(CSV_PATH_PRODUCTOPTIONS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            ProductOption.objects.create(product_id= row[0],stock= row[1] ,plus_price= Decimal(row[2]))

def color():
    with open(CSV_PATH_COLORS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            Color.objects.create(name= row[0])

def thickness():
    with open(CSV_PATH_THICKNESSES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            Thickness.objects.create(value= row[0])

def tag():
    with open(CSV_PATH_TAGS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            Tag.objects.create(name= row[0])

def body():
    with open(CSV_PATH_BODYCOLORS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            BodyColor.objects.create(product_option_id= row[0], color_id= row[1])

def ink():
    with open(CSV_PATH_INKCOLORS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            InkColor.objects.create(product_option_id= row[0], color_id= row[1])

def product_tag():
    with open(CSV_PATH_PRODUCTTAGS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            ProductTag.objects.create(product_id= row[0], tag_id= row[1])

def product_thickness():
    with open(CSV_PATH_PRODUCTTHICKNESSES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            ProductThickness.objects.create(product_option_id= row[0], thickness_id= row[1])


option()
color()
thickness()
tag()
body()
ink()
product_tag()
product_thickness()