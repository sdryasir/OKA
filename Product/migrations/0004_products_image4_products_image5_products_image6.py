# Generated by Django 5.0.6 on 2024-08-06 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_alter_products_image2_alter_products_image3'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image4',
            field=models.FileField(blank=True, help_text='Image size must be 500 X 500 pixels', null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='products',
            name='image5',
            field=models.FileField(blank=True, help_text='Image size must be 500 X 500 pixels', null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='products',
            name='image6',
            field=models.FileField(blank=True, help_text='Image size must be 500 X 500 pixels', null=True, upload_to='products/'),
        ),
    ]
