# Generated by Django 3.2.6 on 2021-09-20 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_rename_members_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='email_address',
            field=models.EmailField(blank=True, max_length=255, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='phone',
            field=models.CharField(blank=True, max_length=25, verbose_name='Contact Phone'),
        ),
    ]
