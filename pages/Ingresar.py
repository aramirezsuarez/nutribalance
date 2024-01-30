import streamlit as st
import streamlit_extras
import streamlit_authenticator as stauth
import re
from deta import Deta
from Registrarse import registro


st.set_page_config(page_title='Inicio de sesion')

def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    users = db.fetch()
    return users.items


try:
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
                st.warning('Usuario no encontrado, Por favor registrese')


except:
    st.success('Inicio de sesion correcto')
