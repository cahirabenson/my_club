# Generated by Django 3.2.6 on 2021-09-19 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Members',
            new_name='Member',
        ),
    ]
