from flask import render_template, request, redirect, jsonify, url_for, send_file
from sqlalchemy import desc
from src.models.model import Venta, Producto, ProductosVentas, Cliente, Abono, Egresos, session
import datetime
from src.controllers.controller import obj
from openpyxl import Workbook

def queryCliente():
    try:
        clientes = session.query(Cliente).all()
        json_clientes = [{
            "identificacion": cliente.identificacion,
            "nombre": cliente.nombre,
            "celular": cliente.celular
        } for cliente in clientes]
        return json_clientes
    except Exception as e:
        error = f"Ocurrió un error en queryCliente: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def queryProducto():
    try:
        productos = session.query(Producto).all()
        json_productos = [{
            "idProducto": producto.idProducto,
            "tipo": producto.tipo,
            "referencia": producto.referencia,
            "cantidad": producto.cantidad,
            "precio": producto.precio
        } for producto in productos]
        return json_productos
    except Exception as e:
        error = f"Ocurrió un error en queryProducto: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def ventas():
    try:
        if obj.get_boolean() is True:
            ventas = session.query(Venta).order_by(desc(Venta.idVenta)).all()
            listaCli = session.query(Cliente).all()
            nombres = {}
            for venta in ventas:
                nombre = ""
                if venta.identificacion == 1:
                    nombre = "Venta en caja"
                else:
                    for cli in listaCli:
                        if venta.identificacion == cli.identificacion:
                            nombre = cli.nombre
                nombres[venta.identificacion] = nombre
            return render_template('ventas.html', ventas=ventas, nombres=nombres)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        error = f"Ocurrió un error en ventas: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def nuevaVenta():
    try:
        if obj.get_boolean() is True:
            productos = queryProducto()
            clientes = queryCliente()
            return render_template('registroVenta.html', productos=productos, clientes=clientes)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        error = f"Ocurrió un error en nuevaVenta: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def registraCliente():
    try:
        datos = request.get_json()
        nombre = datos.get('nombre')
        celular = datos.get('celular')

        nuevoCliente = Cliente(nombre=nombre, celular=celular)
        session.add(nuevoCliente)
        session.commit()

        clientes = queryCliente()
        return jsonify(clientes)
    except Exception as e:
        error = f"Ocurrió un error en registraCliente: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def registroVenta(datos):
    try:
        identificacion = int(datos.get('identificacion'))
        tipoPago = datos.get('tipoPago')
        hoy = datetime.date.today()
        fecha = hoy.strftime('%Y-%m-%d')
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
            nuevaCompra = ProductosVentas(
                idProducto=idProducto, 
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
    except Exception as e:
        error = f"Ocurrió un error en registroVenta: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def registrarVenta():
    try:
        datos = request.get_json()
        identificacion = int(datos.get('identificacion'))
        tipoPago = datos.get('tipoPago')
        totalPagar = 0
        totalPagado = float(datos.get('totalPagado'))
        carrito = datos.get('carrito')
        for p in carrito:
            totalPagar += (p['precio'] - p['descuento'])
        if len(carrito) > 0:
            if tipoPago == "De contado":
                if totalPagado >= totalPagar:
                    id = registroVenta(datos=datos)
                    return jsonify({"status": 'correct', 'id': id})
                else:
                    return jsonify("pagoCero")
            elif tipoPago == "Fiado":
                if identificacion > 1:
                    id = registroVenta(datos=datos)
                    return jsonify({"status": 'correct', 'id': id})
                else:
                    return jsonify({"status": 'clienteInvalido'})
            else:
                return jsonify({"status": 'TipoPagoInvalido'})
        else:
            return jsonify({"status": 'vacio'})
    except Exception as e:
        error = f"Ocurrió un error en registrarVenta: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def registroAbono():
    try:
        datos = request.get_json()
        idVenta = datos.get('idVenta')
        hoy = datetime.date.today()
        fecha = hoy.strftime('%Y-%m-%d')
        valor = datos.get('valor')

        nuevoAbono = Abono(idVenta=idVenta, fecha=fecha, valor=valor)
        session.add(nuevoAbono)
        session.commit()

        venta = session.query(Venta).get(idVenta)
        venta.totalPagado += valor
        session.commit()

        return jsonify('registrado')
    except Exception as e:
        error = f"Ocurrió un error en registroAbono: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def generar_excel():
    try:
        resultados = session.query(Cliente, Venta, ProductosVentas, Producto).\
        select_from(Cliente).\
        join(Venta, Venta.identificacion == Cliente.identificacion).\
        join(ProductosVentas, ProductosVentas.idVenta == Venta.idVenta).\
        join(Producto, Producto.idProducto == ProductosVentas.idProducto).\
        order_by(desc(Venta.idVenta)).\
        all()

        wb = Workbook()
        ws = wb.active
        ws.title = "Información Ventas"

        ws.append(["Nombre Cliente", "Celular", "ID Venta", "Tipo Pago", "Fecha", "Total Pagar", "Total Pagado",
                   "ID Producto", "Tipo Producto", "Referencia", "Cantidad Vendida", "Total Precio", "Descuento"])

        for cliente, venta, producto_venta, producto in resultados:
            if cliente.identificacion == 1:
                cliente.nombre = "Venta en caja"
            if cliente.celular == "" or cliente.identificacion == 1:
                cliente.celular = "N/A"
            ws.append([cliente.nombre, cliente.celular, f"TS00{venta.idVenta}", venta.tipoPago, venta.fecha,
                       venta.totalPagar, venta.totalPagado, f"PTS00{producto.idProducto}", producto.tipo, producto.referencia,
                       producto_venta.cantidad, producto_venta.precio, producto_venta.descuento])

        wb.save("informacion_ventas.xlsx")
        return send_file("informacion_ventas.xlsx", as_attachment=True)
    except Exception as e:
        error = f"Ocurrió un error en generar_excel: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def factura_venta(idVenta):
    try:
        venta = session.query(Venta).get(idVenta)
        abonos = []
        if venta.tipoPago == "Fiado":
            abonos = session.query(Abono).filter_by(idVenta=idVenta).all()
        cliente = session.query(Cliente).get(venta.identificacion)
        productosVendidos = session.query(ProductosVentas, Producto).\
        select_from(ProductosVentas).\
        filter_by(idVenta=idVenta).\
        join(Producto, Producto.idProducto == ProductosVentas.idProducto).\
        all()

        return render_template('factura.html', venta=venta, cliente=cliente, productosVendidos=productosVendidos, abonos=abonos)
    except Exception as e:
        error = f"Ocurrió un error en factura_venta: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def egresos():
    try:
        egresos = session.query(Egresos).all()
        if obj.get_boolean() is True:
            return render_template('egresos.html', egresos=egresos)
        else: 
            return redirect(url_for('login'))
    except Exception as e:
        error = f"Ocurrió un error en egresos: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def eliminar_egresos(idEgresos):
    try:
        egresos_ = session.query(Egresos).get(idEgresos)
        if egresos_:
            session.delete(egresos_)
            session.commit()
            return egresos()
        else:
            return redirect(url_for('egresos'))
    except Exception as e:
        error = f"Ocurrió un error en eliminar_egresos: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()

def registro_egreso():
    try:
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        valor = float(request.form['monto'].replace('$', '').replace('.',''))

        nuevo_egreso = Egresos(descripcion=descripcion, fecha=fecha, valor=valor)
        session.add(nuevo_egreso)
        session.commit()
        return redirect(url_for('egresos'))
    except Exception as e:
        error = f"Ocurrió un error en registro_egreso: {e}"
        return render_template('error.html', error=error)
    finally:
        session.close()