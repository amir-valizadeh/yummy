# Generated by Django 3.2 on 2021-09-12 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='invoice',
        ),
    ]
