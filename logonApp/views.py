from django.shortcuts import render, redirect
# import para login
from .forms  import CustomUserCreationForm, CustomUserLoginForm 
from django.contrib.auth import login, authenticate  
from django.contrib import messages  
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm 
from django.shortcuts import get_object_or_404  

# logonApp/views.py     
def index(request):  
    # Lógica para la vista del administrador  
    return render(request, 'logonApp/index.html')


# Redirigir usuario: 
def seleccionar_tipo_usuario(request):  
    if request.method == 'POST':  
        user_type = request.POST.get('user_type')  
        
        if user_type == 'visita':  
            return redirect('listar_articulos_sv')  # Cambia 'vista_visita' por el nombre de la vista correspondiente  
        elif user_type == 'cliente':  
            return redirect('login')  # Cambia 'vista_cliente' por el nombre de la vista correspondiente  
        elif user_type == 'administrador':  
            return redirect('admin')  # Cambia 'vista_administrador' por el nombre de la vista correspondiente  
        else:  
            # Manejo de error si el tipo de usuario no es válido  
            return render(request, 'error.html', {'mensaje': 'Tipo de usuario no válido.'})  
    
    return render(request, 'login.html')  # Cambia 'tu_template.html' por el nombre de tu plantilla

# logonApp/views.py  
def login_view(request):  
    if request.method == 'POST':  
        user_type = request.POST.get('user_type')  
        if user_type in ['visita', 'cliente']:  
            return redirect('procesar_venta')  
        elif user_type == 'administrador':  
            return redirect('admin')  
    # Para solicitudes GET, renderiza el formulario de inicio de sesión  
    return render(request, 'logonApp/login.html')


#Accesos vistas
def vista_visita(request):  
    return render(request, 'listar_articulos_sv.html')  # Cambia 'listar_articulos_sv.html'  

def vista_cliente(request):  
    return render(request, 'vender_articulo.html')  # Cambia 'login y tras hacer el login debe enviar a vender_articulo.html'  

def vista_administrador(request):  
    return render(request, 'admin.html')  # Cambia 'administrador.html'

# register
def register(request):  
    if request.method == 'POST':  
        username = request.POST.get('username')  # Cambiado a get()  
        password = request.POST.get('password')  # Cambiado a get()  

        if username and password:  # Verifica que ambos campos estén presentes  
            try:  
                user = User.objects.create_user(username=username, password=password)  
                user.save()  
                messages.success(request, 'Usuario registrado exitosamente.')  
                return redirect('login')  # Redirige a la página de inicio de sesión  
            except Exception as e:  
                messages.error(request, f'Error al registrar el usuario: {e}')  
        else:  
            messages.error(request, 'Por favor, completa todos los campos.')  

    return render(request, 'logonApp/register.html')  

# Determinar el acceso
def login_view(request):  
    if request.method == 'POST':  
        form = AuthenticationForm(request, data=request.POST)  
        if form.is_valid():  
            username = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')  
            user = authenticate(request, username=username, password=password)  
            if user is not None:  
                login(request, user)  
                # Verifica si el usuario es administrador  
                if user.is_superuser:  # O puedes usar un campo específico si tienes uno  
                    return redirect('admin')  # Redirige a la vista admin.html  
                else:  
                    return redirect('listar_articulos_sv')  # Redirige a la vista de usuario normal  
            else:  
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')  
    else:  
        form = AuthenticationForm()  
    return render(request, 'logonApp/login.html', {'form': form})  

# Cierre de sesion
def custom_logout(request):  
    logout(request)  # Cierra la sesión del usuario  
    messages.success(request, 'Has cerrado sesión exitosamente.')  # Mensaje de éxito  
    return render(request, 'logonApp/logout.html')  # Renderiza la plantilla de logout  

#Administracion de usuarios:
def administrar_usuarios(request):  
    if not request.user.is_superuser:  
        messages.error(request, "No tienes permiso para acceder a esta página.")  
        return redirect('index')  # Redirige a la página principal si no es administrador  

    usuarios = User.objects.all()  # Obtiene todos los usuarios  
    return render(request, 'logonApp/administrar_usuarios.html', {'usuarios': usuarios})  

# Editar usuario:
def editar_usuario(request, user_id):  
    usuario = get_object_or_404(User, id=user_id)  
    if request.method == 'POST':  
        usuario.username = request.POST.get('username')  
        usuario.email = request.POST.get('email')  
        is_superuser = request.POST.get('is_superuser') == 'True'  # Convierte el valor a booleano  
        usuario.is_superuser = is_superuser  # Actualiza el estado de superusuario  
        usuario.save()  
        messages.success(request, 'Usuario actualizado exitosamente.')  
        return redirect('administrar_usuarios')  
    return render(request, 'logonApp/editar_usuario.html', {'usuario': usuario})  

# Vista para Eliminar Usuario
def eliminar_usuario(request, user_id):  
    usuario = get_object_or_404(User, id=user_id)  
    usuario.delete()  
    messages.success(request, 'Usuario eliminado exitosamente.')  
    return redirect('administrar_usuarios')


#vista agregar_usuario
def agregar_usuario(request):  
    if request.method == 'POST':  
        username = request.POST.get('username')  
        email = request.POST.get('email')  
        password = request.POST.get('password')  
        is_superuser = request.POST.get('is_superuser') == 'True'  # Convierte el valor a booleano  

        # Crear el nuevo usuario  
        try:  
            usuario = User.objects.create_user(username=username, email=email, password=password)  
            usuario.is_superuser = is_superuser  
            usuario.save()  
            messages.success(request, 'Usuario agregado exitosamente.')  
            return redirect('administrar_usuarios')  
        except Exception as e:  
            messages.error(request, f'Error al agregar usuario: {e}')  

    return render(request, 'logonApp/agregar_usuario.html')  