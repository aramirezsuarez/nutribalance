

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
DETA_KEY = "e0qgr2zg4tq_mbZWcCg7iGCpWFBbCy3GGFjEYHdFmZYR"

# Creamos nuestro objeto deta para hacer la conexion a la DB
deta = Deta(DETA_KEY)

# Realizamos la conexion a la DB
db = deta.Base("NutribalanceUsers")

# Funcion para registrar usuarios en la DB
def insertar_usuario(email, username, age, height, password):
    """Agrega usuarios a la Base de Datos"""
    return db.put({"key":email, "username": username, "age":age,
                   "height":height, "password":password})

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

# Funcion para obtener los valores nutricionales del usuario
def get_datos_nutricionales(email):
    usuario = db.get(email)
    return usuario.get("food", [])

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

# Pagina a mostrar en caso de tener un usuario con sesion ingresada
if st.session_state["authentication_status"]:
    # Obtenemos datos nutricionales del usuario
    datos_usuario = get_datos_nutricionales(email)
    # Convierte los datos a un formato que se puede utilizar fácilmente
    datos = []
    for comida in datos_usuario:
        try:
            fecha = datetime.strptime(comida[0], "%Y-%m-%d")
        except (ValueError, TypeError):
          # Fecha predeterminada si hay un problema con el formato
            fecha = datetime.now()

        calorias = comida[1] if len(comida) > 1 else 0
        carbohidratos = comida[2] if len(comida) > 2 else 0
        grasa = comida[3] if len(comida) > 3 else 0
        fibra = comida[4] if len(comida) > 4 else 0
        proteinas = comida[5] if len(comida) > 5 else 0
        datos.append([fecha, calorias, carbohidratos, grasa,
                      fibra, proteinas])

    # Crea un DataFrame de pandas
    columnas = ["Fecha", "Calorias", "Carbohidratos", "Grasa",
                "Fibra", "Proteinas"]
    df = pd.DataFrame(datos, columns=columnas)

    # Calcular calorías semanales
    # Obtener el nombre del día de la semana
    df["DiaSemana"] = pd.to_datetime(df["Fecha"]).dt.strftime('%A')

    # Crear DataFrame con todos los días de la semana pasada
    ultimo_dia = datetime.now().date()
    dias_semana_pasada = pd.date_range(end=ultimo_dia, periods=7, freq="D")
    df_ultimos_7_dias = pd.DataFrame({"Fecha": dias_semana_pasada})

    # Combinar con los datos reales
    df_ultimos_7_dias = pd.merge(df_ultimos_7_dias, df, on="Fecha", how="left")

    # Rellenar NaN (días sin datos) con 0
    df_ultimos_7_dias = df_ultimos_7_dias.fillna(0)

    # Ordenar por fecha
    df_ultimos_7_dias = df_ultimos_7_dias.sort_values("Fecha")

    # Restablecer índice
    df_ultimos_7_dias = df_ultimos_7_dias.reset_index(drop=True)

    tipo_grafico = st.selectbox("Seleccione los graficos que desea ver",
                                ["Calorias","Grasas","Carbohidratos",
                                 "Proteinas"])

    st.subheader(f"Grafico de tu consumo diario semanal")
    if tipo_grafico == "Calorias":
        # Crear gráfico de barras de calorías diarias de los últimos 7 días
        plt.figure(figsize=(10, 6))
        plt.bar(df_ultimos_7_dias["Fecha"], df_ultimos_7_dias["Calorias"],
                color='blue', alpha=0.7)
        plt.title('Calorías Diarias Consumidas (Últimos 7 Días)')
        plt.xlabel('Fecha')
        plt.ylabel('Calorías')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
    
    elif tipo_grafico == "Carbohidratos":
        # Crear gráfico de barras de carbohidratos diarios de los últimos 7 días
        plt.figure(figsize=(10, 6))
        plt.bar(df_ultimos_7_dias["Fecha"], df_ultimos_7_dias["Carbohidratos"],
                color='green', alpha=0.7)
        plt.title('Carbohidratos Diarios Consumidos (Últimos 7 Días)')
        plt.xlabel('Fecha')
        plt.ylabel('Carbohidratos')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    elif tipo_grafico == "Grasas":
        # Crear gráfico de barras de grasa diaria de los últimos 7 días
        plt.figure(figsize=(10, 6))
        plt.bar(df_ultimos_7_dias["Fecha"], df_ultimos_7_dias["Grasa"],
                color='red', alpha=0.7)
        plt.title('Grasa Diaria Consumida (Últimos 7 Días)')
        plt.xlabel('Fecha')
        plt.ylabel('Grasas')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    elif tipo_grafico == "Proteinas":
        # Crear gráfico de barras de proteínas diarias de los últimos 7 días
        plt.figure(figsize=(10, 6))
        plt.bar(df_ultimos_7_dias["Fecha"], df_ultimos_7_dias["Proteinas"],
                color='purple', alpha=0.7)
        plt.title('Proteínas Diarias Consumidas (Últimos 7 Días)')
        plt.xlabel('Fecha')
        plt.ylabel('Proteínas (g)')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    # Graficos Mensuales
    st.subheader("Grafico de tu consumo mensual")
    # Convertir la columna "Fecha" a formato datetime
    df["Fecha"] = pd.to_datetime(df["Fecha"])

    # Filtrar los últimos 12 meses
    fecha_limite = df["Fecha"].max() - pd.DateOffset(months=12)
    df_meses = df[df['Fecha'] >= fecha_limite]
    df_meses["Mes"] = df_meses["Fecha"].dt.to_period("M")

    if tipo_grafico == "Calorias":
        # Crear gráfico de barras de calorías mensuales
        plt.figure(figsize=(10, 6))
        df_calorias_mensuales = df_meses.groupby("Mes")["Calorias"].sum().reset_index()
        plt.bar(df_calorias_mensuales["Mes"].astype(str),
                df_calorias_mensuales["Calorias"],
                color='blue', alpha=0.7)
        plt.title('Calorías Mensuales Consumidas (Últimos 12 Meses)')
        plt.xlabel('Mes')
        plt.ylabel('Calorías')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    elif tipo_grafico == "Carbohidratos":
        # Graficos Mensuales para Carbohidratos
        plt.figure(figsize=(10, 6))
        df_calorias_mensuales = df_meses.groupby("Mes")["Carbohidratos"].sum().reset_index()
        plt.bar(df_calorias_mensuales["Mes"].astype(str),
                df_calorias_mensuales["Carbohidratos"],
                color='green', alpha=0.7)
        plt.title('Carbohidratos Mensuales Consumidos (Últimos 12 Meses)')
        plt.xlabel('Mes')
        plt.ylabel('Carbohidratos')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    elif tipo_grafico == "Grasas":
        # Graficos Mensuales para Grasas
        plt.figure(figsize=(10, 6))
        df_calorias_mensuales = df_meses.groupby("Mes")["Grasa"].sum().reset_index()
        plt.bar(df_calorias_mensuales["Mes"].astype(str), df_calorias_mensuales["Grasa"],
                color='red', alpha=0.7)
        plt.title('Grasas Mensuales Consumidas (Últimos 12 Meses)')
        plt.xlabel('Mes')
        plt.ylabel('Grasas')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    elif tipo_grafico == "Proteinas":
        # Graficos Mensuales para Proteínas
        plt.figure(figsize=(10, 6))
        df_calorias_mensuales = df_meses.groupby("Mes")["Proteinas"].sum().reset_index()
        plt.bar(df_calorias_mensuales["Mes"].astype(str), df_calorias_mensuales["Proteinas"],
                color='purple', alpha=0.7)
        plt.title('Proteínas Mensuales Consumidas (Últimos 12 Meses)')
        plt.xlabel('Mes')
        plt.ylabel('Proteínas (g)')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
    
    # Mostrar estadisticos empleando numpy
    if tipo_grafico == "Calorias":
        st.subheader("Estadísticas de Calorías Diarias (Últimos 7 Días)")
        st.write(f"Consumo Promedio: {np.average(df_ultimos_7_dias['Calorias']):.2f} ")
        st.write(f"Valor Mínimo: {np.min(df_ultimos_7_dias['Calorias']):.2f} ")
        st.write(f"Valor Máximo: {np.max(df_ultimos_7_dias['Calorias']):.2f} ")
        st.subheader("Estadísticas de Calorías Mensuales (Últimos 12 Meses)")
        st.write(f"Consumo Promedio: {np.average(df_calorias_mensuales['Calorias']):.2f} ")
        st.write(f"Valor Mínimo: {np.min(df_calorias_mensuales['Calorias']):.2f} ")
        st.write(f"Valor Máximo: {np.max(df_calorias_mensuales['Calorias']):.2f} ")
    elif tipo_grafico == "Carbohidratos":
        st.subheader("Estadísticas de Carbohidratos Diarias (Últimos 7 Días)")
        st.write(f"Consumo Promedio: {np.average(df_ultimos_7_dias['Carbohidratos']):.2f} ")
        st.write(f"Valor Mínimo: {np.min(df_ultimos_7_dias['Carbohidratos']):.2f} ")
        st.write(f"Valor Máximo: {np.max(df_ultimos_7_dias['Carbohidratos']):.2f} ")
        st.subheader("Estadísticas de Carbohidratos Mensuales (Últimos 12 Meses)")
        st.write(f"Consumo Promedio: {np.average(df_calorias_mensuales['Carbohidratos']):.2f} ")
        st.write(f"Valor Mínimo: {np.min(df_calorias_mensuales['Carbohidratos']):.2f} ")
        st.write(f"Valor Máximo: {np.max(df_calorias_mensuales['Carbohidratos']):.2f} ")
    elif tipo_grafico == "Grasas":
        st.subheader("Estadísticas de Grasas Diarias (Últimos 7 Días)")
        st.write(f"Consumo Promedio: {np.average(df_ultimos_7_dias['Grasa']):.2f} ")
        st.write(f"Valor Mínimo: {np.min(df_ultimos_7_dias['Grasa']):.2f} ")
        st.write(f"Valor Máximo: {np.max(df_ultimos_7_dias['Grasa']):.2f} ")
        st.subheader("Estadísticas de Grasas Mensuales (Últimos 12 Meses)")
        st.write(f"Consumo Promedio: {np.average(df_calorias_mensuales['Grasa']):.2f} ")
        st.write(f"Valor Mínimo: {np.min(df_calorias_mensuales['Grasa']):.2f} ")
        st.write(f"Valor Máximo: {np.max(df_calorias_mensuales['Grasa']):.2f} ")
    elif tipo_grafico == "Proteinas":
        st.subheader("Estadísticas de Proteinas Diarias (Últimos 7 Días)")
        st.write(f"Consumo Promedio: {np.average(df_ultimos_7_dias['Proteinas']):.2f} g")
        st.write(f"Valor Mínimo: {np.min(df_ultimos_7_dias['Proteinas']):.2f} g")
        st.write(f"Valor Máximo: {np.max(df_ultimos_7_dias['Proteinas']):.2f} g")
        st.subheader("Estadísticas de Proteinas Mensuales (Últimos 12 Meses)")
        st.write(f"Consumo Promedio: {np.average(df_calorias_mensuales['Proteinas']):.2f} g")
        st.write(f"Valor Mínimo: {np.min(df_calorias_mensuales['Proteinas']):.2f} g")
        st.write(f"Valor Máximo: {np.max(df_calorias_mensuales['Proteinas']):.2f} g")

else:
    st.write("Si desea ver sus datos nutricionales "
         "y gráficas correspondientes,Inicie sesion o Registrese")
