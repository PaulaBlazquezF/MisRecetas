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

-- Crea la tabla de recetas
CREATE TABLE IF NOT EXISTS recetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    fecha DATE,
    tiempo TEXT,
    ingredientes TEXT,
    preparacion TEXT
);
