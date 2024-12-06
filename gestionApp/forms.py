from django import forms  
from .models import Articulo  

# Form para Artículo
class ArticuloForm(forms.ModelForm):  
    class Meta:  
        model = Articulo  
        fields = ['codigo', 'descripcion', 'categoria', 'precio', 'cantidad']  


