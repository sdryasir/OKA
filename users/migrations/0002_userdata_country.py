# Generated by Django 5.0.6 on 2024-08-23 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
