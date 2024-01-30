# Pagina de inicio de sesion

# Importar librerias necesarias
import streamlit as st
import streamlit_extras
import streamlit_authenticator as stauth
import re
from deta import Deta

# Almacenamos la key de la base de datos en una constante
DETA_KEY = "e0qgr2zg4tq_mbZWcCg7iGCpWFBbCy3GGFjEYHdFmZYR"

# Creamos nuestro objeto deta para hacer la conexion a la DB
deta = Deta(DETA_KEY)

# Realizamos la conexion a la DB
db = deta.Base("NutribalanceUsers")

# Funcion para registrar usuarios en la DB
def insertar_usuario(email, username, age, height, password):
    """
    Agrega un nuevo usuario a la Base de Datos.

    Parameters:
    - email (str): Dirección de correo electrónico única del usuario.
    - username (str): Nombre de usuario único del usuario.
    - age (int): Edad del usuario.
    - height (float): Altura del usuario en centímetros.
    - password (str): Contraseña del usuario.

    Returns:
    - bool: True si la inserción fue exitosa, False si hubo un error.
    """
    return db.put({"key": email, "username": username, "age": age,
                   "height": height, "password": password})

# Funcion que retorna los usuarios registrados
def fetch_usuarios():
    """
   Recupera y devuelve un diccionario con los usuarios
   registrados en la Base de Datos.

   Returns:
   - dict: Un diccionario que contiene la información de los
   usuarios registrados.
   Cada clave es la dirección de correo electrónico única del usuario,
   y cada valor es un diccionario con detalles como
   "username", "age", "height", y "password".
   """
    # guardamos los datos de la DB en users y retornamos su contenido
    users = db.fetch()
    return users.items

# Funcion que retorna los emails de los usuarios registrados
def get_emails_usuarios():
    """
    Recupera y devuelve una lista con las direcciones de correo
    electrónico de cada usuario registrado en la Base de Datos.

    Returns:
    - list: Una lista que contiene las direcciones de correo electrónico de
    todos los usuarios registrados.
    """
    # guardamos los datos de la DB en users
    users = db.fetch()
    emails = []
    # filtramos los emails de la DB
    for user in users.items:
        emails.append(user["key"])
    return emails

# Funcion que retorna los nombres de usuario de los usuarios registrados
def get_usernames_usuarios():
    """
    Recupera y devuelve una lista con los nombres de usuario de cada
    usuario registrado en la Base de Datos.

    Returns:
    - list: Una lista que contiene los nombres de usuario de
    todos los usuarios registrados.
    """
    # guardamos los datos de la DB en users
    users = db.fetch()
    usernames = []
    # filtramos los usernames de la DB
    for user in users.items:
        usernames.append(user["username"])
    return usernames

# Funcion que verifica si un email ingresado es valido
def validar_email(email):
    """
   Retorna True si el email ingresado es válido, de lo contrario retorna False

   Parameters:
   - email (str): Dirección de correo electrónico a validar.

   Returns:
   - bool: True si el email es válido, False si no lo es.
   """
    # Patrones tipicos de un email valido
    pattern = "^[a-zA-Z0_9-_]+@[a-zA-Z0_9-_]+\.[a-z]{1,3}$"
    pattern1 = "^[a-zA-Z0_9-_]+@[a-zA-Z0_9-_]+\.[a-z]{1,3}+\.[a-z]{1,3}$"

    # Verifica si el email ingresado coincide con algun patron definido
    if re.match(pattern, email) or re.match(pattern1, email):
        return True
    return False

# Funcion que verifica si un username ingresado es valido
def validar_username(username):
    """
    Retorna True si el nombre de usuario ingresado es válido,
    de lo contrario, retorna False.

    Parameters:
    - username (str): Nombre de usuario a validar.

    Returns:
    - bool: True si el nombre de usuario es válido, False si no lo es.
    """
    # Se define el patron de un username tipico
    pattern = "^[a-zA-Z0-9]*$"
    # Se verifica si el username ingresado coincide con el patron tipico
    if re.match(pattern, username):
        return True
    return False

# Función para actualizar la contraseña y/o el nombre de usuario
def actualizar_datos_usuario(username, new_username, new_password):
    """
    Actualiza la contraseña y/o el nombre de usuario de un usuario registrado.

    Parameters:
    - username (str): Nombre de usuario actual del usuario.
    - new_username (str): Nuevo nombre de usuario (puede ser el mismo).
    - new_password (str): Nueva contraseña (puede ser la misma).

    Returns:
    - bool: True si la actualización fue exitosa, False si hubo un error.
    """
    users = db.fetch()
    for user in users.items:
        if user["username"] == username:
            if new_username:
                user["username"] = new_username
            if new_password:
                new_encrypted_password = stauth.Hasher([new_password]).generate()
                user["password"] = new_encrypted_password[0]
            db.put(user)
            return True
    return False


# Crear pie de pagina con los datos de contacto de los creadores
footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgb(14, 17, 23);
        color: black;
        text-align: center;
    }
    .footer p {
        color: white;
    }
</style>
<div class="footer">
    <p>App desarrollada por: <br />
    Luis Fernando López Echeverri | Andres Felipe Ramirez Suarez <br />
    Contactenos: <a href="#">lulopeze@unal.edu.co</a> | <a href="#">aramirezsu@unal.edu.co</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
