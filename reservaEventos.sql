create schema reservaEventos;

use reservaEventos;


CREATE TABLE eventos (
  id varchar(25) PRIMARY KEY,
  event_name VARCHAR(255) NOT NULL,
  date INT NOT NULL,
  time INT NOT NULL,
  attendees INT NOT NULL
);

CREATE TABLE lugares (
  id_lugar varchar(25) PRIMARY KEY,
  direccion VARCHAR(255) NOT NULL,
  tipo_lugar varchar(255) NOT NULL
);

CREATE TABLE usuarios (
  id_usuario varchar(25) PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  correo VARCHAr(255) NOT NULL,
  numero varchar(255) NOT NULL
);

CREATE TABLE reservas (
  id_reserva INT AUTO_INCREMENT PRIMARY KEY,
  id_lugar VARCHAR(25) NOT NULL,
  id_evento VARCHAR(25) NOT NULL,
  id_usuario VARCHAR(25) NOT NULL,
  FOREIGN KEY (id_lugar) REFERENCES lugares(id_lugar),
  FOREIGN KEY (id_evento) REFERENCES eventos(id),
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);