# Generated by Django 4.0.5 on 2022-06-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='post_code',
            new_name='postal_code',
        ),
        migrations.AddField(
            model_name='order',
            name='country_code',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_option',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
