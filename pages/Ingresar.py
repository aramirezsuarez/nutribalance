# Importar librerias necesarias
import streamlit as st
from deta import Deta
import streamlit_authenticator as stauth

# Almacenamos la key de la base de datos en una constante
DETA_KEY = "e0qgr2zg4tq_mbZWcCg7iGCpWFBbCy3GGFjEYHdFmZYR"

# Creamos nuestro objeto deta para hacer la conexion a la DB
deta = Deta(DETA_KEY)

# Realizamos la conexion a la DB
db = deta.Base("NutribalanceUsers")

# Se almacenan los datos necesarios de la DB
users = db.fetch()
emails = [user["key"] for user in users.items]
usernames = [user["username"] for user in users.items]
passwords = [user["password"] for user in users.items]

# Se crea el diccionario credentials necesario para el funcionamiento del autenticador de cuentas
credentials = {"usernames": {}}
for index in range(len(emails)):
    credentials["usernames"][usernames[index]] = {"name": emails[index], "password": passwords[index]}

# Creacion del autenticador
Authenticator = stauth.Authenticate(credentials, cookie_name="Streamlit", key="cookiekey", cookie_expiry_days=3)

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
    try:
        db.put({"key": email, "username": username, "age": age, "height": height, "password": password})
        return True
    except Exception as e:
        st.error(f"Error al insertar usuario: {e}")
        return False

# Página de inicio de sesión
def login():
    st.subheader("Iniciar Sesión")

    # Formulario de inicio de sesión
    with st.form(key="login_form", clear_on_submit=True):
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        submit_button = st.form_submit_button("Iniciar Sesión")

    # Validar la información del formulario
    if submit_button:
        if username in credentials["usernames"] and stauth.Hasher([password]).verify(credentials["usernames"][username]["password"]):
            st.success("Inicio de sesión exitoso")
            st.session_state["authentication_status"] = True
        else:
            st.error("Credenciales incorrectas")

# Página principal
def main():
    # Verificar si el usuario está autenticado
    if st.session_state.get("authentication_status", False):
        st.write("¡Ya has iniciado sesión!")
        st.button("Cerrar Sesión", on_click=Authenticator.logout)
    else:
        login()

# Ejecutar la aplicación principal
if __name__ == "__main__":
    main()
