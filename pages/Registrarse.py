# Importar librerias necesarias
import streamlit as st
import streamlit_extras
import streamlit_authenticator as stauth
import re
from deta import Deta
from datetime import datetime



# Formulario de registro con los datos que debe ingresar el usuario
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

# Manejo de posibles errores


# Se crea el diccionario credentials necesario para el
# funcionamiento del autenticador de cuentas


# Crear pie de pagina con los datos de contacto de los creadores
footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
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
</div>
"""
