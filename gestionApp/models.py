from django.db import models  
from django.utils import timezone  
from django.contrib.auth.models import AbstractUser  

# modelo Articulo ahora BD y API EVA 4
class Articulo(models.Model):  
    codigo = models.IntegerField(unique=True)  
    descripcion = models.CharField(max_length=255)  
    categoria = models.CharField(max_length=100)  
    precio = models.DecimalField(max_digits=10, decimal_places=2)  
    cantidad = models.IntegerField()  
    is_active = models.BooleanField(default=True)  

    def __str__(self):  
        return self.descripcion  

class Venta(models.Model):  
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)  
    cantidad_vendida = models.IntegerField(null=False)  # Asegúrate de que no se permita null  
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)  # Se asegura de que no se permita null  
    fecha = models.DateTimeField(default=timezone.now)  
    

    def save(self, *args, **kwargs):  
        if self.total is None or self.total == 0:  # Solo si total no se ha definido o es 0  
            self.total = self.cantidad_vendida * self.articulo.precio  
        super().save(*args, **kwargs)


# gestionApp/models.py  
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
        related_name='gestionapp_customuser_set',  # Nombre único para evitar conflictos  
        blank=True,  
        help_text='The groups this user belongs to.',  
        verbose_name='groups',  
    )  
    
    user_permissions = models.ManyToManyField(  
        'auth.Permission',  
        related_name='gestionapp_customuser_permissions_set',  # Nombre único para evitar conflictos  
        blank=True,  
        help_text='Specific permissions for this user.',  
        verbose_name='user permissions',  
    )  

    def __str__(self):  
        return self.username
    
