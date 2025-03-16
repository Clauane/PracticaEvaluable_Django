from django.db import models

# En los modelos se crean los objetos de la base de datos

class Biblioteca(models.Model):
    id = models.AutoField(primary_key=True)
    Nombre=models.CharField(max_length=255)
    Direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.Nombre
    
class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    Titulo = models.CharField(max_length=255)
    Autor = models.CharField(max_length=255)
    Biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE, related_name='libros') 
    Prestado = models.BooleanField(default=False)

    def __str__(self):
        return self.Titulo
    
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    NombreUsuario = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)

    def __str__(self):
        return self.NombreUsuario
    
class Prestamo(models.Model):
    id = models.AutoField(primary_key=True)
    Libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos')
    Fecha_prestamo = models.DateTimeField(auto_now_add=True)
    Fecha_devolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.Usuario.NombreUsuario} - {self.Libro.Titulo}'


