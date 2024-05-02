from flask import render_template, redirect, url_for
from sqlalchemy import desc
from src.models.model import Cliente, Venta, session

def listarCliente():
    clientes = session.query(Cliente).order_by(desc(Cliente.identificacion)).all()
    size = len(clientes)
    return render_template('clientes.html', clientes=clientes, size=size)

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