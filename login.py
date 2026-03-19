# Importamos las librerías necesarias
import streamlit as st  # Librería para crear aplicaciones web interactivas. Instalación: pip install streamlit
import pandas as pd  # Librería para manipulación y análisis de datos. Instalación: pip install pandas
from streamlit_cookies_controller import CookieController # Librería para manejar cookies en Streamlit. Instalación: pip install streamlit-cookies-controller
from db import supabase
from rol_pages import pages_roles

# Creamos una instancia de CookieController
controller = CookieController()
DEV = True
rol_dev="sys"

def restaurar_sesion():
    usuario_cookie = controller.get("usuario")
    rol_cookie = controller.get("rol")

    if usuario_cookie and "usuario" not in st.session_state:
        st.session_state["usuario"] = usuario_cookie
        st.session_state["rol"] = rol_cookie

def validarUsuario(usuario,clave):    
    """Permite la validación de usuario y clave

    Args:
        usuario (str): usuario a validar
        clave (str): clave del usuario

    Returns:
        bool: True usuario valido, False usuario invalido
    """    
    # Leemos el archivo csv con los usuarios y claves
    
    response = (
        supabase
        .table("users")
        .select("*")
        .eq("user", usuario)
        .eq("password", clave)
        .execute()
    )
    
    # Filtramos el dataframe para buscar el usuario y la clave
    print(response.data)
    if response.data:
        # Si el usuario y la clave existen, retornamos True
        # Set a cookie
        controller.set('usuario', usuario)
        controller.set('rol', response.data[0]["rol"])
        
        return True
    else:
        # Si el usuario o la clave no existen, retornamos False
        return False

# Generación de menú según el usuario y el rol se maneja desde el código
def generarMenu(usuario):
    """Genera el menú dependiendo del usuario y el rol

    Args:
        usuario (str): usuario utilizado para generar el menú
    """        
    with st.sidebar: # Creamos una barra lateral para el menú
        # Cargamos la tabla de usuarios

        # Cargamos el nombre del usuario
        nombre=controller.get('usuario')
        # Cargamos el rol
        rol= controller.get('rol')
        #Mostramos el nombre del usuario
        st.write(f"Hola **:blue-background[{nombre}]** ") # Mostramos el nombre del usuario con formato
        st.caption(f"Rol: {rol}") # Mostramos el rol del usuario
        # Mostramos los enlaces de páginas
        st.page_link("inicio.py", label="Inicio", icon=":material/home:") # Enlace a la página de inicio
        st.subheader("Tableros") # Subtítulo para los tableros
        # Mostramos los enlaces a las páginas según el rol del usuario
        if rol in ['ventas','admin','comercial']:
            st.page_link("pages/Gestion_Personal.py", label="Ventas", icon=":material/sell:") # Enlace a la página de ventas        
        if rol in ['compras','admin','comercial']:
            st.page_link("pages/Detalle_Personal.py", label="Compras", icon=":material/shopping_cart:") # Enlace a la página de compras
        if rol in ['personal','admin','compras']:
            st.page_link("pages/Configuracion.py", label="Personal", icon=":material/group:") # Enlace a la página de personal   
        if rol in ['contabilidad','admin']:
            st.page_link("pages/Nuevo_Personal.py", label="Contabilidad", icon=":material/payments:") # Enlace a la página de contabilidad    
        # Botón para cerrar la sesión
        btnSalir=st.button("Salir") # Creamos un botón para salir
        if btnSalir: # Si se presiona el botón
            st.session_state.clear() # Limpiamos las variables de sesión
            # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
            st.rerun() # Reiniciamos la aplicación


# Validación de acceso a la página según los roles del usuario
def validarPagina(pagina,usuario):
    """Valida si el usuario tiene permiso para acceder a la página

    Args:
        pagina (str): página a validar
        usuario (str): usuario a validar

    Returns:
        bool: True si tiene permiso, False si no tiene permiso
    """
    
    rol= controller.get('rol')
    # Filtrar la página
    dfPagina = pages_roles[pages_roles["pagina"] == pagina]

    # Validamos si existe la página
    if len(dfPagina) > 0:
        roles_permitidos = dfPagina["roles"].values[0]

        if rol in roles_permitidos or rol == "admin" or st.secrets["tipoPermiso"] == "rol":
            return True
        else:
            return False
    else:
        return False

