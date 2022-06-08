# Generated by Django 3.2.5 on 2021-10-10 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product_gender'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.product'),
        ),
    ]
