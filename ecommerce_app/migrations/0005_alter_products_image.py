# Generated by Django 3.2.19 on 2024-01-14 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0004_alter_customer_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.CharField(max_length=250),
        ),
    ]