# Generated by Django 3.2 on 2021-08-28 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('payment', '0001_initial'),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('is_paid', models.BooleanField(default=False, verbose_name='is paid')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='accounts.customer', verbose_name='customer')),
                ('invoice', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cart', to='payment.invoice', verbose_name='invoice')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='CartLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('price', models.IntegerField(default=0, verbose_name='price')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='cart.cart', verbose_name='cart')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lines', to='item.item', verbose_name='item')),
            ],
            options={
                'verbose_name': 'Cart line',
                'verbose_name_plural': 'Cart lines',
                'db_table': 'cart_line',
            },
        ),
    ]
