import mysql.connector

def conectar_bd():
    # Configuración de la conexión a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Paulita2",
        database="misRecetas"
    )
    return conexion
