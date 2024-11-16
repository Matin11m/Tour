# Generated by Django 5.0.7 on 2024-11-16 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0006_banner_city_province_remove_profile_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='transport',
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='images_category/'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='Tour.category'),
        ),
        migrations.AddField(
            model_name='tour',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='tour/'),
        ),
        migrations.AddField(
            model_name='tour',
            name='required_documents',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='tour',
            name='tour_rules',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='tour',
            name='tour_services',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='duration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='stay',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='trip_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to='header_banner/'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='CityBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='City_banners/')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_banners', to='Tour.city')),
            ],
        ),
        migrations.CreateModel(
            name='FirstBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='First_banners/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_banners', to='Tour.category')),
            ],
        ),
        migrations.CreateModel(
            name='TourImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='tour_images/')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_images', to='Tour.tour')),
            ],
        ),
        migrations.CreateModel(
            name='TourReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('report', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='reports/')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='Tour.tour')),
            ],
        ),
    ]
