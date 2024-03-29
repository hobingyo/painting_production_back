# Generated by Django 4.0.5 on 2022-07-04 15:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_alter_article_exposure_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='exposure_start_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 4, 15, 54, 58, 877598, tzinfo=utc), verbose_name='게시 일자'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_converted',
            field=models.FileField(null=True, upload_to='article/converted/'),
        ),
    ]
