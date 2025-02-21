# Generated by Django 5.1.3 on 2025-02-21 14:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poupeai', '0009_alter_cardtransaction_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardtransaction',
            name='credit_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_card', to='poupeai.creditcard'),
        ),
        migrations.AlterField(
            model_name='cardtransaction',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice', to='poupeai.invoice'),
        ),
        migrations.AlterField(
            model_name='cardtransaction',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_transactions', to='poupeai.transaction'),
        ),
    ]
