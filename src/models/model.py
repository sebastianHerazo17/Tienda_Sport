from sqlalchemy import create_engine, Column, Integer, String, Boolean, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear una instancia de la clase Base de SQLAlchemy
Base = declarative_base()

# Definir la clase Producto que representa la tabla de productos en la base de datos
class Producto(Base):
    __tablename__ = 'producto'

    idProducto = Column(Integer, primary_key=True)
    tipo = Column(String)
    referencia = Column(String)
    cantidad = Column(Integer)
    costo = Column(Double)
    precio = Column(Double)

class Usuario(Base):
    __tablename__ = 'usuarios'

    idUsuario = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)
    contraseña = Column(String(100), nullable=False)

    

# Crear el motor de la base de datos (usando MySQL)
engine = create_engine('mysql://root:@localhost/tienda')

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()
