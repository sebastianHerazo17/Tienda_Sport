from flask import  Flask, render_template, request, redirect, url_for, jsonify
from flask import session
from src.models.model import *
import datetime
from src.controllers.controller import obj

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
    if obj.get_boolean() is True:
        ventas = session.query(Venta).all()
        listaCli = session.query(Cliente).all()
        nombres = {}
        for venta in ventas:
            nombre = ""
            if(venta.identificacion == 1):
                nombre = "Venta en caja"
            else:
                for cli in listaCli:
                    if(venta.identificacion == cli.identificacion):
                        nombre = cli.nombre
            nombres[venta.identificacion] = nombre

        
        return render_template('ventas.html', ventas=ventas, nombres=nombres)
    else:
        return redirect(url_for('login'))

def nuevaVenta():
    if obj.get_boolean() is True:
        productos = queryProducto()
        clientes = queryCliente()
        return render_template('registroVenta.html',  productos=productos, clientes=clientes)
    else:
        return redirect(url_for('login'))
    
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
    fecha =  hoy.strftime('%Y-%m-%d')
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
    
def registrarVenta():
    datos = request.get_json()
    identificacion = int(datos.get('identificacion'))
    tipoPago = datos.get('tipoPago')
    totalPagar = 0
    totalPagado = float(datos.get('totalPagado'))
    carrito = datos.get('carrito')
    for p in carrito:
        totalPagar += (p['precio']*p['orden']) - p['descuento']
    if len(carrito) > 0:
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
    else:
        return jsonify("vacio")
    

    # REGISTRO DE ABONO

def registroAbono():
    datos = request.get_json()
    idVenta = datos.get('idVenta')
    hoy = datetime.date.today()
    fecha =  hoy.strftime('%Y-%m-%d')
    valor = datos.get('valor')

    nuevoAbono = Abono(idVenta=idVenta, fecha=fecha, valor=valor)
    session.add(nuevoAbono)
    session.commit()

    venta = session.query(Venta).get(idVenta)
    venta.totalPagado += valor
    session.commit()

    return jsonify('registrado')


# Esto es lo que vas a agregar
def egresos():
    egresos = session.query(Egresos).all()
    if obj.get_boolean() is True:
        return render_template('egresos.html', egresos=egresos)
    else: 
        return redirect(url_for('login'))
    
def eliminar_egresos(idEgresos):
    egresos_ = session.query(Egresos).get(idEgresos)
    if egresos_: 
        egre = session.query(Egresos).get(idEgresos)
        session.delete(egre)
        session.commit()
        return egresos()
    
def registro_egreso():
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    valor = float(request.form['monto'].replace('$', '').replace('.',''))

    nuevo_egreso = Egresos(descripcion=descripcion, fecha=fecha, valor=valor)
    session.add(nuevo_egreso)
    session.commit()
    return redirect(url_for('egresos'))