# Generated by Django 5.2.1 on 2025-06-05 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_category_slug_alter_product_org_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
        migrations.DeleteModel(
            name='Categorization',
        ),
    ]
