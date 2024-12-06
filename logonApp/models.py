# logonApp/models.py  
from django.contrib.auth.models import AbstractUser  
from django.db import models  

class CustomUser(AbstractUser):  
    USER_TYPE_CHOICES = (  
        ('cliente', 'Cliente'),  
        ('administrador', 'Administrador'),  
    )  
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='cliente')  

    groups = models.ManyToManyField(  
        'auth.Group',  
        related_name='logonapp_customuser_set',  # Nombre único para evitar conflictos  
        blank=True,  
        help_text='The groups this user belongs to.',  
        verbose_name='groups',  
    )  
    
    user_permissions = models.ManyToManyField(  
        'auth.Permission',  
        related_name='logonapp_customuser_permissions_set',  # Nombre único para evitar conflictos  
        blank=True,  
        help_text='Specific permissions for this user.',  
        verbose_name='user permissions',  
    )  

    def __str__(self):  
        return self.username