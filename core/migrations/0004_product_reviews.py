# Generated by Django 3.2.5 on 2021-10-10 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_reviews_product'),
        ('core', '0003_product_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.reviews'),
        ),
    ]
