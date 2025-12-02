from django.db import models

# Create your models here.
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.models import TimeStampedModel

class AuditLog(TimeStampedModel):
    """
    The 'Ghost' Log.
    Uses GenericForeignKey to track any model (Assets, Users, etc.).
    """
    # Polymorphic Fields (The Magic)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=50) # Using Char to support UUIDs
    content_object = GenericForeignKey('content_type', 'object_id')

    # Action Details
    action = models.CharField(max_length=50) # e.g. "CREATED", "UPDATED"
    changes = models.JSONField(null=True, blank=True) # Store what changed (Old vs New)

    def __str__(self):
        return f"{self.action} - {self.content_object}"