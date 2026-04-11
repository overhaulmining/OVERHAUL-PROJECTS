import uuid
import streamlit as st
import pandas as pd
from streamlit_cookies_controller import CookieController
from db import supabase
from rol_pages import pages_roles
import os
from dotenv import load_dotenv
import time

load_dotenv()

# # Instancia global del controlador de cookies

# # Configuración de entorno de desarrollo
dev_env_value = os.getenv('DEV', 'False')
DEV = dev_env_value.lower() in ('true', '1', 't', 'y', 'yes')
rol_dev = "admin"

# def restaurar_sesion():
#     """Sincroniza las cookies con el session_state al iniciar"""
#     usuario_cookie = controller.get("usuario")
#     rol_cookie = controller.get("rol")
#     session_id_cookie = controller.get("session_id")

#     if usuario_cookie and "usuario" not in st.session_state:
#         # Validamos en DB si la sesión de la cookie sigue activa
#         if validar_sesion(session_id_cookie):
#             st.session_state["usuario"] = usuario_cookie
#             st.session_state["rol"] = rol_cookie
#             st.session_state["session_id"] = session_id_cookie

def guardar_sesion(usuario, rol, controller):
    """Establece cookies, session_state y registro en DB"""
    session_id = str(uuid.uuid4())

    # 2. Guardar en Cookies (Persistente)
    controller.set("session_id", session_id)
    controller.set("usuario", usuario)
    controller.set("rol", rol)
    
    # 3. Registrar en Supabase
    supabase.table("sessions").insert({
        "session_id": session_id,
        "user": usuario,
        "rol": rol,
        "active": True
    }).execute()
    
# def validar_sesion(session_id):
#     """Verifica si el ID de sesión existe y está activo en la DB"""
#     if not session_id:
#         return False
#     res = supabase.table("sessions")\
#         .select("*")\
#         .eq("session_id", session_id)\
#         .eq("active", True)\
#         .execute()
#     return len(res.data) > 0
    
def cerrar_sesion(controller):
    """Limpia cookies, estado local y desactiva sesión en DB"""
    session_id = controller.get("session_id")
    if session_id:
        supabase.table("sessions")\
            .update({"active": False})\
            .eq("session_id", session_id)\
            .execute()

    controller.set("usuario", None)
    controller.set("rol", None)
    controller.set("session_id", None)
    st.session_state.clear()

    st.toast("Sesión cerrada")

    time.sleep(0.3)
    st.rerun()

def validarUsuario(usuario, clave, controller):
    """Valida credenciales contra la tabla de usuarios"""
    response = supabase.table("users")\
        .select("*")\
        .eq("user", usuario)\
        .eq("password", clave)\
        .execute()

    if response.data:
        guardar_sesion(usuario, response.data[0]["rol"], controller)
        return True
    return False

def generarMenu(usuario, controller):
    """Menú manual basado en lógica de roles directa"""
    rol = controller.get('rol')
    with st.sidebar:
        st.write(f"Hola **:blue-background[{usuario}]**")
        st.caption(f"Rol: {rol}")
        st.page_link("inicio.py", label="Inicio", icon=":material/home:")
        st.subheader("Tableros")
        
        if rol in ['ventas','admin','comercial']:
            st.page_link("pages/Gestion_Personal.py", label="Ventas", icon=":material/sell:")
        if rol in ['compras','admin','comercial']:
            st.page_link("pages/Detalle_Personal.py", label="Compras", icon=":material/shopping_cart:")
        if rol in ['personal','admin','compras']:
            st.page_link("pages/Configuracion.py", label="Personal", icon=":material/group:")
        if rol in ['contabilidad','admin']:
            st.page_link("pages/Nuevo_Personal.py", label="Contabilidad", icon=":material/payments:")
        
        if st.button("Salir", key="btn_salir_manual"):
            cerrar_sesion(controller)

def validarPagina(pagina, usuario, controller):
    """Control de seguridad por página"""
    rol = controller.get('rol')
    dfPagina = pages_roles[pages_roles["pagina"] == pagina]

    if len(dfPagina) > 0:
        roles_permitidos = dfPagina["roles"].values[0]
        return rol in roles_permitidos or rol == "admin" or st.secrets.get("tipoPermiso") == "rol"
    return False

