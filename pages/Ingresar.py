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

# Resto del código
users = fetch_users()
emails = []
usernames = []
passwords = []

for user in users:
    emails.append(user['key'])
    usernames.append(user['username'])
    passwords.append(user['password'])

credentials = {'usernames': {}}
for index in range(len(emails)):
    credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

info, info1 = st.columns(2)

if not authentication_status:
    sign_up()

if username:
    if username in usernames:
        if authentication_status:
            st.sidebar.subheader(f'Bienvenido {username}')
            Authenticator.logout('Cerrar sesión', 'sidebar')

        elif not authentication_status:
            with info:
                st.error('Contraseña o Usuario Incorrecto')
        else:
            with info:
                st.warning('Por favor introduzca sus credenciales')
    else:
        with info:
            st.warning('Usuario no encontrado, Por favor regístrese')
