from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Biblioteca, Libro, Usuario, Prestamo

@csrf_exempt
def Lista_Biblioteca(request):
    if request.method == 'GET':
        bibliotecas = list(Biblioteca.objects.all().values())
        return JsonResponse(bibliotecas, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        biblioteca = Biblioteca.objects.create(
            Nombre=data['Nombre'],
            Direccion=data['Direccion']
        )
        return JsonResponse({'id': biblioteca.id, 'Nombre': biblioteca.Nombre, 'Direccion': biblioteca.Direccion})

@csrf_exempt
def Detalles_Biblioteca(request, id):
    try:
        biblioteca = Biblioteca.objects.get(id=id)
    except Biblioteca.DoesNotExist:
        return JsonResponse({'error': 'Biblioteca no encontrada'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': biblioteca.id, 'Nombre': biblioteca.Nombre, 'Direccion': biblioteca.Direccion})
    elif request.method == 'DELETE':
        biblioteca.delete()
        return JsonResponse({'message': 'Biblioteca eliminada correctamente'})

@csrf_exempt
def Lista_Libro(request):
    if request.method == 'GET':
        libros = list(Libro.objects.all().values())
        return JsonResponse(libros, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            biblioteca = Biblioteca.objects.get(id=data['Biblioteca'])
        except Biblioteca.DoesNotExist:
            return JsonResponse({'error': 'Biblioteca no encontrada'}, status=404)

        libro = Libro.objects.create(
            Titulo=data['Titulo'],
            Autor=data['Autor'],
            Biblioteca=biblioteca,
            Prestado=data.get('Prestado', False)
        )
        return JsonResponse({'id': libro.id, 'Titulo': libro.Titulo, 'Autor': libro.Autor, 'Biblioteca': libro.Biblioteca.id, 'Prestado': libro.Prestado})

@csrf_exempt
def Detalles_Libro(request, id):
    try:
        libro = Libro.objects.get(id=id)
    except Libro.DoesNotExist:
        return JsonResponse({'error': 'Libro no encontrado'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': libro.id, 'Titulo': libro.Titulo, 'Autor': libro.Autor, 'Biblioteca': libro.Biblioteca.id, 'Prestado': libro.Prestado})
    elif request.method == 'DELETE':
        libro.delete()
        return JsonResponse({'message': 'Libro eliminado correctamente'})
    elif request.method == 'PUT':
        libro.Prestado = True
        libro.save()
        return JsonResponse({'message': 'Libro marcado como prestado'})

@csrf_exempt
def Lista_Usuario(request):
    if request.method == 'GET':
        usuarios = list(Usuario.objects.all().values())
        return JsonResponse(usuarios, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        usuario = Usuario.objects.create(
            NombreUsuario=data['NombreUsuario'],
            Email=data['Email']
        )
        return JsonResponse({'id': usuario.id, 'NombreUsuario': usuario.NombreUsuario, 'Email': usuario.Email})

@csrf_exempt
def Detalles_Usuario(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': usuario.id, 'NombreUsuario': usuario.NombreUsuario, 'Email': usuario.Email})
    elif request.method == 'DELETE':
        usuario.delete()
        return JsonResponse({'message': 'Usuario eliminado correctamente'})

@csrf_exempt
def Lista_Prestamo(request):
    if request.method == 'GET':
        prestamos = list(Prestamo.objects.all().values())
        return JsonResponse(prestamos, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            usuario = Usuario.objects.get(id=data['Usuario'])
            libro = Libro.objects.get(id=data['Libro'])
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Libro.DoesNotExist:
            return JsonResponse({'error': 'Libro no encontrado'}, status=404)

        if libro.Prestado:
            return JsonResponse({'error': 'Libro ya prestado'}, status=400)

        prestamo = Prestamo.objects.create(
            Libro=libro,
            Usuario=usuario
        )
        libro.Prestado = True
        libro.save()

        return JsonResponse({'id': prestamo.id, 'Libro': prestamo.Libro.id, 'Usuario': prestamo.Usuario.id, 'Fecha_prestamo': prestamo.Fecha_prestamo})

@csrf_exempt
def Detalles_Prestamo(request, id):
    try:
        prestamo = Prestamo.objects.get(id=id)
    except Prestamo.DoesNotExist:
        return JsonResponse({'error': 'Préstamo no encontrado'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': prestamo.id,
            'Libro': prestamo.Libro.id,
            'Usuario': prestamo.Usuario.id,
            'Fecha_prestamo': prestamo.Fecha_prestamo,
            'Fecha_devolucion': prestamo.Fecha_devolucion
        })
    elif request.method == 'PUT':
        data = json.loads(request.body)
        prestamo.Fecha_devolucion = data.get('Fecha_devolucion')
        prestamo.Libro.Prestado = False
        prestamo.Libro.save()
        prestamo.save()
        return JsonResponse({'message': 'Libro devuelto correctamente'})
