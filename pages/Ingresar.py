import streamlit as st
from datetime import datetime
from deta import Deta

# Almacenamos la key de la base de datos en una constante
DETA_KEY = "e0qgr2zg4tq_mbZWcCg7iGCpWFBbCy3GGFjEYHdFmZYR"

# Creamos nuestro objeto deta para hacer la conexión a la DB
deta = Deta(DETA_KEY)

# Realizamos la conexión a la DB
db = deta.Base("NutribalanceUsers")

# Tu función fetch_usuarios
def fetch_usuarios():
    users = db.fetch()
    return users.items

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

# Se almacenan los datos necesarios de la DB
users = fetch_usuarios()
emails = get_emails_usuarios()
usernames = get_usernames_usuarios()
passwords = [user["password"] for user in users]

# Se crea el diccionario credentials necesario para el
# funcionamiento del autenticador de cuentas
credentials = {"usernames": {}}
for index in range(len(emails)):
    credentials["usernames"][usernames[index]] = {"name": emails[index],
                                                  "password": passwords[index]}

def login(username, password, credentials):
    """
    Función de inicio de sesión que verifica las credenciales
    con los usuarios registrados en la base de datos.
    """
    for user in credentials["usernames"]:
        if user["name"] == username and user["password"] == password:
            return True
    return False

# Luego, puedes llamar a la función login con tus credenciales
if login(username, password, credentials):
    st.success(f"Bienvenido, {username}!")
    # Agrega el contenido de la aplicación después del inicio de sesión exitoso.
    st.write("Aquí va el contenido de tu aplicación.")
else:
    st.error("Credenciales incorrectas. Por favor, inténtalo de nuevo.")
