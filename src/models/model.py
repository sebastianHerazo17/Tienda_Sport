from sqlalchemy import create_engine, Column, Integer, String, Boolean, Double, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear una instancia de la clase Base de SQLAlchemy
Base = declarative_base()

# Definir la clase Producto que representa la tabla de productos en la base de datos
class Producto(Base):
    __tablename__ = 'Producto'
    __tablename__ = 'Producto'

    idProducto = Column(Integer, primary_key=True)
    tipo = Column(String)
    referencia = Column(String)
    cantidad = Column(Integer)
    costo = Column(Double)
    precio = Column(Double)

class Usuario(Base):
    __tablename__ = 'Usuario'
    __tablename__ = 'Usuario'

    idUsuario = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)
    contraseña = Column(String(100), nullable=False)

class Cliente(Base):
    __tablename__ = 'Cliente'
    
    identificacion = Column(Integer, primary_key=True)
    nombre = Column(String)
    celular = Column(String)

class Venta(Base):
    __tablename__ = 'Venta'

    idVenta = Column(Integer, primary_key=True)
    identificacion = Column(Integer)
    tipoPago = Column(String)
    fecha = Column(Date)
    totalPagar = Column(Double)
    totalPagado = Column(Double)

class ProductosVentas(Base):
    __tablename__ = 'ProductosVentas'
     
    idProducto = Column(Integer, primary_key=True)
    idVenta = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    descuento = Column(Double)

class Abono(Base):
    __tablename__ = 'Abono'

    idAbonos = Column(Integer, primary_key=True)
    idVenta = Column(Integer)
    fecha = Column(Date)
    valor = Column(Double)



# Crear el motor de la base de datos (usando MySQL)
engine = create_engine('mysql://root:@localhost/tienda')

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()


