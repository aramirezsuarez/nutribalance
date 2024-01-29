# Importar librerias
import re
import pandas as pd
import numpy as np
import streamlit as st
import streamlit_extras
import streamlit_authenticator as stauth
from deta import Deta
from datetime import datetime
from datetime import time
import matplotlib.pyplot as plt

# Almacenamos la key de la base de datos en una constante

# Titulo en la pagina
st.title("Nutribalance")

# Descripcion de la app
st.write("Nutribalance es una aplicación web enfocada en el mejoramiento de la"
"nutricion general de los usuarios, basandose en 3 objetivos básicos de los"
         "mismos: Mantenerse en un peso, Bajar de peso o Subir de peso.")

st.markdown("## Características de la app")

# Caracteristicas de la app
st.write("Calcular la información nutricional de las comidas del usuario.")
st.write("Una vez registrado, revisar el progreso de las rutinas "
"alimentarias del usuario.")
st.write("Recomendaciones alimentarias basadas en los objetivos "
"personales del usuario.")
st.write("Las recomendaciones tendrán en cuenta alergias o intolerancias que "
"tenga el usuario frente a ciertos alimentos/ingredientes, "
"si este lo especifica.")

# Manejo de posibles errores
try:
    # Se almacenan los datos necesarios de la DB
    users = fetch_usuarios()
    emails = get_emails_usuarios()
    usernames = get_usernames_usuarios()
    passwords = [user["password"] for user in users]

    # Se crea el diccionario credentials necesario para el
    # funcionamiento del autenticador de cuentas
    credentials = {"usernames" : {}}
    for index in range(len(emails)):
        credentials["usernames"][usernames[index]] = {"name" : emails[index],
                                                "password" : passwords[index]}

    # Creacion del autenticador
    Authenticator = stauth.Authenticate(credentials, cookie_name="Streamlit",
                                        key="cookiekey", cookie_expiry_days=3)

    # Crear boton de Cerrar sesion si la sesion fue iniciada
    if st.session_state["authentication_status"]:
        email, authentication_status, username = \
    Authenticator.login("Ingresar", "main")
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


