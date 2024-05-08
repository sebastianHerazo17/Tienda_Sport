from flask import render_template, redirect, url_for, request, jsonify
from sqlalchemy import desc
from src.models.model import Cliente, Venta, session
from src.controllers.controller import obj

def listarCliente():
    if obj.get_boolean() is True:
        clientes = session.query(Cliente).order_by(desc(Cliente.identificacion)).all()
        size = len(clientes)
        return render_template('clientes.html', clientes=clientes, size=size)
    else:
        return redirect(url_for('login'))
    

def eliminar_cliente(id):
    cliente = session.query(Cliente).get(id)
    ventas =  session.query(Venta).filter_by(identificacion=id).all()
    i = 0
    for venta in ventas:
        venta.identificacion = 2
        ventas[i] = venta
        i += 1
    session.commit()
    session.delete(cliente)
    session.commit()
    return redirect(url_for('clientes'))

def modificar_cliente(id):
    datos = request.get_json()
    nombre = datos.get("nombre")
    celular = datos.get("celular")

    cliente = session.query(Cliente).get(id)
    cliente.nombre = nombre
    cliente.celular = celular
    session.commit()
    return jsonify('mod')