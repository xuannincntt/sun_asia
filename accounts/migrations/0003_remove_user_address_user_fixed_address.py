# Generated by Django 5.2.1 on 2025-06-03 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.AddField(
            model_name='user',
            name='fixed_address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
