from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    storage_used = models.BigIntegerField(default=0)
    max_storage = models.BigIntegerField(default=100*1024*1024)
    
    # Override with custom related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    def __str__(self):
        return self.username