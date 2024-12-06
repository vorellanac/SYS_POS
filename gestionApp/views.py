from datetime import datetime  
from django.utils import timezone   
from django.shortcuts import render, redirect, get_object_or_404  
from .models import Articulo, Venta  
from .forms import ArticuloForm  
from django.db.models import Q 
import csv  
from django.http import HttpResponse  
from django.contrib.auth.decorators import login_required  # Importa el decorador  
# imports para apis
from django.urls import path  
from django.views.generic import CreateView, UpdateView, ListView  
from django.urls import reverse_lazy

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404 
from .serializers import ArticulosSerializers
from rest_framework import generics 


# Create your views here.  
def adm(request):  
    current_year = datetime.now().year  
    current_time = timezone.now().strftime("%H:%M")  # Formato de 24 horas  
    return render(request, 'admin.html', {'current_year': current_year})  # usado en el footer  

# Crear Artículo

def crear_articulo(request):  
    if request.method == 'POST':  
        form = ArticuloForm(request.POST)  
        if form.is_valid():  
            form.save()  # Graba en BD  
            return redirect('listar_articulos')  # Si crea el artículo, redirige a lista de artículos  
    else:  
        form = ArticuloForm()  
    return render(request, 'crear_articulo.html', {'form': form})  

# Listar Artículos  
def listar_articulos(request):  
    articulos = Articulo.objects.all()  
    return render(request, 'listar_articulos.html', {'articulos': articulos})  

#listar articulos vista simple 
def listar_articulos_sv(request):  
    articulos = Articulo.objects.all()  
    return render(request, 'listar_articulos_sv.html', {'articulos': articulos})  


# Editar Artículo  

def editar_articulo(request, codigo):  
    articulo = get_object_or_404(Articulo, codigo=codigo)  
    if request.method == 'POST':  
        form = ArticuloForm(request.POST, instance=articulo)  
        if form.is_valid():  
            form.save()  
            return redirect('listar_articulos')  
    else:  
        form = ArticuloForm(instance=articulo)  
    return render(request, 'editar_articulo.html', {'form': form})  

# Eliminar Artículo 

def eliminar_articulo(request, codigo):  
    articulo = get_object_or_404(Articulo, codigo=codigo)  
    if request.method == 'POST':  
        articulo.delete()  
        return redirect('listar_articulos')  
    return render(request, 'eliminar_articulo.html', {'articulo': articulo})   

# Vender artículos  
def vender_articulo(request, codigo):  
    # Obtener el artículo específico por código  
    articulo = get_object_or_404(Articulo, codigo=codigo)  
    productos = []  # Lista para almacenar productos encontrados  
    error_message = None  

    if request.method == 'POST':  
        search_query = request.POST.get('search', '')  
        if search_query:  
            # Buscar productos por código o nombre utilizando LIKE  
            productos = Articulo.objects.filter(  
                Q(codigo__icontains=search_query) | Q(descripcion__icontains=search_query)  
            )  
        
        # Procesar la venta de múltiples artículos  
        selected_product_ids = request.POST.getlist('productos')  
        if selected_product_ids:  
            for product_id in selected_product_ids:  
                cantidad_a_vender = int(request.POST.get(f'cantidad_{product_id}', 0))  
                articulo_a_vender = get_object_or_404(Articulo, id=product_id)  

                if cantidad_a_vender > 0 and cantidad_a_vender <= articulo_a_vender.cantidad:  
                    # Calcular total  
                    total = cantidad_a_vender * articulo_a_vender.precio  

                    # Crear la venta  
                    venta = Venta(articulo=articulo_a_vender, cantidad_vendida=cantidad_a_vender, total=total)  
                    venta.save()  # Guardar la venta en la base de datos  

                    # Descontar cantidad del artículo  
                    articulo_a_vender.cantidad -= cantidad_a_vender  
                    articulo_a_vender.save()  
                else:  
                    error_message = "Cantidad no válida para uno o más artículos."  
                    break  

            if not error_message:  
                return render(request, 'procesar_venta.html', {  
                    'fecha': venta.fecha,  
                    'total': total,  
                })  
    
    return render(request, 'vender_articulo.html', {'articulo': articulo, 'productos': productos, 'error_message': error_message})  

# Activar artículo  
def activar_articulo(request, codigo):  
    articulo = get_object_or_404(Articulo, codigo=codigo)  
    if request.method == 'POST':  
        articulo.is_active = True  
        articulo.save()  
        return redirect('listar_articulos')  
    return render(request, 'activar_articulo.html', {'articulo': articulo})   

# Desactivar artículo 

