import streamlit as st

# Credenciales de usuario (solo para fines de demostración, no utilizar en un entorno de producción)
credenciales = {"usuario1": "contrasena1", "usuario2": "contrasena2"}

def login(username, password):
    """
    Función de inicio de sesión simple.
    """
    if username in credenciales and credenciales[username] == password:
        return True
    return False

def main():
    st.title("Inicio de Sesión")

    # Formulario de inicio de sesión
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        if login(username, password):
            st.success(f"Bienvenido, {username}!")
            # Agrega el contenido de la aplicación después del inicio de sesión exitoso.
            st.write("Aquí va el contenido de tu aplicación.")
        else:
            st.error("Credenciales incorrectas. Por favor, inténtalo de nuevo.")

if __name__ == "__main__":
    main()
