# Generated by Django 4.2.4 on 2023-08-10 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='account',
            name='lastname',
        ),
    ]
