# Generated by Django 5.1.3 on 2025-02-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poupeai', '0006_remove_transaction_fixed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='payment_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
