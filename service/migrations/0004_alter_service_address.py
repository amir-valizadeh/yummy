# Generated by Django 3.2 on 2021-08-31 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0006_rename_user_customeraddress_customer_user'),
        ('service', '0003_alter_service_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='address.serviceaddress', verbose_name='address'),
        ),
    ]
