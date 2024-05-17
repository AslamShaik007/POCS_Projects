from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, null=True, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        # Assuming all users have permission to access all modules
        return True
    
    def has_perm(self, perm, obj=None):
        # For simplicity, assuming all users have all permissions
        return True