# Generated by Django 5.0.2 on 2024-05-11 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0013_jobdetail_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobdetail',
            old_name='text',
            new_name='detail_of_project',
        ),
    ]
