# Generated by Django 4.2.11 on 2024-04-01 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='type',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='body',
            new_name='description',
        ),
    ]
