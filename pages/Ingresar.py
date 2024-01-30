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

import streamlit as st
from datetime import datetime

# Tu función fetch_usuarios
def fetch_usuarios():
    users = db.fetch()
    return users.items

# Tu función de inicio de sesión
def login(username, password):
    """
    Función de inicio de sesión que verifica las credenciales
    con los usuarios registrados en la base de datos.
    """
    usuarios = fetch_usuarios()
    for usuario in usuarios:
        if usuario["username"] == username and usuario["password"] == password:
            return True
    return False

# Tu función principal
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


