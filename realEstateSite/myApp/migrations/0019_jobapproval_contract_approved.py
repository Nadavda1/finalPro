# Generated by Django 5.0.6 on 2024-06-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0018_jobapproval_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapproval',
            name='contract_approved',
            field=models.BooleanField(default=False),
        ),
    ]
