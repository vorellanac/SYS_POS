from rest_framework import serializers  
from .models import Articulo  

class ArticulosSerializers(serializers.ModelSerializer):  
    class Meta:  
        model = Articulo  
        fields = '__all__'  