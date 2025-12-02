from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory.models import Asset
from audit.models import AuditLog
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Asset)
def log_asset_change(sender, instance, created, **kwargs):
    """
    Automatically creates an AuditLog entry whenever an Asset is saved.
    """
    action = "CREATED" if created else "UPDATED"
    
    # Logic to determine specific actions (Assignment/Return)
    if not created:
        if instance.status == 'ASSIGNED':
             action = "ASSIGNED"
        elif instance.status == 'AVAILABLE':
             action = "RETURNED"

    AuditLog.objects.create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,
        action=action,
        changes={"status": instance.status} 
    )