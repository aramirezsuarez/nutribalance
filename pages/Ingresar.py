import streamlit as st
from datetime import datetime, timedelta
from deta import Deta

# Almacenamos la key de la base de datos en una constante
DETA_KEY = "e0qgr2zg4tq_mbZWcCg7iGCpWFBbCy3GGFjEYHdFmZYR"

# Creamos nuestro objeto deta para hacer la conexión a la DB
deta = Deta(DETA_KEY)

# Realizamos la conexión a la DB
db = deta.Base("NutribalanceUsers")

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Función para obtener usuarios desde la base de datos
def fetch_users():
    users = db.fetch()
    return {user['username']: User(user['username'], user['password']) for user in users.items}

# Función para obtener los nombres de usuario
def get_usernames(users):
    return list(users.keys())

# Función para verificar las credenciales del usuario
def login(username, password, users):
    if username in users and users[username].password == password:
        return True
    return False

# Función para obtener el token de sesión desde la base de datos
def get_session_token(username):
    session = db.get(username)
    return session.get("session_id") if session else None

# Función para guardar el token de sesión en la base de datos
def save_session_token(username, session_id):
    db.put({"key": username, "session_id": session_id})

# Función principal
def main():
    st.title("Inicio de Sesión")

    # Obtener usuarios desde la base de datos
    users = fetch_users()
    usernames = get_usernames(users)

    # Formulario de inicio de sesión
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    # Verificar credenciales al hacer clic en el botón
    if st.button("Iniciar Sesión"):
        if username in usernames and login(username, password, users):
            # Obtener el token de sesión existente o crear uno nuevo
            session_id = get_session_token(username) or f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            # Guardar el token de sesión en la base de datos
            save_session_token(username, session_id)
            st.success(f"Bienvenido, {username}!")
            # Agregar el contenido de la aplicación después del inicio de sesión exitoso.
            st.write("Inicio de sesión exitoso")
        else:
            st.error("Credenciales incorrectas. Por favor, inténtalo de nuevo.")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
