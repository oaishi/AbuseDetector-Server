# Generated by Django 2.2.3 on 2019-09-01 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='average_percentage',
            field=models.FloatField(default=0),
        ),
    ]
