
# Importar librerias
import re
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import streamlit_authenticator as stauth
from deta import Deta


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
