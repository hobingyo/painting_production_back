# Generated by Django 4.0.5 on 2022-07-05 04:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_alter_article_exposure_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='exposure_start_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 5, 4, 31, 12, 461505, tzinfo=utc), verbose_name='게시 일자'),
        ),
    ]
