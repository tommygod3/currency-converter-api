# Generated by Django 3.0.2 on 2020-01-12 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_auto_20200112_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='name',
            field=models.CharField(default='none', max_length=100),
            preserve_default=False,
        ),
    ]
