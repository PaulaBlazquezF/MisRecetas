from flask import Flask, jsonify, render_template, request, url_for
import requests, random
import pandas as pd
from conexionBD import conectar_bd
from datetime import datetime
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Función para insertar una receta en la base de datos
def insertar_receta(titulo, fecha, tiempo, ingredientes, preparacion):
    try:
        # Conectar a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # Verificar si algún campo está vacío
        if not all([titulo, fecha, tiempo, ingredientes, preparacion]):
            raise ValueError("Todos los campos son obligatorios")
        
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Formato de fecha incorrecto. Utiliza el formato YYYY-MM-DD")

        # Query SQL para insertar la receta en la tabla 'recetas'
        sql = "INSERT INTO recetas (titulo, fecha, tiempo, ingredientes, preparacion) VALUES (%s, %s, %s, %s, %s)"
        valores = (titulo, fecha, tiempo, ingredientes, preparacion)

        # Ejecutar la consulta SQL
        cursor.execute(sql, valores)
        
        # Confirmar los cambios en la base de datos
        conexion.commit()
        
        # Cerrar la conexión
        cursor.close()
        conexion.close()

        return True, "Receta guardada correctamente"
    
    except Exception as e:
        return False, str(e)
    
# Función para insertar un nuevo usuario en la base de datos
def insertar_usuario(nombre, email, password):
    try:
        # Conectar a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # Verificar si algún campo está vacío
        if not all([nombre, email, password]):
            raise ValueError("Todos los campos son obligatorios")
        
        # Query SQL para insertar el usuario en la tabla 'usuarios'
        sql = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
        valores = (nombre, email, password)

        # Ejecutar la consulta SQL
        cursor.execute(sql, valores)
        
        # Confirmar los cambios en la base de datos
        conexion.commit()
        
        # Cerrar la conexión
        cursor.close()
        conexion.close()

        return True, "Usuario creado correctamente"
    
    except Exception as e:
        return False, str(e)


# Función para autenticar un usuario
def autenticar_usuario(email, password):
    try:
        # Conectar a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # Consultar la base de datos para encontrar el usuario por su correo electrónico
        sql = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        usuario = cursor.fetchone()

        if usuario:
            # Si se encontró el usuario, verificar la contraseña
            if check_password_hash(usuario['contrasena'], password):
                # Contraseña correcta, autenticación exitosa
                return True, "Autenticación exitosa"
            else:
                # Contraseña incorrecta
                return False, "Contraseña incorrecta"
        else:
            # Usuario no encontrado
            return False, "Usuario no encontrado"

    except Exception as e:
        # Manejar cualquier error de base de datos
        return False, str(e)

def buscar_recetas(receta):
    try:
        # Conectar a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # Query SQL para buscar recetas que coincidan con el término de búsqueda en el título
        sql = "SELECT * FROM recetas WHERE titulo LIKE %s"
        cursor.execute(sql, receta)
        recetas = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        conexion.close()

        return True, recetas  # Retorna éxito y las recetas encontradas

    except Exception as e:
        return False, str(e)  # Retorna False y el mensaje de error si hay algún problema


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/notebook')
def notebook():
    return render_template('notebook.html')

@app.route('/ideas')
def ideas():
    return render_template('ideas.html')

@app.route('/guardar_receta', methods=['POST'])
def guardar_receta():
    # Obtener los datos del formulario
    titulo = request.form.get('titulo')
    fecha = request.form.get('fecha')
    tiempo = request.form.get('tiempo')
    ingredientes = request.form.get('ingredientes')
    preparacion = request.form.get('preparacion')

    # Insertar la receta en la base de datos
    exito, mensaje = insertar_receta(titulo, fecha, tiempo, ingredientes, preparacion)

    # Retornar un mensaje de éxito o error al cliente
    return render_template('notebook.html', mensaje = mensaje)


@app.route('/buscar_receta', methods=['POST'])
def buscar_receta():
    # Obtener los datos del formulario
    receta = request.form.get('receta')
    
    exito, recetas = buscar_recetas(receta)
    
    if exito:
        # Si la búsqueda fue exitosa, mostrar los resultados
        return render_template('notebook.html', recetas=recetas)
    else:
        # Si ocurrió un error, mostrar un mensaje de error
        return render_template('notebook.html', mensaje="Error al buscar receta")

@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para el formulario de creación de usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    # Obtener los datos del formulario
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')

    # Insertar el usuario en la base de datos
    exito, mensaje = insertar_usuario(nombre, email, password)
    # Redireccionar dependiendo del resultado de la inserción
    if exito:
        return render_template('index.html')
    else:
        return render_template('login.html', mensaje_registro=mensaje)
    
# Ruta para la autenticación de usuario
@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    # Obtener los datos del formulario
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Autenticar al usuario
    exito, mensaje = autenticar_usuario(email, password)

    if exito:
        # Autenticación exitosa, redirigir al usuario a la página de inicio
        return render_template('index.html')
    else:
        # Autenticación fallida, redirigir al usuario a la página de inicio de sesión con un mensaje de error
        return render_template('login.html', mensaje_login=mensaje)

@app.route('/api')
def api():  

    platos = [
    "Spaghetti",
    "Chicken soup",
    "Sushi",
    "Hamburger",
    "Pizza",
    "Pad Thai",
    "Lasagna",
    "Fried Rice",
    "Steak",
    "Caesar Salad",
    "Tacos",
    "Chicken Alfredo",
    "Ramen",
    "Fish and Chips",
    "Miso Soup",
    "Sashimi",
    "Curry",
    "Chili",
    "Gyoza",
    "Paella",
    "Beef Wellington",
    "Burrito",
    "Fajitas",
    "Peking Duck",
    "Chicken Parmesan",
    "Ceviche",
    "Eggs",
    "Hot Dog",
    "Tuna Salad",
    "Moussaka",
    "Crepes",
    "Guacamole",
    "Ratatouille",
    "Cheesecake",
    "Tiramisu",
    "Apple pie"
    ]

    platos_random = random.choice(platos)

    url = "https://food-recipes-with-images.p.rapidapi.com/"
    querystring = {"q": platos_random }
    headers = {
        "X-RapidAPI-Key": "1361a3ebc7msha64a0577179ec90p1e29fdjsn6968b972f711",
        "X-RapidAPI-Host": "food-recipes-with-images.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    # Si la solicitud fue exitosa (código de estado 200), retornamos la respuesta JSON
    if response.status_code == 200:
        datos = response.json()['d']
        primeros_cinco = datos[:5]
        return render_template('ideas.html', platos = primeros_cinco)
    else:
        # Si la solicitud falla, retornamos un mensaje de error
        return ("error en la solicitud de la API")


if __name__ == '__main__':

    app.run(debug=True)


    