"""
URL configuration for sistemaVentas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestionApp.views import adm, crear_articulo, listar_articulos,editar_articulo, eliminar_articulo, vender_articulo, listar_ventas, desactivar_articulo, activar_articulo,vender_articulo,procesar_venta,exportar_ventas_csv,listar_articulos_sv, consultar_api, ArticuloList, ArticuloDetail

#Llamada a login view desde logonApp
from logonApp.views import login_view, index, seleccionar_tipo_usuario, register, custom_logout, administrar_usuarios, editar_usuario, eliminar_usuario, agregar_usuario
#Para llamar desde funciones de login desde la app gestion a login APP
from django.contrib import admin  
from django.urls import path, include  


urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('', index),  
    path('administrador/', adm, name='admin'),
    path('articulos/nuevo/', crear_articulo, name='crear_articulo'),  
    path('articulos/', listar_articulos, name='listar_articulos'),  
    path('articulosv/', listar_articulos_sv, name='listar_articulos_sv'), #Vista simple solo articulos
    path('articulos/editar/<int:codigo>/', editar_articulo, name='editar_articulo'),  
    path('articulos/eliminar/<int:codigo>/', eliminar_articulo, name='eliminar_articulo'),   
    path('articulos/desactivar/<int:codigo>/', desactivar_articulo, name='desactivar_articulo'),  
    path('articulos/activar/<int:codigo>/', activar_articulo, name='activar_articulo'),  
    path('articulos/vender/<int:codigo>/', vender_articulo, name='vender_articulo'),  # URL para vender   
    path('ventas/', listar_ventas, name='listar_ventas'),  # URL para listar ventas  
    path('articulos/procesar/', procesar_venta, name='venta_confirmacion'),  
    path('articulos/procesar/', procesar_venta, name='procesar_venta'),
    path('articulos/exportar/ventas/csv/', exportar_ventas_csv, name='exportar_ventas_csv'),
    #LogonApp urls
    path('seleccionar-tipo-usuario/', seleccionar_tipo_usuario, name='seleccionar_tipo_usuario'),
    path('login/', login_view, name='login'),  #vista principal 
    path('procesar_venta/', procesar_venta, name='procesar_venta'), # Si es visita o cliente pasa a esta vista. 
    path('index/', index, name='index'),  #si el usuario login es == adm pasa a la vista admin. 
    #login
    path('register/', register, name='register'),  
    path('login/', login_view, name='login'), 
    path('logout/', custom_logout, name='logout'),     
    #administracion de usuarios
    path('administrar_usuarios/', administrar_usuarios, name='administrar_usuarios'),  # Nueva URL
    path('editar_usuario/<int:user_id>/', editar_usuario, name='editar_usuario'),  # Nueva URL  
    path('eliminar_usuario/<int:user_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('agregar_usuario/', agregar_usuario, name='agregar_usuario'),  # Nueva URL  
    #Consultar API Externa
    path('consultar-api/', consultar_api, name='consultar_api'),  
    #Consultar API Interna
    path('api/articulos/', ArticuloList.as_view(), name='articulo-list'),  # Listar y crear artículos  
    path('api/articulos/<int:pk>/edit', ArticuloDetail.as_view(), name='articulo-detail'),  # Detalle, actualizar y eliminar un artículo  
    path('api/articulos/', ArticuloList.as_view(), name='articulo-list'),  # Listar y crear artículos  
    path('api/articulos/<int:pk>/', ArticuloDetail.as_view(), name='articulo-detail'),  # Detalle, actualizar y eliminar un artículo  
    path('articulos/nuevo/', crear_articulo, name='articulo-create'),  # Crear artículo  
    path('articulos/<int:pk>/edit/', editar_articulo, name='articulo-edit'),  # Editar artículo  
       
]  
 



