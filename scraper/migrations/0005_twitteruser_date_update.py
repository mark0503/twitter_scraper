# Generated by Django 4.1.2 on 2022-10-10 05:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_alter_twitteruser_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='date_update',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date update'),
        ),
    ]
