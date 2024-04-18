from flask import  Flask, render_template, request, redirect, url_for
from flask import session as ses
from src.models.model import *
from src.db import db

class MyClass:
    def __init__(self):
        self.my_boolean = False

    def get_boolean(self):
        return self.my_boolean

    def set_boolean(self, value):
        self.my_boolean = value
obj = MyClass()


def index1():   
    productos = db.connection("Select * from Producto")
    if productos:
        for Producto in productos:
            return productos
    else:
        print("No se pudieron obtener los productos.")




# Validar el usuario y la contraseña para el acceso a la plataforma
def login():
    obj.set_boolean(False)
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        # Busca al usuario en la base de datos
        user = session.query(Usuario).filter_by(usuario=usuario, contraseña=contraseña).first()

        if user:
            obj.set_boolean(True)
            # Autenticación exitosa, guarda al usuario en la sesión
            return redirect(url_for('index'))  # Redirige a la página principal después del inicio de sesión
        else:
            error='Usuario o contraseña incorrectos'
            return render_template('login.html', error=error)

    # Si no se envió un formulario POST, renderiza el formulario de inicio de sesión
    return render_template('login.html')

def logout():
    obj.set_boolean(False)
    return redirect(url_for('login'))

def index():
    if obj.get_boolean() is True:
        return render_template('index.html')
    else: 
        return redirect(url_for('login'))
def productos():
    productos = session.query(Producto).all()
    if obj.get_boolean() is True:
        return render_template('productos.html', productos=productos)
    else: 
        return redirect(url_for('login'))
    
def consultar_productos():
    return productos

def registrar_productos():
    # Obtener los datos del formulario
    tipo = request.form['tipo']
    referencia = request.form['referencia']
    cantidad = int(request.form['cantidad'])
    costo = float(request.form['costo'])
    precio = float(request.form['precio'])
    
    # Crear un nuevo objeto Producto con los datos recibidos
    nuevo_producto = Producto(tipo=tipo, referencia=referencia, cantidad=cantidad, costo=costo, precio=precio)
    
    # Guardar el nuevo producto en la base de datos
    session.add(nuevo_producto)
    session.commit()
    
    # Redirigir a la página de productos después de guardar el producto
    return redirect(url_for('productos'))

def producto():
    # Realizar una consulta para obtener todos los productos
    productos= session.query(Producto).all()
    return render_template('productos.html', productos=productos)