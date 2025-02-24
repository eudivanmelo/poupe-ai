from django.db.models.signals import post_delete
from django.dispatch import receiver
from apps.poupeai.models import AccountTransaction, CardTransaction
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_delete, sender=AccountTransaction)
def delete_related_transaction(sender, instance, **kwargs):
    """
    Exclui a Transaction relacionada quando uma AccountTransaction é excluída.
    """
    if instance.transaction:
        instance.transaction.delete()

@receiver(post_delete, sender=CardTransaction)
def delete_related_transaction_for_card(sender, instance, **kwargs):
    """Exclui a Transaction relacionada quando uma CardTransaction é excluída."""
    try:
        transaction = instance.transaction
        if transaction and not transaction.card_transactions.exists():
            transaction.delete()
    except ObjectDoesNotExist:
        pass