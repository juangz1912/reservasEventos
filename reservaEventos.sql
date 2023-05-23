create schema reservaEventos;

use reservaEventos;

CREATE TABLE reservas (
  id INT PRIMARY KEY,
  event_name VARCHAR(255) NOT NULL,
  date INT NOT NULL,
  time INT NOT NULL,
  attendees INT NOT NULL
);

CREATE TABLE lugares (
  id varchar(25) PRIMARY KEY,
  direccion VARCHAR(255) NOT NULL,
  tipo_lugar varchar(255) NOT NULL
);

CREATE TABLE usuarios (
  id_usuario varchar(25) PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  correo VARCHAr(255) NOT NULL,
  numero varchar(255) NOT NULL
);
