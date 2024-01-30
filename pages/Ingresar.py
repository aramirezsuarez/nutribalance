import streamlit as st
import streamlit_authenticator as stauth
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
    user_dict = {user['username']: user for user in users.items}
    return user_dict
def get_usernames_usuarios():
    """
    Recupera y devuelve una lista con los nombres de usuario de cada
    usuario registrado en la Base de Datos.
    Returns:
    - list: Una lista que contiene los nombres de usuario de
    todos los usuarios registrados.
    """
    # guardamos las claves (nombres de usuario) de los datos de la DB
    users = fetch_usuarios()
    usernames = list(users.keys())
    return usernames
# Tu función de inicio de sesión
def login(username, password, credentials):
    """
    Función de inicio de sesión que verifica las credenciales
    con los usuarios registrados en la base de datos.
    """
    if username in credentials["usernames"]:
        stored_user = credentials["usernames"][username]
        if stored_user["password"] == password:
            return True
    return False
def get_emails_usuarios():
    """
    Recupera y devuelve una lista con las direcciones de correo
    electrónico de cada usuario registrado en la Base de Datos.
    Returns:
    - list: Una lista que contiene las direcciones de correo electrónico de
    todos los usuarios registrados.
    """
    # guardamos las claves (nombres de usuario) de los datos de la DB
    users = fetch_usuarios()
    emails = list(users.keys())
    return emails
# Tu función principal
def main():
    st.title("Inicio de Sesión")

    # Formulario de inicio de sesión
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        if username in usernames:
            if login(username, password, credentials):
                st.success(f"Bienvenido, {username}!")
                # Agrega el contenido de la aplicación después del inicio de sesión exitoso.
                st.write("Inicio de sesión exitoso")
            else:
                st.error("Credenciales incorrectas. Por favor, inténtalo de nuevo.")
        else:
            st.error("Usuario no encontrado. Por favor, regístrese.")

# Se almacenan los datos necesarios de la DB
all_users = fetch_usuarios()
usernames = get_usernames_usuarios()
passwords = [all_users[username]["password"] for username in usernames]
# Se crea el diccionario credentials necesario para el
# funcionamiento del autenticador de cuentas
credentials = {"usernames": {}}
for username in usernames:
    credentials["usernames"][username] = {"name": all_users[username]["key"],
                                          "password": all_users[username]["password"]}
if __name__ == "__main__":
    main()
