# Generated by Django 3.2.5 on 2021-10-11 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_rename_description_product_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='reviews',
        ),
    ]
