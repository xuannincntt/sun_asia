# Generated by Django 5.2.1 on 2025-06-05 16:41

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
