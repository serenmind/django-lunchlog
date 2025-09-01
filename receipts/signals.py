from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import logging

from .models import Receipt, ReceiptImage
from .tasks import fetch_places_for_receipt

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Receipt)
def receipt_created(sender, instance, created, **kwargs):
    if not created:
        return
    # Enqueue task to fetch places for this receipt's address
    address = instance.address or ''
    fetch_places_for_receipt.delay(instance.id, address)


@receiver(post_delete, sender=ReceiptImage)
def delete_image_file_on_model_delete(sender, instance, **kwargs):
    """Delete image file from storage when a ReceiptImage is deleted."""
    try:
        if instance.image:
            instance.image.delete(save=False)
    except Exception:
        logger.exception('Failed to delete image file for ReceiptImage %s', getattr(instance, 'pk', None))
