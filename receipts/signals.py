from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Receipt
from .tasks import fetch_places_for_receipt


@receiver(post_save, sender=Receipt)
def receipt_created(sender, instance, created, **kwargs):
    if not created:
        return
    # Enqueue task to fetch places for this receipt's address
    address = instance.address or ''
    fetch_places_for_receipt.delay(instance.id, address)
