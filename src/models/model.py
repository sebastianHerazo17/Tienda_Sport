from sqlalchemy import create_engine, Column, Integer, String, Double, Date, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear una instancia de la clase Base de SQLAlchemy
Base = declarative_base()

# Definir la clase Producto que representa la tabla de productos en la base de datos
class Producto(Base):
    __tablename__ = 'Producto'
    idProducto = Column(Integer, primary_key=True)
    tipo = Column(String(30), nullable=False)
    referencia = Column(String(30), nullable=False)
    cantidad = Column(Integer, nullable=False)
    costo = Column(Double, nullable=False)
    precio = Column(Double, nullable=False)

class Usuario(Base):
    __tablename__ = 'Usuario'
    __tablename__ = 'Usuario'

    idUsuario = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)
    contraseña = Column(String(100), nullable=False)

class Cliente(Base):
    __tablename__ = 'Cliente'
    identificacion = Column(Integer, primary_key=True)
    nombre = Column(String(40), nullable=False)
    celular = Column(String(10), nullable=False)

class Venta(Base):
    __tablename__ = 'Venta'
    idVenta = Column(Integer, primary_key=True)
    identificacion = Column(Integer, ForeignKey('Cliente.identificacion'), nullable=False)
    tipoPago = Column(String(20), nullable=False)
    fecha = Column(Date, nullable=False)
    totalPagar = Column(Double, nullable=False)
    totalPagado = Column(Double, nullable=False)
    cliente = relationship("Cliente")
    productos = relationship("ProductosVentas")

class ProductosVentas(Base):
    __tablename__ = 'ProductosVentas'
    idProducto = Column(Integer, ForeignKey('Producto.idProducto'), primary_key=True)
    idVenta = Column(Integer, ForeignKey('Venta.idVenta'), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Double, nullable=False)
    descuento = Column(Double, nullable=False)
    producto = relationship("Producto")
    venta = relationship("Venta")

class Abono(Base):
    __tablename__ = 'Abono'

    idAbonos = Column(Integer, primary_key=True)
    idVenta = Column(Integer)
    fecha = Column(Date)
    valor = Column(Double)

class Egresos(Base):
    __tablename__= 'Egresos'

    idEgresos = Column(Integer, primary_key=True)
    descripcion = Column(String)
    fecha = Column(Date)
    valor = Column(Double)

# Crear el motor de la base de datos (usando MySQL)
engine = create_engine('mysql://root:@localhost/tienda')
Base.metadata.create_all(engine)
# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()


