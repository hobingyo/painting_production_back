<<<<<<< HEAD
# Generated by Django 4.0.5 on 2022-06-30 02:22
=======
# Generated by Django 4.0.5 on 2022-06-30 04:37
>>>>>>> 3cd01cd61d6f3d313669cd8f3e8d2ef773ce2617

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_alter_article_exposure_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='exposure_start_date',
<<<<<<< HEAD
            field=models.DateField(default=datetime.datetime(2022, 6, 30, 2, 22, 11, 492916, tzinfo=utc), verbose_name='게시 일자'),
=======
            field=models.DateField(default=datetime.datetime(2022, 6, 30, 4, 37, 14, 867667, tzinfo=utc), verbose_name='게시 일자'),
>>>>>>> 3cd01cd61d6f3d313669cd8f3e8d2ef773ce2617
        ),
    ]
