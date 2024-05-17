-- Crea la base de datos misRecetas si no existe
CREATE DATABASE IF NOT EXISTS misRecetas;

-- Usa la base de datos misRecetas
USE misRecetas;

-- Crea la tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);

INSERT INTO `usuarios` (`id`, `nombre`,`email`, `password`) VALUES
(1, 'albert', 'wew@wwe.com','admin'),
(2, 'paula', 'Paulablazquez@gmail.com' ,'1234');

-- Crea la tabla de recetas
CREATE TABLE IF NOT EXISTS recetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    fecha text,
    tiempo TEXT,
    ingredientes TEXT,
    preparacion TEXT
);


INSERT INTO `recetas` (`id`, `titulo`,`fecha`, `tiempo`,`ingredientes`, `preparacion` ) VALUES
(1, 'Carbonara', '2000-05-17','30min', 'huevo, pasta, sal, pimienta, parmesano', 'hervir la pasta, batir una yema de huevo, rallar el queso, salpimentar'),
(2, 'Guisantes con jamon', '2000-05-17' ,'1h', 'guisantes, jamon a trozos', 'hervir los guisantes, freir el jamon, juntar todo');


