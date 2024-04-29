from flask import render_template, request, redirect, url_for
from flask import session
from src.models.model import *
from datetime import datetime, timedelta
# from src.db import db

class MyClass:
    def __init__(self):
        self.my_boolean = False

    def get_boolean(self):
        return self.my_boolean

    def set_boolean(self, value):
        self.my_boolean = value
obj = MyClass()


# def index1():   
#     productos = db.connection("Select * from Producto")
#     if productos:
#         for Producto in productos:
#             return productos
#     else:
#         print("No se pudieron obtener los productos.")




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
    #Cual es la fecha de hace 20 días
    fecha20 = datetime.now() - timedelta(days=20)
    #comparar las fechas y el tipo de venta
    ventas_fiadas = session.query(Venta).filter(Venta.fecha <= fecha20, Venta.tipoPago == 'Fiado').all()
    
    ids_clientes_con_deuda = [venta.identificacion for venta in ventas_fiadas]

    clientes_con_deuda = session.query(Cliente).filter(Cliente.identificacion.in_(ids_clientes_con_deuda)).all()

    productos_bajo_stock = session.query(Producto).filter(Producto.cantidad <= 10).all()

    deuda_clientes = {}
    for cliente in clientes_con_deuda:
        deuda = 0
        for venta in ventas_fiadas:
            if venta.identificacion == cliente.identificacion:
                deuda += (venta.totalPagar-venta.totalPagado)
        deuda_clientes[cliente.identificacion] = deuda
    
    if obj.get_boolean() is True:
        return render_template('index.html',productos_bajo_stock=productos_bajo_stock, clientes_con_deuda=clientes_con_deuda, deuda_clientes=deuda_clientes)
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
    costo = float(request.form['costo'].replace('$', '').replace('.',''))
    precio = float(request.form['precio'].replace('$', '').replace('.',''))
    
    # Crear un nuevo objeto Producto con los datos recibidos
    nuevo_producto = Producto(tipo=tipo, referencia=referencia, cantidad=cantidad, costo=costo, precio=precio)
    
    # Guardar el nuevo producto en la base de datos
    session.add(nuevo_producto)
    session.commit()
    
    # Redirigir a la página de productos después de guardar el producto
    return redirect(url_for('productos'))

def editar_productos(idProducto):
    producto=session.query(Producto).filter_by(idProducto=idProducto).first()
    productos = session.query(Producto).all()
    return render_template('productos.html', producto=producto, productos=productos)


def modificar_productos(idProducto):
    tipo = request.form['tipo']
    referencia = request.form['referencia']
    cantidad = int(request.form['cantidad'])
    costo = float(request.form['costo'].replace('$', '').replace('.',''))
    precio = float(request.form['precio'].replace('$', '').replace('.',''))

    producto = session.query(Producto).get(idProducto)

    producto.tipo = tipo
    producto.referencia = referencia
    producto.cantidad = cantidad
    producto.costo = costo
    producto.precio = precio

    session.commit()
    return redirect(url_for('productos'))

def eliminar_productos(idProducto):
    producto = session.query(Producto).get(idProducto)
    session.delete(producto)
    session.commit()
    return redirect(url_for('productos'))
