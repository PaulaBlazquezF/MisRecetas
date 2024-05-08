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

    #Si la solicitud fue exitosa (código de estado 200), retornamos la respuesta JSON
    if response.status_code == 200:
        datos = response.json()['d']
        # Crear una lista para almacenar las recetas formateadas
        recetas_formateadas = []

        for receta in datos:
            # Obtener el título de la receta
            titulo_receta = receta['Title']
            
            # Obtener los ingredientes de la receta
            ingredientes = receta['Ingredients']

            imagen = receta['Image']
            
            # Crear un diccionario para almacenar el título y los ingredientes de esta receta
            receta_formateada = {
                'titulo': titulo_receta,
                'ingredientes': list(ingredientes.values()),  # Convertir los valores del diccionario a una lista
                'imagen': imagen
            }
            
            # Agregar la receta formateada a la lista de recetas formateadas
            recetas_formateadas.append(receta_formateada)
    else:
        # Si la solicitud falla, retornamos un mensaje de error
        return ("error en la solicitud de la API")

    # Pasar la lista de recetas formateadas a la plantilla 'ideas.html' para su renderización
    return render_template('ideas.html', platos=recetas_formateadas)



    # return render_template('ideas.html')

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

# @app.route('/api')
# def api():  
#     datos = [{'id': '58', 'Title': 'Spiced Lamb and Dill Yogurt Pasta', 'Ingredients': {'1': '3 large egg yolks', '2': '2 cups kefir (cultured milk) or plain whole-milk yogurt', '3': '3 cups (lightly packed) dill fronds with tender stems (about 1 large bunch), divided', '4': '3 garlic cloves, divided', '5': '3 Tbsp. unsalted butter', '6': '½ cup pine nuts or slivered almonds', '7': '½ cup dried currants or raisins', '8': '1 tsp. kosher salt, plus more', '9': '1 Tbsp. ground cumin', '10': '1½ tsp. freshly ground black pepper', '11': '1 lb. ground lamb', '12': '1 lb. orecchiette or other short pasta', '13': '½ lemon'}, 'Instructions': 'Combine egg yolks, kefir, and 1½ cups dill in a blender; finely grate in 1 garlic clove and blend until smooth. Set purée aside. Finely chop remaining 1½ cups dill and set aside separately.\nMelt butter over medium heat in a large skillet. Add pine nuts and cook, stirring often, until golden brown, about 2 minutes. Add dried currants and cook, stirring often, until plump, about 1 minute. Scrape nut mixture into a small bowl; season with salt.\nWipe out skillet and heat over medium-high. Stir together cumin, pepper, and 1 tsp. salt in a small bowl. Place lamb in pan and use a sturdy spatula to aggressively flatten (like you’re making smash burgers); sprinkle spice mixture over. Cook, undisturbed, until lamb is well browned and crisp underneath, about 4 minutes. Hold back meat and drain off all of the fat. Break up meat into small pieces and mix in reserved nut mixture. Finely grate in remaining 2 garlic cloves and add reserved chopped dill. Cook, stirring, until herbs are wilted, about 1 minute. Set aside until pasta is ready.\nMeanwhile, cook pasta in a large pot of boiling salted water, stirring occasionally, until 1 minute shy of al dente (pasta will finish cooking in the sauce). Drain pasta and return to pot.\nPour reserved purée over pasta and set over medium heat. Cook, stirring constantly, until sauce thickens enough to cling to pasta and just comes to a simmer, about 3 minutes. Remove from heat; finely grate zest from lemon half over pasta, then squeeze in juice. Season with salt.\nDivide pasta among bowls and top with lamb mixture.', 'Image': '//20fix.com/xfood/img/spiced-lamb-and-dill-yogurt-pasta.jpg'}, 
#                 {'id': '70', 'Title': 'Swiss Chard Pasta With Toasted Hazelnuts and Parmesan', 'Ingredients': {'1': '¼ cup hazelnuts', '2': '1 pound bow tie pasta (farfalle)', '3': '8 tablespoons unsalted butter, plus more if needed', '4': '4 cloves of garlic, minced', '5': 'Hefty pinch each of salt and freshly ground black pepper', '6': 'Small pinch of crushed red pepper flakes', '7': '1 bunch Swiss chard, stems finely chopped and greens thinly sliced', '8': '4 ounces Parmesan cheese, shaved', '9': '2 tablespoons balsamic vinegar (optional)'}, 'Instructions': 'Add the hazelnuts to a small skillet over medium heat. Toast them slowly, shaking the pan often, until lightly browned, 8 to 10 minutes. Remove them from the skillet, and when they are cool enough to handle, roughly chop the nuts.\nBring a large pot of salted water to a boil and cook the pasta until al dente. Drain it, reserving 1/2 cup of the cooking liquid and add it to a large bowl.\nIn a large skillet, heat the butter over medium-low heat. Once the butter begins to foam, add the garlic and use a wooden spoon to stir the mixture constantly until the butter begins to brown and have a slight nutty aroma, about 5 minutes. Add the salt, black pepper, and red pepper flakes. Give the mixture a good stir, and then set it aside to infuse for about 5 minutes longer away from the heat.\nPour the butter mixture (scraping the garlic, salt, pepper, and red pepper flakes) all over the warm pasta. If the pasta feels a bit dry, add a touch of the reserved cooking liquid. Toss to combine and set aside.\nSet the same skillet (without cleaning it) over medium-high heat. Add the chard stems and cook for 5 minutes. Add the chard leaves and continue to cook, tossing the mixture every so often, until the greens begin to wilt and turn bright green, 3 to 5 minutes longer. Add a touch more butter or oil to the pan if it dries out too much.\nAdd the Swiss chard and hazelnuts to the pasta and toss it all together. Add the Parmesan shavings and the balsamic vinegar (if you’re using it); toss. Taste for seasonings and add more salt and pepper if needed.\nServe warm or at room temperature.\nLocalize it: You can use kale instead of chard, and any nut will work in place of the hazelnuts. Fresh out of balsamic vinegar? Red wine vinegar or freshly squeezed lemon juice will work.', 'Image': '//20fix.com/xfood/img/swiss-chard-pasta-with-toasted-hazelnuts-and-parmesan.jpg'}, 
#                 {'id': '82', 'Title': 'Melted Broccoli Pasta With Capers and Anchovies', 'Ingredients': {'1': 'Kosher salt', '2': '2 heads (about 1 pound, or 454g, total) broccoli, cut into bitesize florets', '3': '12 ounces (340 g) whole-wheat penne pasta, or other short tubular pasta', '4': '3 tablespoons (45 ml) extra-virgin olive oil, divided', '5': '1 cup (54 g) panko or Freezer Bread Crumbs (see Note)', '6': '4 oil-packed anchovy fillets', '7': '¼ cup (36 g) capers, chopped if large (rinsed well if salt-packed)', '8': '2 garlic cloves, minced', '9': '¼ teaspoon red pepper flakes'}, 'Instructions': "Bring a large pot of salted water to a boil over high heat. Add the broccoli florets and cook until bright green and crisp-tender, 2 to 3 minutes. Using a slotted spoon, transfer the broccoli to a large bowl.\nAdd the pasta to the boiling water and cook for 1 minute less than the package instructions for al dente, about 9 minutes.\nMeanwhile, toast the bread crumbs. Heat 1 tablespoon (15 ml) of olive oil in a large, high-sided sauté pan or skillet over medium heat. Add the breadcrumbs and sauté until the crumbs are golden brown and crisp, 4 to 5 minutes. Transfer to a small bowl and set aside.\nPour the remaining 2 tablespoons (30 ml) of olive oil into the pan. Add the anchovies and sauté until they disintegrate, about 1 minute. Add the capers, garlic, and red pepper flakes. Sauté until fragrant, about 1 minute, and remove from the heat.\nWhen the pasta is ready, reserve 1½ cups (360 ml) of pasta water with a measuring cup, then drain the pasta. Add the broccoli and reserved pasta water to the pan and bring to a simmer. Continue to simmer, using a wooden spoon to break the florets into small pieces as they become more tender, until the water is reduced by about half and you've been able to break apart enough florets that you're left with a very chunky mixture, 5 to 7 minutes.\nAdd the pasta to the pan. Cook, tossing and stirring, until the pasta is al dente and the sauce thickens and coats the pasta, 1 to 2 minutes. Remove from the heat, add half the toasted bread crumbs, and toss again to combine. Serve garnished with the remaining toasted bread crumbs.", 'Image': '//20fix.com/xfood/img/melted-broccoli-pasta-sheela-prakash.jpg'}, 
#                 {'id': '90', 'Title': 'Burst Cherry Tomato Pasta', 'Ingredients': {'1': '½ cup extra-virgin olive oil, plus more for drizzling', '2': '6 garlic cloves, smashed', '3': '2½ lb. cherry tomatoes (about 4 pints)', '4': '2 large sprigs basil, plus 1 cup basil leaves, torn if large', '5': '¾ tsp. crushed red pepper flakes', '6': '1½ tsp. kosher salt, plus more', '7': 'Pinch of sugar (optional)', '8': '12 oz. casarecce or other medium-size pasta', '9': '1 oz. Parmesan, finely grated (about ½ cup), plus more for serving'}, 'Instructions': 'Heat ½ cup oil in a large heavy pot over low. Add garlic and cook, stirring often with a wooden spoon, until softened but not browned, about 2 minutes.\nIncrease heat to medium and add tomatoes, basil sprigs, red pepper flakes, and 1½ tsp. salt. Cook, stirring to coat, until some of the tomatoes begin to burst and release their juices, about 4 minutes. Smash some but not all of the tomatoes with the spoon to help release their liquid, then continue to cook, stirring occasionally, until a chunky, thickened sauce forms (about half the tomatoes should still be intact), 10–12 minutes. Taste and add sugar if sauce is too tart and add more salt if needed. Pluck out and discard basil sprigs.\nMeanwhile, cook pasta in a large pot of boiling salted water, stirring occasionally, until al dente.\nDrain pasta, add to pot with sauce, and cook, stirring, until coated, about 1 minute. Remove from heat and stir in 1 oz. Parmesan.\nDivide pasta among bowls; drizzle with oil. Top with more Parmesan and 1 cup basil leaves.', 'Image': '//20fix.com/xfood/img/burst-cherry-tomato-pasta.jpg'}, 
#                 {'id': '256', 'Title': 'Pasta With Broccoli and Lemon Cashew-Cream Sauce', 'Ingredients': {'1': '1 cup (150g or 5¼ oz) raw cashews', '2': '2 cups (500ml or 17 fl oz) boiling water', '3': '1 cup (250ml or 8½ fl oz) good-quality vegetable stock', '4': '¼ cup (60ml or 2 fl oz) lemon juice', '5': 'Sea salt and cracked black pepper', '6': '400g (14 oz) dried wholemeal (whole-wheat) spaghetti', '7': '300g (10½ oz) broccoli florets (about 1 head)', '8': '½ cup (10g or ¼ oz) small basil leaves', '9': '1 tablespoon finely shredded lemon rind'}, 'Instructions': 'To make the lemon cashew-cream sauce, place the cashews in a medium heatproof bowl and cover with the boiling water. Allow to stand for 30 minutes. Drain the cashews well and place them in a blender. Add the stock, lemon juice, salt and pepper and blend until very smooth.\nCook the pasta in a large saucepan of salted boiling water for 6 minutes. Add the broccoli and cook for a further 4 minutes or until the pasta is al dente and the broccoli is just tender. Drain the pasta and broccoli and immediately return to the warm saucepan. Add the cashew-cream sauce and toss to combine.\nDivide the pasta between serving bowls and top with the basil and lemon rind to serve.', 'Image': '//20fix.com/xfood/img/pasta-with-broccoli-and-lemon-cashew-cream-sauce.jpg'}]

#     primeros_cinco = datos[:5]
    
#     for receta in primeros_cinco:
#         # Obtener el diccionario de ingredientes de la receta actual
#         ingredientes = receta['Ingredients']
        
#         # Imprimir el título de la receta
#         receta = "Ingredientes para", receta['Title'] + ":"

#         for ingrediente in ingredientes.values():
#             print(ingrediente)

#     return render_template('ideas.html', platos = receta)
    
if __name__ == '__main__':

    app.run(debug=True)


    