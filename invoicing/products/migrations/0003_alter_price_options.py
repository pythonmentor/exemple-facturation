# Generated by Django 4.0.5 on 2022-06-30 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_price_product_currency_unicity_constraint'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ['-date_created']},
        ),
    ]
