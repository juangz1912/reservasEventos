create schema reservaEventos;

use reservaEventos;

CREATE TABLE reservas (
  id INT PRIMARY KEY,
  event_name VARCHAR(255) NOT NULL,
  date INT NOT NULL,
  time INT NOT NULL,
  attendees INT NOT NULL
);
