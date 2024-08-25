# Generated by Django 5.0.6 on 2024-08-25 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header_footer', '0006_remove_footersection_footer_remove_footer_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footer',
            name='create',
        ),
        migrations.RemoveField(
            model_name='footer',
            name='name',
        ),
        migrations.RemoveField(
            model_name='footer',
            name='url',
        ),
        migrations.AddField(
            model_name='footer',
            name='title',
            field=models.CharField(default='Default Footer Title', max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='FooterSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('footer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='header_footer.footer')),
            ],
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='header_footer.footersection')),
            ],
        ),
    ]
