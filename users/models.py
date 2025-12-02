from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from common.models import TimeStampedModel
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Custom User Model for TechVault.
    Login: Email
    Roles: Admin or Employee
    """
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPLOYEE = "EMPLOYEE", "Employee"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    # Role Field - Key for your "Role Enforcement" requirement
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.EMPLOYEE)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email & Password are required by default

    objects = CustomUserManager()

    def __str__(self):
        return self.email