# Generated by Django 3.2.5 on 2023-07-16 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_product_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='orders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.order'),
        ),
    ]