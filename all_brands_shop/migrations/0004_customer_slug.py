# Generated by Django 4.0.6 on 2022-08-20 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_brands_shop', '0003_orderitem_size_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=models.SlugField(max_length=250, null=True, unique=True, verbose_name='url'),
        ),
    ]
