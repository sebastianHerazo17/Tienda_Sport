from flask import  Flask, render_template, request, redirect, url_for, jsonify
from flask import session
from src.models.model import *
import datetime

def queryCliente():
    clientes = session.query(Cliente).all()
    json_clientes = [{
        "identificacion": cliente.identificacion,
        "nombre": cliente.nombre,
        "celular": cliente.celular
    }
    for cliente in clientes
    ]

    return json_clientes

def queryProducto():
    productos = session.query(Producto).all()
    json_productos = [{
        "idProducto": producto.idProducto,
        "tipo": producto.tipo,
        "referencia": producto.referencia,
        "cantidad": producto.cantidad,
        "precio": producto.precio
    } 
    for producto in productos
    ]

    return json_productos

def ventas():
    productos = queryProducto()
    clientes = queryCliente()
    return render_template('ventas.html', productos=productos, clientes=clientes)

def registraCliente():
    datos = request.get_json()
    # Procesar datos
    nombre = datos.get('nombre')
    celular = datos.get('celular')

    nuevoCliente = Cliente(nombre=nombre, celular=celular)

    session.add(nuevoCliente)
    session.commit()

    clientes = queryCliente()

    # Devolver respuesta como JSON
    return jsonify(clientes)

def registroVenta(datos):
    identificacion = int(datos.get('identificacion'))
    tipoPago = datos.get('tipoPago')
    hoy = datetime.date.today()
    fecha = hoy.strftime('%Y-%m-%d')
    totalPagar = 0
    totalPagado = float(datos.get('totalPagado'))
    carrito = datos.get('carrito')
    for p in carrito:
        totalPagar += (p['precio']*p['orden']) - p['descuento']

    nuevaVenta = Venta(
        identificacion=identificacion, 
        tipoPago=tipoPago,
        fecha=fecha, 
        totalPagar=totalPagar, 
        totalPagado=totalPagado
        )
    
    session.add(nuevaVenta)
    session.commit()
    id = nuevaVenta.idVenta

    for producto in carrito:
        idProducto = producto['idProducto']
        orden = producto['orden']
        descuento = producto['descuento']
        nuevaCompra = ProductosVentas(idProducto=idProducto, 
                    idVenta=id, 
                    cantidad=orden, 
                    descuento=descuento
                    )
        session.add(nuevaCompra)
        session.commit()
        
        productoMod = session.query(Producto).get(idProducto)
        productoMod.cantidad = productoMod.cantidad - orden
        session.commit()
    return nuevaVenta
    
def registrarVenta():
    datos = request.get_json()
    identificacion = int(datos.get('identificacion'))
    tipoPago = datos.get('tipoPago')
    totalPagar = 0
    totalPagado = float(datos.get('totalPagado'))
    carrito = datos.get('carrito')
    for p in carrito:
        totalPagar += (p['precio']*p['orden']) - p['descuento']
   
    if (tipoPago == "De contado"):
        if (totalPagado >= totalPagar):
            registroVenta(datos=datos)
            return jsonify("correct")
        else:
            return jsonify("pagoCero")
    elif (tipoPago == "Fiado"):
        if (identificacion > 1):
            registroVenta(datos=datos)
            return jsonify("correct")
        else:
            return jsonify("clienteInvalido")
    else:
        return jsonify("TipoPagoInvalido")
    