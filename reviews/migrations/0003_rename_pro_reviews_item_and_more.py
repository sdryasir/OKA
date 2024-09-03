# Generated by Django 5.0.6 on 2024-09-03 13:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0016_remove_products_shipping_charges'),
        ('orders', '0003_alter_orders_payment_id'),
        ('reviews', '0002_rename_product_reviews_pro_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviews',
            old_name='pro',
            new_name='Item',
        ),
        migrations.AlterUniqueTogether(
            name='reviews',
            unique_together={('user', 'Item', 'order')},
        ),
    ]
