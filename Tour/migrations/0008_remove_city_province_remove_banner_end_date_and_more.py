# Generated by Django 5.0.7 on 2024-11-27 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0007_remove_tour_transport_category_image_category_parent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='province',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images_category/'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='Tour.category'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='tour/'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='required_documents',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='tour_rules',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='tour_services',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Province',
        ),
    ]