# Generated by Django 4.2.6 on 2023-10-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0002_remove_products_image_remove_products_subimage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]