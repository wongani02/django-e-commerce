# Generated by Django 4.0.5 on 2022-06-20 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_users_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='digital_product',
            field=models.FileField(blank=True, upload_to='digital-product/'),
        ),
    ]
