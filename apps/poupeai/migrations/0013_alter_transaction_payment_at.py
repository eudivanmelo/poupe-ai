# Generated by Django 5.1.3 on 2025-02-21 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poupeai', '0012_alter_transaction_payment_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
