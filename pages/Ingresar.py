import streamlit as st
import streamlit_extras
import streamlit_authenticator as stauth
import re
from deta import Deta


st.set_page_config(page_title='Inicio de sesion')

def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    users = db.fetch()
    return users.items
def registro():
    """
    Formulario de registro que guarda un registro de usuario en la
    base de datos si este es válido.

    Parameters:
    None

    Returns:
    None

    """
    # Se define un checkbox en el que se deben aceptar los
    # T&C antes de enviar un registro
    st.write("Debe aceptar los términos y condiciones antes de"
         "poder enviar el formulario")
    aceptar_terminos = st.checkbox("Acepto los [Términos y Condiciones]"
"(https://github.com/lflunal/ppi_20/blob/main/Politica%20de%20Tratamiento%20de%20Datos.md)")

    # Si se aceptan los términos y condiciones habilitar el registro
    if aceptar_terminos:
        # Creacion del formulario
        with st.form(key="registro", clear_on_submit=True):
            # Titulo del formulario
            st.subheader("Registrarse")

            # Campos a ser llenados por el usuario
            email = st.text_input("Email", placeholder="Ingrese su Email")
            username = st.text_input("Usuario",
                                    placeholder="Ingrese su nombre de usuario")
            dob = st.date_input("Fecha de Nacimiento",
                                min_value=datetime(1900, 1, 1),
                                max_value=datetime.today())
            password = st.text_input("Contraseña",
                            placeholder="Ingrese su contraseña", type="password")
            # Cambiar fecha del formulario a un formato almacenable en la DB
            dob_str = dob.isoformat() if dob else None

            # Boton de envio de datos de registro
            st.form_submit_button("Registrate")
        # Revisar validez de los datos ingresados por el usuario
        # y registro a la DB
        if email and username and dob and password:
            if validar_email(email):
                if email not in get_emails_usuarios():
                    if validar_username(username):
                        if username not in get_usernames_usuarios():
                            password_encriptada = stauth.Hasher([password]) \
                      .generate()
                            insertar_usuario(email, username, dob_str,
                                            password_encriptada[0])
                            st.success("Cuenta creada con exito!")
                        else:
                            st.warning("Nombre de usuario en uso")
                    else:
                        st.warning("Nombre de usuario invalido"
                        "(solo debe tener letras y numeros)")
                else:
                    st.warning("El email ya esta en uso")
            else:
                st.warning("Email invalido")
        else:
            st.warning("Debe rellenar todos los campos")
    else:
        st.warning("Debes aceptar los terminos y condiciones antes de poder registrarte")


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
