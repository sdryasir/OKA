# Generated by Django 5.0.6 on 2024-08-11 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0008_alter_products_image4_alter_products_image5_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='title',
            new_name='name',
        ),
    ]
