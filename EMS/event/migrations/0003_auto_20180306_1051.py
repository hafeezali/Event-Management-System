# Generated by Django 2.0.2 on 2018-03-06 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20180305_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
