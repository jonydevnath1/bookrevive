# Generated by Django 4.2.9 on 2024-08-08 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0006_alter_order_payment_mathod_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="payment_mathod",
            new_name="payment_method",
        ),
    ]
