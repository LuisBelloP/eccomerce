# Generated by Django 3.2.19 on 2024-01-28 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0009_alter_order_code_postal'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='calle',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