def desactivar_articulo(request, codigo):  
    articulo = get_object_or_404(Articulo, codigo=codigo)  
    if request.method == 'POST':  
        articulo.is_active = False  
        articulo.save()  
        return redirect('listar_articulos')  
    return render(request, 'desactivar_articulo.html', {'articulo': articulo})   

# Reportes de ventas  
def listar_ventas(request):  
    ventas = Venta.objects.all()  # Obtener todas las ventas  
    total_ventas = []  

    for venta in ventas:  
        total_ventas.append({  
            'codigo': venta.articulo.codigo,  
            'descripcion': venta.articulo.descripcion,  
            'cantidad': venta.cantidad_vendida,  
            'total': venta.total,         
            'fecha': venta.fecha,  
        })  

    return render(request, 'listar_ventas.html', {'total_ventas': total_ventas})

# Logica para procesar venta. 
def procesar_venta(request):  
    if request.method == 'POST':  
        total = 0  
        fecha = None  
        error_message = None  

        # Aquí deberías recoger los datos del POST  
        selected_product_ids = request.POST.getlist('productos')  
        for product_id in selected_product_ids:  
            cantidad_a_vender = int(request.POST.get(f'cantidad_{product_id}', 0))  
            articulo_a_vender = get_object_or_404(Articulo, id=product_id)  

            if cantidad_a_vender > 0 and cantidad_a_vender <= articulo_a_vender.cantidad:  
                # Calcular total  
                total += cantidad_a_vender * articulo_a_vender.precio  

                # Crear la venta  
                venta = Venta(articulo=articulo_a_vender, cantidad_vendida=cantidad_a_vender, total=total)  
                venta.save()  

                # Descontar cantidad del artículo  
                articulo_a_vender.cantidad -= cantidad_a_vender  
                articulo_a_vender.save()  
                fecha = venta.fecha  # Guarda la fecha de la venta  
            else:  
                error_message = "Cantidad no válida para uno o más artículos."  
                break  

        # Renderizar la plantilla de confirmación  
        return render(request, 'venta_confirmacion.html', {'total': total, 'fecha': fecha, 'error_message': error_message})  

    return render(request, 'error.html', {'message': 'Método no permitido'})

# Exportar Ventas
def exportar_ventas_csv(request):  
    # Crear la respuesta HTTP con el tipo de contenido adecuado  
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="ventas.csv"'  

    # Crear el escritor CSV  
    writer = csv.writer(response)  
    writer.writerow(['Codigo', 'Descripcion', 'Cantidad', 'Total','Fecha'])  # Encabezados del CSV  

    # Obtener las ventas realizadas  
    total_ventas = Venta.objects.all()  # Ajusta esto según tu lógica para obtener las ventas  

    # Escribir los datos de las ventas en el CSV  
    for venta in total_ventas:  
        writer.writerow([venta.articulo.codigo, venta.articulo.descripcion, venta.cantidad_vendida, venta.total, venta.fecha])  

    return response  

# Consultar API 
def consultar_api(request):  
    return render(request, 'consultar_api.html')
  

from rest_framework import generics  
from .models import Articulo  
from .serializers import ArticulosSerializers  

# Vista para listar y crear artículos (CRUD)  
class ArticuloList(generics.ListCreateAPIView):  
    queryset = Articulo.objects.all()  
    serializer_class = ArticulosSerializers  

# Vista para obtener, actualizar y eliminar un artículo específico (CRUD)  
class ArticuloDetail(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Articulo.objects.all()  
    serializer_class = ArticulosSerializers  


from django.shortcuts import render, redirect, get_object_or_404  
from rest_framework import generics  
from .models import Articulo  
from .serializers import ArticulosSerializers  

# Vista para listar y crear artículos  
class ArticuloList(generics.ListCreateAPIView):  
    queryset = Articulo.objects.all()  
    serializer_class = ArticulosSerializers  

# Vista para obtener, actualizar y eliminar un artículo específico  
class ArticuloDetail(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Articulo.objects.all()  
    serializer_class = ArticulosSerializers  

# Vista para crear un nuevo artículo  
def crear_articulo(request):  
    if request.method == 'POST':  
        form = ArticuloForm(request.POST)  
        if form.is_valid():  
            form.save()  
            return redirect('articulo-list')  # Redirige a la lista de artículos  
    else:  
        form = ArticuloForm()  
    return render(request, 'crear_articulo.html', {'form': form})  

# Vista para editar un artículo existente  
def editar_articulo(request, pk):  
    articulo = get_object_or_404(Articulo, pk=pk)  
    if request.method == 'POST':  
        form = ArticuloForm(request.POST, instance=articulo)  
        if form.is_valid():  
            form.save()  
            return redirect('articulo-list')  # Redirige a la lista de artículos  
    else:  
        form = ArticuloForm(instance=articulo)  
    return render(request, 'editar_articulo.html', {'form': form})