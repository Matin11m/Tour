# Generated by Django 5.0.7 on 2024-11-27 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0008_remove_city_province_remove_banner_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='verification_code',
            field=models.CharField(default='2345', max_length=4),
        ),
    ]
