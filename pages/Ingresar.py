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

# Funciones de utilidad
def fetch_users():
    users = db.fetch()
    return users.items

def get_emails_usuarios():
    users = db.fetch()
    emails = [user["key"] for user in users.items]
    return emails

def get_usernames_usuarios():
    users = db.fetch()
    usernames = [user["username"] for user in users.items]
    return usernames

import streamlit as st

# Credenciales de usuario (solo para fines de demostración, no utilizar en un entorno de producción)
credenciales = {"usuario1": "contrasena1", "usuario2": "contrasena2"}

def login(username, password):
    """
    Función de inicio de sesión simple.
    """
    if username in credenciales and credenciales[username] == password:
        return True
    return False

def main():
    st.title("Inicio de Sesión")

    # Formulario de inicio de sesión
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        if login(username, password):
            st.success(f"Bienvenido, {username}!")
            # Agrega el contenido de la aplicación después del inicio de sesión exitoso.
            st.write("Aquí va el contenido de tu aplicación.")
        else:
            st.error("Credenciales incorrectas. Por favor, inténtalo de nuevo.")

if __name__ == "__main__":
    main()

