# Generated by Django 4.2.9 on 2024-08-08 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0003_order_orderitem"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="shipping_address1",
            new_name="shipping_address",
        ),
    ]
