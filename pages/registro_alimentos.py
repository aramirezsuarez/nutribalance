
# Importar librerias
import re
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import streamlit_authenticator as stauth
from deta import Deta

# Almacenamos la key de la base de datos en una constante
DETA_KEY = "e0qgr2zg4tq_mbZWcCg7iGCpWFBbCy3GGFjEYHdFmZYR"

# Creamos nuestro objeto deta para hacer la conexion a la DB
deta = Deta(DETA_KEY)

# Realizamos la conexion a la DB
db = deta.Base("NutribalanceUsers")

# Funcion que retorna los usuarios registrados
def fetch_usuarios():
    """Regresa un diccionario con los usuarios registrados"""
    # guardamos los datos de la DB en users y retornamos su contenido
    users = db.fetch()
    return users.items

# Funcion que retorna los emails de los usuarios registrados
def get_emails_usuarios():
    """Regresa una lista con los emails de cada usuario"""
    # guardamos los datos de la DB en users
    users = db.fetch()
    emails = []
    # filtramos los emails de la DB
    for user in users.items:
        emails.append(user["key"])
    return emails

# Funcion que retorna los nombres de usuario de los usuarios registrados
def get_usernames_usuarios():
    """Regresa una lista con los username de cada usuario"""
    # guardamos los datos de la DB en users
    users = db.fetch()
    usernames = []
    # filtramos los usernames de la DB
    for user in users.items:
        usernames.append(user["username"])
    return usernames

# Funcion que verifica si un email ingresado es valido
def validar_email(email):
    """Retorna True si el email ingresado es valido,
    de lo contrario retorna False"""
    # Patrones tipicos de un email valido
    pattern = "^[a-zA-Z0_9-_]+@[a-zA-Z0_9-_]+\.[a-z]{1,3}$"
    pattern1 = "^[a-zA-Z0_9-_]+@[a-zA-Z0_9-_]+\.[a-z]{1,3}+\.[a-z]{1,3}$"

    # Verifica si el email ingresado coincide con algun patron definido
    if re.match(pattern, email) or re.match(pattern1, email):
        return True
    return False

# Funcion que verifica si un username ingresado es valido
def validar_username(username):
    """Retorna True si el username es valido, de lo contrario,
    retorna False"""
    # Se define el patron de un username tipico
    pattern = "^[a-zA-Z0-9]*$"
    # Se verifica si el username ingresado coincide con el patron tipico
    if re.match(pattern, username):
        return True
    return False

# Manejo de posibles errores
try:
    # Se almacenan los datos necesarios de la DB
    users = fetch_usuarios()
    emails = get_emails_usuarios()
    usernames = get_usernames_usuarios()
    passwords = [user["password"] for user in users]

    # Se crea el diccionario credentials necesario para el funcionamiento
    # del autenticador de cuentas
    credentials = {"usernames" : {}}
    for index in range(len(emails)):
        credentials["usernames"][usernames[index]] = {"name" : emails[index],
                                               "password" : passwords[index]}

    # Creacion del autenticador
    Authenticator = stauth.Authenticate(credentials, cookie_name="Streamlit",
                                      key="cookiekey", cookie_expiry_days=3)

    # Crear boton de Cerrar sesion si la sesion fue iniciada
    if st.session_state["authentication_status"]:
        Authenticator.logout("Cerrar sesion", location="sidebar")

# Informar de que hubo una excepcion en caso de que la haya
except:
    st.error("Excepcion lanzada")

# Crear pie de pagina con los datos de contacto de los creadores
footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        z-index: 10;
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

# Titulo de la seccion
st.title("Registro de ejercicios realizados")

url_exercise = (
    "https://docs.google.com/spreadsheets/d/e/2PACX"
    "-1vSMxHG9CEe_akA21j9UciEP14scuPRsWMrT_I8W5bLuZ"
    "Vrq93h5XzyD20hdJL0cCRk0ZqUkmgdl-leY/pub?output=csv"
)

df_exercise=pd.read_csv(url_exercise)

# Convertir a enteros en el DataFrame food
columnas_to_clean = ["130 lb", "155 lb", "180 lb", "205 lb"]

for elements in columnas_to_clean:
    df_exercise[elements] = df_exercise[elements].astype(int)

# Mostrar el dataframe
st.write("### Lista de ejercicios disponibles para elegir:")
st.write(df_exercise)

# Elemento interactivo para que el usuario seleccione alimentos
ejercicio_seleccionado = st.selectbox(
    "Selecciona un ejercicio:",
    df_exercise["Activity, Exercise or Sport (1 hour)"]
)

# Obtener los detalles del alimento seleccionado
detalles_ejercicio = df_exercise[
    df_exercise["Activity, Exercise or Sport (1 hour)"] ==
    ejercicio_seleccionado
]

if not detalles_ejercicio.empty:
    st.write("### Detalles del Ejercicio Seleccionado:")
    st.write(detalles_ejercicio)
else:
    st.write("Selecciona un ejercicio de la lista.")

# Inicializa una variable para realizar,
# el seguimiento del total de calorías quemadas
total_calorias_quemadas = 0

# Variable que almacena varios ejercicios
ejercicios_seleccionados = st.multiselect(
    "Selecciona los ejercicios que has realizado:",
    df_exercise["Activity, Exercise or Sport (1 hour)"]
)

# Obtener los detalles de los ejercicios seleccionados y sumar las calorías
for ejercicio_seleccionado in ejercicios_seleccionados:
    detalles_ejercicio = df_exercise[
    df_exercise["Activity, Exercise or Sport (1 hour)"] ==
    ejercicio_seleccionado
]

    if not detalles_ejercicio.empty and "130 lb" in detalles_ejercicio.columns:
        calorias_ejercicio = detalles_ejercicio["130 lb"].values[0]
        total_calorias_quemadas += calorias_ejercicio
        st.write(f"Detalles del Ejercicio Seleccionado "
         f"({ejercicio_seleccionado}):")
        st.write(detalles_ejercicio)
        st.write(f"Calorías quemadas:{calorias_ejercicio}")

# Mostrar el total de calorías quemadas
st.write(f"Total de calorías quemadas: {total_calorias_quemadas}")

# Funcion para cargar las animaciones
def load_lottieurl(url):
    """
    Carga un archivo JSON Lottie desde una URL.

    Parameters:
    - url (str): La URL del archivo JSON Lottie.

    Returns:
    - dict or None: Un diccionario que representa el contenido JSON
    del archivo Lottie si la carga es exitosa.
    None si la carga falla debido a un código de estado diferente a 200.
    """
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# URL de animacion #1
lottie_ejercicio_sumo = load_lottieurl("https://raw.githubusercontent.com/"
 "lflunal/ppi_20/main/animaciones/ejercicio%20%22sumo%22")

# Mostrar animacion #1
st_lottie(lottie_ejercicio_sumo, height = 180, key="sumo")
