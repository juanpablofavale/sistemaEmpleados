CREATE SCHEMA `sistemaempleados` ;

CREATE TABLE `sistemaempleados`.`empleados` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  `correo` VARCHAR(255) NULL,
  `foto` VARCHAR(5000) NULL,
  PRIMARY KEY (`id`));

select * from empleados;

insert into empleados (nombre, correo, foto) values ("mario", "mario@hotmail.com", "fotodemario.jpg");