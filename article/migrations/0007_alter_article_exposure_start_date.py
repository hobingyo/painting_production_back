# Generated by Django 4.0.5 on 2022-07-05 08:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_alter_article_exposure_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='exposure_start_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 5, 8, 42, 20, 361517, tzinfo=utc), verbose_name='게시 일자'),
        ),
    ]
