# Generated by Django 3.0.7 on 2020-06-30 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20200630_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='day',
            field=models.TextField(default='day_wrong', max_length=9),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.TextField(max_length=200),
        ),
    ]
