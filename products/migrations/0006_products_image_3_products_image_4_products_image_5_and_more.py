# Generated by Django 5.0.6 on 2024-08-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_products_image_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image_3',
            field=models.FileField(blank=True, max_length=60, null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='products',
            name='image_4',
            field=models.FileField(blank=True, max_length=60, null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='products',
            name='image_5',
            field=models.FileField(blank=True, max_length=60, null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='products',
            name='image_6',
            field=models.FileField(blank=True, max_length=60, null=True, upload_to='products/'),
        ),
    ]
