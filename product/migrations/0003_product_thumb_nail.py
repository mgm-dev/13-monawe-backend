# Generated by Django 3.1.2 on 2020-10-23 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_color_hex_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thumb_nail',
            field=models.URLField(null=True),
        ),
    ]