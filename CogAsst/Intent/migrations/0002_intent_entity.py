# Generated by Django 3.2.6 on 2022-08-08 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Intent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='intent',
            name='entity',
            field=models.TextField(default='', max_length=300),
        ),
    ]
