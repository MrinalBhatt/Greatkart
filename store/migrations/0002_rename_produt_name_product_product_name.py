# Generated by Django 5.0.4 on 2024-04-08 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='produt_name',
            new_name='product_name',
        ),
    ]