def generarMenuRoles(usuario, controller):
    """Menú dinámico basado en el archivo rol_pages"""
    rol = controller.get('rol')
    with st.sidebar:
        st.write(f"Hola **:blue-background[{usuario}]**")
        st.caption(f"Rol: {rol}")
        
        ocultar_opciones = st.secrets.get("ocultarOpciones") == "True"

        if ocultar_opciones:
            pages_filtradas = pages_roles[
                pages_roles["roles"].apply(lambda r: rol in r or rol == "admin")
            ]
            for _, row in pages_filtradas.iterrows():
                if row.get("sidebar", True):
                    st.page_link(row["pagina"], label=row["nombre"], icon=f":material/{row['icono']}:")
        else:
            for _, row in pages_roles.iterrows():
                deshabilitar = not (rol in row["roles"] or rol == "admin")
                st.page_link(row["pagina"], label=row["nombre"], icon=f":material/{row['icono']}:", disabled=deshabilitar)

        if st.button("Salir", key="btn_salir_roles"):
            cerrar_sesion(controller)

# def generarLogin(archivo):
#     """Punto de entrada principal para el login y menús"""
#     restaurar_sesion()
    
#     if DEV:
#         if "usuario" not in st.session_state:
#             st.session_state["usuario"] = "admin"
#             st.session_state["rol"] = rol_dev
        
#         menu_type = st.secrets.get("tipoPermiso")
#         generarMenuRoles(st.session_state["usuario"]) if menu_type == "rolpagina" else generarMenu(st.session_state["usuario"])
#         return

#     # Si hay una sesión activa, verificar que sea válida en DB
#     session_id = st.session_state.get("session_id")
#     if session_id and not validar_sesion(session_id):
#         cerrar_sesion()

#     if 'usuario' in st.session_state:
#         menu_type = st.secrets.get("tipoPermiso")
#         generarMenuRoles(st.session_state['usuario']) if menu_type == "rolpagina" else generarMenu(st.session_state['usuario'])
        
#         if not validarPagina(archivo, st.session_state['usuario']):
#             st.error(f"Acceso denegado a: {archivo}", icon=":material/gpp_maybe:")
#             st.stop()
#     else:
#         with st.form('frmLogin'):
#             parUsuario = st.text_input('Usuario')
#             parPassword = st.text_input('Password', type='password')
#             if st.form_submit_button('Ingresar', type='primary'):
#                 if validarUsuario(parUsuario, parPassword):
#                     st.rerun()
#                 else:
#                     st.error("Credenciales incorrectas", icon=":material/gpp_maybe:")

# def restaurar_sesion():
#     """Sincroniza las cookies con el session_state al iniciar"""
#     usuario_cookie = controller.get("usuario")
#     rol_cookie = controller.get("rol")
#     session_id_cookie = controller.get("session_id")

#     if usuario_cookie and "usuario" not in st.session_state:
#         # Validamos en DB si la sesión de la cookie sigue activa
#         if validar_sesion(session_id_cookie):
#             st.session_state["usuario"] = usuario_cookie
#             st.session_state["rol"] = rol_cookie
#             st.session_state["session_id"] = session_id_cookie


def generarLogin(archivo):
    controller = CookieController()
    
    session_id = controller.get("session_id")
    
    if session_id == None:
        with st.form('frmLogin'):
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Password', type='password')
            
            if st.form_submit_button('Ingresar', type='primary'):
                if validarUsuario(parUsuario, parPassword, controller):
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas", icon=":material/gpp_maybe:")
    usuario = controller.get("usuario")
    rol = controller.get("rol")

    if usuario:
        menu_type = st.secrets.get("tipoPermiso")
        generarMenuRoles(usuario, controller) if menu_type == "rolpagina" else generarMenu(usuario)
        if not validarPagina(archivo, controller.get("usuario"), controller):
            st.error(f"Acceso denegado a: {archivo}", icon=":material/gpp_maybe:")
            st.stop()
            
def existUser():
    controller = CookieController()
    usuario = controller.get("usuario")
    if usuario:
        return True
    else:
        return False