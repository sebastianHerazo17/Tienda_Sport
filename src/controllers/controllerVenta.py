from flask import render_template, request, redirect, jsonify, url_for, send_file
from sqlalchemy import desc
from src.models.model import Venta, Producto, ProductosVentas, Cliente, Abono, Egresos, session
import datetime
from src.controllers.controller import obj
from openpyxl import Workbook


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
        ventas = session.query(Venta).order_by(desc(Venta.idVenta)).all()
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
        totalPagar += (p['precio'] - p['descuento'])

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
        precio = producto['precio']
        descuento = producto['descuento']
        nuevaCompra = ProductosVentas(idProducto=idProducto, 
                    idVenta=id, 
                    cantidad=orden,
                    precio=precio,
                    descuento=descuento
                    )
        session.add(nuevaCompra)
        session.commit()
        
        productoMod = session.query(Producto).get(idProducto)
        productoMod.cantidad = productoMod.cantidad - orden
        session.commit()
    return id
def registrarVenta():
    datos = request.get_json()
    identificacion = int(datos.get('identificacion'))
    tipoPago = datos.get('tipoPago')
    totalPagar = 0
    totalPagado = float(datos.get('totalPagado'))
    carrito = datos.get('carrito')
    for p in carrito:
        totalPagar += (p['precio'] - p['descuento'])
    if len(carrito) > 0:
        if (tipoPago == "De contado"):
            if (totalPagado >= totalPagar):
                id = registroVenta(datos=datos)
                return jsonify({
                    "status": 'correct', 
                    'id': id 
                    })
            else:
                return jsonify("pagoCero")
        elif (tipoPago == "Fiado"):
            if (identificacion > 1):
                id = registroVenta(datos=datos)
                return jsonify({
                    "status": 'correct', 
                    'id': id 
                    })
            else:
                return jsonify({
                    "status": 'clienteInvalido'
                    })
        else:
            return jsonify({
                    "status": 'TipoPagoInvalido'
                    })
    else:
        return jsonify({
                    "status": 'vacio'
                    })
    

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

# Exportar Ventas
def generar_excel():
    resultados = session.query(Cliente, Venta, ProductosVentas, Producto).\
    select_from(Cliente).\
    join(Venta, Venta.identificacion == Cliente.identificacion).\
    join(ProductosVentas, ProductosVentas.idVenta == Venta.idVenta).\
    join(Producto, Producto.idProducto == ProductosVentas.idProducto).\
    order_by(desc(Venta.idVenta)).\
    all()
    session.close()
    # Crea un libro de Excel y una hoja
    wb = Workbook()
    ws = wb.active
    ws.title = "Información Ventas"

    # Escribe los encabezados de las columnas
    ws.append(["Nombre Cliente", "Celular", "ID Venta", "Tipo Pago", "Fecha", "Total Pagar", "Total Pagado",
               "ID Producto", "Tipo Producto", "Referencia", "Cantidad Vendida", "Total Precio", "Descuento"])
    
    # Escribe los datos de cada venta en el archivo Excel
    for cliente, venta, producto_venta, producto in resultados:
        if cliente.identificacion == 1:
            cliente.nombre = "Venta en caja"
        if cliente.celular == "" or cliente.identificacion == 1:
            cliente.celular = "N/A"
        ws.append([cliente.nombre, cliente.celular, f"TS00{venta.idVenta}", venta.tipoPago, venta.fecha,
                   venta.totalPagar, venta.totalPagado, f"PTS00{producto.idProducto}", producto.tipo, producto.referencia,
                   producto_venta.cantidad, producto_venta.precio, producto_venta.descuento])

    # Guarda el archivo Excel en el sistema de archivos
    wb.save("informacion_ventas.xlsx")

    return send_file("informacion_ventas.xlsx", as_attachment=True)

# FACTURA DE VENTA 
def factura_venta(idVenta):
    venta =  session.query(Venta).get(idVenta)
    abonos = []
    if venta.tipoPago == "Fiado":
        abonos =  session.query(Abono).filter_by(idVenta=idVenta).all()
    cliente = session.query(Cliente).get(venta.identificacion)
    productosVendidos = session.query(ProductosVentas, Producto).\
    select_from(ProductosVentas).\
    filter_by(idVenta=idVenta).\
    join(Producto, Producto.idProducto == ProductosVentas.idProducto).\
    all()
    session.close()
    # ids_productos = [prod.idProducto for prod in productosVendidos]
    # productos = session.query(Producto).filter(Producto.idProducto.in_(ids_productos)).all()

    return render_template('factura.html', venta=venta, cliente=cliente, productosVendidos=productosVendidos, abonos=abonos)



# Egresos
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