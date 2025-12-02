

# Create your models here.
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings 
from common.models import TimeStampedModel

class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Asset(TimeStampedModel):
    """
    Represents a physical item (Laptop, Phone, License).
    Includes the 'State Machine' logic via Status choices.
    """
    # Status Choices (The State Machine)
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        ASSIGNED = "ASSIGNED", "Assigned"
        BROKEN = "BROKEN", "Broken"
        # PENDING = "PENDING", "Pending Approval"
        UNDER_REPAIR = "UNDER_REPAIR", "Under Repair"
        ARCHIVED = "ARCHIVED", "Archived"

    # Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200) # e.g. "MacBook Pro M1"
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='assets')
    serial_number = models.CharField(max_length=100, unique=True)
    
    # The "File Handling" Requirement (QR Code storage)
    image = models.ImageField(upload_to='assets/qr_codes/', blank=True, null=True)

    # Assignment Logic
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_assets'
    )
    
    status = models.CharField(
        max_length=50, 
        choices=Status.choices, 
        default=Status.AVAILABLE
    )

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    # The "Validation" Requirement
    def clean(self):
        """
        Custom Logic:
        1. An asset cannot be assigned if it is BROKEN or UNDER_REPAIR.
        2. If assigned_to is set, status must be ASSIGNED.
        """
        if self.assigned_to and self.status in [self.Status.BROKEN, self.Status.UNDER_REPAIR]:
            raise ValidationError("Cannot assign a broken or under-repair asset.")
        
        # Auto-correct status if assigned (optional helper)
        if self.assigned_to and self.status == self.Status.AVAILABLE:
            self.status = self.Status.ASSIGNED

    def save(self, *args, **kwargs):
        self.full_clean() # Force validation on every save
        super().save(*args, **kwargs)