# Generación de menú según el usuario y el rol se maneja desde un archivo csv
def generarMenuRoles(usuario):
    """Genera el menú dependiendo del usuario y el rol asociado a la página"""

    with st.sidebar:

        usuario = controller.get("usuario")
        rol = controller.get("rol")

        if usuario:
            st.write(f"Hola **:blue-background[{usuario}]**")

        st.caption(f"Rol: {rol}")
        # st.subheader("Opciones")

        ocultar_opciones = st.secrets["ocultarOpciones"] == "True"

        # --- OPCION 1: OCULTAR PÁGINAS SIN PERMISO ---
        if ocultar_opciones:

            pages_filtradas = pages_roles[
                pages_roles["roles"].apply(lambda r: rol in r or rol == "admin")
            ]

            for _, row in pages_filtradas.iterrows():
                
                if row["sidebar"]== False:
                    pass
                else:
                    st.page_link(
                        row["pagina"],
                        label=row["nombre"],
                        icon=f":material/{row['icono']}:"
                    )

        # --- OPCION 2: MOSTRAR TODAS PERO DESHABILITAR ---
        else:

            for _, row in pages_roles.iterrows():

                deshabilitar = not (rol in row["roles"] or rol == "admin")

                st.page_link(
                    row["pagina"],
                    label=row["nombre"],
                    icon=f":material/{row['icono']}:",
                    disabled=deshabilitar
                )

        # --- BOTÓN SALIR ---
        if st.button("Salir"):
            st.session_state.clear()
            controller.remove("usuario")
            st.rerun()
            
# Generación de la ventana de login y carga de menú
def generarLogin(archivo):
    """Genera la ventana de login o muestra el menú si el login es valido
    """    
    restaurar_sesion()
    
    if DEV:
        if "usuario" not in st.session_state:
            st.session_state["usuario"] = "admin"
            st.session_state["rol"] = rol_dev
            controller.set('usuario', "admin")
            controller.set('rol', rol_dev)

        # cargar menú igual que si estuviera logueado
        if st.secrets["tipoPermiso"] == "rolpagina":
            generarMenuRoles(st.session_state["usuario"])
        else:
            generarMenu(st.session_state["usuario"])

        return
    
    if 'usuario' in st.session_state: # Verificamos si la variable usuario esta en el session state
        
        # Si ya hay usuario cargamos el menu
        if st.secrets["tipoPermiso"]=="rolpagina":
            generarMenuRoles(st.session_state['usuario']) # Generamos el menú para la página
        else:
            generarMenu(st.session_state['usuario']) # Generamos el menú del usuario       
        if validarPagina(archivo,st.session_state['usuario'])==False: # Si el usuario existe, verificamos la página        
            st.error(f"No tiene permisos para acceder a esta página {archivo}",icon=":material/gpp_maybe:")
            st.stop() # Detenemos la ejecución de la página
    else: # Si no hay usuario
        # Cargamos el formulario de login       
        with st.form('frmLogin'): # Creamos un formulario de login
            parUsuario = st.text_input('Usuario') # Creamos un campo de texto para usuario
            parPassword = st.text_input('Password',type='password') # Creamos un campo para la clave de tipo password
            btnLogin=st.form_submit_button('Ingresar',type='primary') # Botón Ingresar
            if btnLogin: # Verificamos si se presiono el boton ingresar
                if validarUsuario(parUsuario,parPassword): # Verificamos si el usuario y la clave existen
                    st.session_state['usuario'] =parUsuario # Asignamos la variable de usuario
                    # Si el usuario es correcto reiniciamos la app para que se cargue el menú
                    st.rerun() # Reiniciamos la aplicación
                else:
                    # Si el usuario es invalido, mostramos el mensaje de error
                    st.error("Usuario o clave inválidos",icon=":material/gpp_maybe:") # Mostramos un mensaje de error                    