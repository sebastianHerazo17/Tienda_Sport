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



CREATE TABLE Usuario (
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
  identificacion INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  nombre VARCHAR(40)  NOT NULL  ,
  celular VARCHAR(10)  NOT NULL    ,
PRIMARY KEY(identificacion));

INSERT INTO Cliente(identificacion, nombre, celular) VALUES (0, 'Seleccionar Cliente', ' ');


CREATE TABLE Venta (
  idVenta INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  identificacion INTEGER UNSIGNED  NOT NULL  ,
  tipoPago VARCHAR(20)  NOT NULL  ,
  fecha DATE  NOT NULL  ,
  totalPagar DOUBLE  NOT NULL  ,
  totalPagado DOUBLE  NOT NULL    ,
PRIMARY KEY(idVenta)  ,
INDEX Venta_FKIndex1(identificacion)  ,
  FOREIGN KEY(identificacion)
    REFERENCES Cliente(identificacion)
      ON DELETE RESTRICT
      ON UPDATE CASCADE);
      

CREATE TABLE ProductosVentas (
  idProducto INTEGER UNSIGNED  NOT NULL  ,
  idVenta INTEGER UNSIGNED  NOT NULL  ,
  cantidad INTEGER UNSIGNED  NOT NULL  ,
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

-- select * from Producto;
-- DELETE FROM Producto WHERE idProducto IN (1, 2, 3, 4, 5, 6);



INSERT INTO Usuario (usuario, contraseña) VALUES 
('admin', 'admin123'),
('sebas12', 'herazo17');


select * FROM ProductosVentas;
select * from Venta;
select * from Producto;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'qwe.123';