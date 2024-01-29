# -*- coding: utf-8 -*-
"""registro_alimentos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RpvmsWeHdW4oW3MTPrx2MPdmU6WMKeck
"""

# Importar librerias
import re
from datetime import date
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

# Funcion para agregar valores caloricos a la DB registrados en un dia
def add_food(email, new_food_data):
    """
    Agrega una comida al día o actualiza una existente,
    si la fecha ya está registrada.
    """
    user = db.get(email)
    date = new_food_data[0]
    calories = new_food_data[1]
    carbs = new_food_data[2]
    fat = new_food_data[3]
    fiber = new_food_data[4]
    protein = new_food_data[5]

    # Convierte la fecha en una cadena en formato ISO
    date_iso = date.isoformat()

    # Verifica si la fecha ya existe en la lista de comidas
    food_updated = False
    for food in user["food"]:
        if food[0] == date_iso:
            # La fecha ya existe, actualiza las calorías en lugar de
            # agregar una nueva entrada
            food[1] = calories
            food[2] = carbs
            food[3] = fat
            food[4] = fiber
            food[5] = protein
            food_updated = True
            # Termina el bucle si la fecha coincide
            break

    # Si no se actualizó, agrega una nueva entrada
    if not food_updated:
        user["food"].append([date_iso, calories, carbs, fat, fiber, protein])

    # Actualiza el usuario en la base de datos
    db.put(user)

def update_food(email, values):
    """
    Actualiza la comida del dia de en caso de que se vuelvan a enviar
    datos de un dia ya registrado en la base de datos
    """
    user = db.get(email)

    for food in user["food"]:
        if food[0] == values[0]:
            food[1] = values[1]
            break

    db.put(user)

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
        email, authentication_status, username = Authenticator.login(
    "Ingresar", "main"
)
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


# Lectura de datos
url_foods = (
  "https://docs.google.com/spreadsheets/d/e/2PACX"
  "-1vTRvtsx_JsvwK7xeQ-tB-Q6zOsAv3hmo5t4On_FQicArs50"
  "-N0QJy60J3DH6rNsxRJgHLlGXCinT9yO/pub?output=csv"
  )


# Cargar el DataFrame desde la URL y ordenar alfabeticamente
df_foods_base = pd.read_csv(url_foods)
df_foods_base = df_foods_base.sort_values("Food")

# Eliminar comas y convertir a enteros en el DataFrame food
columns_to_clean = ["Calories", "Grams", "Protein", "Fat","Sat.Fat",
                    "Fiber", "Carbs"]

for column in columns_to_clean:
    df_foods_base[column] = df_foods_base[column].str.replace(',',
                                                              '', regex=True)
    df_foods_base[column] = df_foods_base[column].str.replace('t',
                                                              '0', regex=True)
    df_foods_base[column] = df_foods_base[column].str.replace('a',
                                                              '0', regex=True)
    df_foods_base[column] = df_foods_base[column].str.replace("'",
                                                              '', regex=True)
    df_foods_base[column] = df_foods_base[column].str.strip()
    df_foods_base[column] = df_foods_base[column].str.replace(',',
                                                              '.', regex=True)
    df_foods_base[column] = df_foods_base[column].replace('', '0')
    df_foods_base[column] = df_foods_base[column].astype(float) \
    .fillna(0).astype(int)

# Configuración de la aplicación Streamlit
st.title("Registro de Alimentos Consumidos en el Día")

# Seleccionar posibles alergias o disgustos de algun alimento
alergias_seleccionadas = st.multiselect(
    "Selecciona los alimentos que no desea incluir:",
    df_foods_base["Food"]
)

# Inicializa una variable para realizar el seguimiento del total de calorías
total_calorias_consumidas = 0
total_carbohidratos_consumidas = 0
total_proteinas_consumidas = 0
total_grasa_saturada_consumidas = 0
total_fibra_consumida_consumidas = 0

# Guardamos inicialmente todos los alimentos en df_foods
df_foods = df_foods_base

# Ocultar del dataframe los elementos seleccionados
for alergia in alergias_seleccionadas:
    df_foods = df_foods[df_foods["Food"] != alergia]

st.write("### Lista de Alimentos:")
st.write(df_foods)

# Variable para la selecion de varias comidas
alimentos_seleccionados = st.multiselect(
    "Selecciona los alimentos que has consumido:",
    df_foods["Food"]
)

# Obtener los detalles de los alimentos seleccionados
for alimento_seleccionado in alimentos_seleccionados:
    detalles_alimento = df_foods[df_foods["Food"] == alimento_seleccionado]
    if not detalles_alimento.empty:
        st.write(f"### Detalles del Alimento Seleccionado "
         f"({alimento_seleccionado}):")


        # Genera una clave única para el widget number_input
        widget_key = f"number_input_{alimento_seleccionado}"

        # Utiliza la clave única en el number_input
        cantidad = st.number_input("Cantidad de porciones consumidas",
                                   value=1, key=widget_key)

        # Obtiene los valores del alimento
        calorias_alimento = detalles_alimento["Calories"].values[0]
        carbohidratos_alimento = detalles_alimento["Carbs"].values[0]
        proteina_alimento = detalles_alimento["Protein"].values[0]
        grasas_saturadas_alimento = detalles_alimento["Sat.Fat"].values[0]
        fibra_alimento = detalles_alimento["Fiber"].values[0]

        # Realiza las sumas utilizando NumPy
        total_calorias_consumidas += calorias_alimento * cantidad
        total_carbohidratos_consumidas += carbohidratos_alimento * cantidad
        total_proteinas_consumidas += proteina_alimento * cantidad
        total_grasa_saturada_consumidas += (
                          grasas_saturadas_alimento * cantidad)
        total_fibra_consumida_consumidas += fibra_alimento * cantidad

        st.write(detalles_alimento)
    else:
        st.write(
    "Selecciona un alimento de la lista o verifica la ortografía."
)


# Mostrar el total de valorico consumido (calorias, carb, grasas...)
st.write(f"Total de calorías consumidas: "
         f"{total_calorias_consumidas} calorías")
st.write(f"Total de carbohidratos consumidos: "
         f"{total_carbohidratos_consumidas} ")
st.write(f"Total de grasas saturadas consumida: "
         f"{total_grasa_saturada_consumidas} ")
st.write(f"Total de fibra consumida: "
         f"{total_fibra_consumida_consumidas} ")
st.write(f"Total de proteina consumida: {total_proteinas_consumidas} ")

# Se almacena el valor de los datos nutricionales al presionar el boton
boton_almacenar = st.button("Almacenar datos nutricionales")

if boton_almacenar:
    if st.session_state["authentication_status"]:
        fecha = date.today()
        add_food(email, [fecha,
                         float(total_calorias_consumidas),
                         float(total_carbohidratos_consumidas),
                         float(total_grasa_saturada_consumidas),
                         float(total_fibra_consumida_consumidas),
                         float(total_proteinas_consumidas)])
        st.success("Datos almacenados")
    else:
        st.warning("Para almacenar los datos primero debe iniciar"
                   "sesion o registrarse")

# Funcion para cargar las animaciones
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# URL de animacion #1
lottie_peso = load_lottieurl("https://raw.githubusercontent.com/lflunal/"
"ppi_20/main/animaciones/peso.json")

# Mostrar animacion #1
st_lottie(lottie_peso, height = 180, key="peso")
