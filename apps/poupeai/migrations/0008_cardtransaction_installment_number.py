# Generated by Django 5.1.3 on 2025-02-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poupeai', '0007_alter_accounttransaction_payment_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardtransaction',
            name='installment_number',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
