# Generated by Django 3.0.6 on 2021-08-12 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_picture',
            field=models.ImageField(default='', null=True, upload_to='Display Picture'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email_address',
            field=models.CharField(default='accounts.CustomUser', max_length=250),
        ),
    ]