# Generated by Django 5.1.3 on 2025-02-21 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poupeai', '0010_alter_cardtransaction_credit_card_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounttransaction',
            name='payment_at',
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
