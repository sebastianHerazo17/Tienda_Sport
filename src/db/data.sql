-- drop database if exists tienda;
CREATE database IF NOT exists tienda;

use tienda;

CREATE TABLE Producto (
  idProducto INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  tipo VARCHAR(30)  NOT NULL  ,
  referencia VARCHAR(30)  NOT NULL  ,
  cantidad INTEGER UNSIGNED  NOT NULL  ,
  costo DOUBLE  NOT NULL  ,
  precio DOUBLE  NOT NULL    ,
PRIMARY KEY(idProducto));



CREATE TABLE Usuarios (
  idUsuario INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  usuario VARCHAR(20)  NULL  ,
  contraseña VARCHAR(100)  NULL    ,
PRIMARY KEY(idUsuario));



CREATE TABLE Egresos (
  idEgresos INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  descripcion VARCHAR(100)  NULL  ,
  fecha DATE  NULL  ,
  valor DOUBLE  NULL    ,
PRIMARY KEY(idEgresos));



CREATE TABLE Cliente (
  identificacion INTEGER UNSIGNED  NOT NULL  ,
  nombre VARCHAR(40)  NOT NULL  ,
  celular VARCHAR(10)  NOT NULL    ,
PRIMARY KEY(identificacion));



CREATE TABLE Venta (
  idVenta INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  identificacion INTEGER UNSIGNED  NOT NULL  ,
  idUsuario INTEGER UNSIGNED  NOT NULL  ,
  tipoPago VARCHAR(20)  NOT NULL  ,
  fecha DATE  NOT NULL  ,
  totalPagar DOUBLE  NOT NULL  ,
  totalPagado DOUBLE  NOT NULL    ,
PRIMARY KEY(idVenta)  ,
INDEX Venta_FKIndex1(identificacion)  ,
INDEX Venta_FKIndex2(idUsuario),
  FOREIGN KEY(identificacion)
    REFERENCES Cliente(identificacion)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(idUsuario)
    REFERENCES Usuarios(idUsuario)
      ON DELETE RESTRICT
      ON UPDATE CASCADE);



CREATE TABLE ProductosVentas (
  idProducto INTEGER UNSIGNED  NOT NULL  ,
  idVenta INTEGER UNSIGNED  NOT NULL  ,
  descuento DOUBLE  NOT NULL    ,
PRIMARY KEY(idProducto, idVenta)  ,
INDEX Producto_has_Venta_FKIndex1(idProducto)  ,
INDEX Producto_has_Venta_FKIndex2(idVenta),
  FOREIGN KEY(idProducto)
    REFERENCES Producto(idProducto)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(idVenta)
    REFERENCES Venta(idVenta)
      ON DELETE RESTRICT
      ON UPDATE CASCADE);



CREATE TABLE Abono (
  idAbonos INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  idVenta INTEGER UNSIGNED  NOT NULL  ,
  fecha DATE  NULL  ,
  valor DOUBLE  NULL    ,
PRIMARY KEY(idAbonos)  ,
INDEX Abonos_FKIndex2(idVenta),
  FOREIGN KEY(idVenta)
    REFERENCES Venta(idVenta)
      ON DELETE RESTRICT
      ON UPDATE CASCADE);


INSERT INTO Producto (tipo, referencia, cantidad, costo, precio) VALUES 
('Electrodoméstico', 'Lavadora LG', 10, 500.00, 700.00),
('Electrónica', 'Smartphone Samsung', 20, 300.00, 400.00),
('Electrodoméstico', 'Refrigerador Whirlpool', 15, 800.00, 1000.00),
('Electrónica', 'Laptop HP', 30, 600.00, 800.00),
('Mueble', 'Sofá de tres puestos', 8, 400.00, 600.00);

INSERT INTO Usuarios (usuario, contraseña) VALUES 
('admin', 'admin123'),
('sebas12', 'herazo17'),
('empleado2', 'pass456'),
('empleado3', 'pass789'),
('gerente', 'gerente123');

INSERT INTO Egresos (descripcion, fecha, valor) VALUES 
('Pago de servicios', '2024-04-10', 500.00),
('Compra de inventario', '2024-04-08', 1000.00),
('Pago de nómina', '2024-04-05', 1500.00),
('Gastos administrativos', '2024-04-03', 700.00),
('Mantenimiento de local', '2024-04-01', 300.00);

INSERT INTO Cliente (identificacion, nombre, celular) VALUES 
(1001, 'Juan Pérez', '3123456789'),
(1002, 'María Gómez', '3219876543'),
(1003, 'Carlos Ramírez', '3001234567'),
(1004, 'Laura Martínez', '3109876543'),
(1005, 'Luis Rodríguez', '3158765432');


INSERT INTO Venta (identificacion, idUsuario, tipoPago, fecha, totalPagar, totalPagado) VALUES 
(1001, 1, 'Efectivo', '2024-04-10', 800.00, 800.00),
(1002, 2, 'Tarjeta de crédito', '2024-04-09', 1200.00, 1200.00),
(1003, 3, 'Efectivo', '2024-04-08', 1500.00, 1500.00),
(1004, 4, 'Transferencia bancaria', '2024-04-07', 2000.00, 2000.00),
(1005, 5, 'Efectivo', '2024-04-06', 1000.00, 1000.00);


ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';