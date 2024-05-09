from flask import Flask
from src.controllers import controller, controllerVenta, controllerCliente
from src.models.model import *



app = Flask(__name__)
app.config['SECRET_KEY']='security key momently'


# RUTAS PARA INICIO DE SESIÓN
@app.route('/')
def inicio():
    return controller.login()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return controller.login()

@app.route('/inicio')
def index():
    return controller.index()

# RUTAS PARA LOS PRODUCTOS
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    return controller.productos("")

def formatear_moneda(valor):
    formato = "{:,.0f}".format(valor)
    result = formato.replace(',','.')
    return f'$ {result}'

# Registrar el filtro personalizado para formatear como moneda
@app.template_filter('moneda')
def moneda_colombiana_filter(valor):
    return formatear_moneda(valor)


# RUTAS DE PRODUCTOS
@app.route('/registrar_productos', methods=['POST'])
def registrar_productos():
    return controller.registrar_productos()
@app.route('/editar_productos/<idProducto>', methods=['GET'])
def editar_productos(idProducto):
    return controller.editar_productos(idProducto)

@app.route('/modificar_productos/<idProducto>', methods=['POST', 'GET'])
def modificar_productos(idProducto):
    return controller.modificar_productos(idProducto)

@app.route('/eliminar_productos/<idProducto>', methods=['GET'])
def eliminar_productos(idProducto):
    return controller.eliminar_productos(idProducto)

# RUTAS PARA VENTAS
@app.route('/ventas')
def ventas():
    return controllerVenta.ventas()

@app.route('/venta-nueva')
def nuevaVenta():
    return controllerVenta.nuevaVenta()


@app.route('/registra_venta', methods=['POST'])
def registraVenta():
    return controllerVenta.registrarVenta()

# RUTAS DE CLIENTES
@app.route('/clientes')
def clientes():
    return controllerCliente.listarCliente()

@app.route('/cliente', methods=['POST'])
def registraCliente():
    return controllerVenta.registraCliente()

@app.route('/eliminar_cliente/<id>')
def eliminarCliente(id):
    return controllerCliente.eliminar_cliente(id)

@app.route('/modificar_cliente/<id>', methods=['POST'])
def modificarCliente(id):
    return controllerCliente.modificar_cliente(id)

# RUTA PARA ABONOS
@app.route('/abono', methods=['POST'])
def abono():
    return controllerVenta.registroAbono()

# RUTAS EXTRA
@app.route('/finanzas/<fi>/<ff>/<gb>')
def finanza(fi, ff, gb):
    return controller.finanzas(fi, ff, gb)

if __name__ == '__main__':
    app.run(debug=True)