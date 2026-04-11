import streamlit as st
from datetime import date
import pandas as pd
from db import supabase


st.title("📝 Inscripciones de Personas")

with st.form("form_inscripcion", clear_on_submit=True):
    col1, col2 = st.columns(2)
    cursos_list = supabase.table("cursos").select("nombre_curso").execute()
    cursos_df = pd.DataFrame(cursos_list.data)
    cursos = cursos_df["nombre_curso"].to_list()
    
    empresas_list = supabase.table("empresas").select("*").execute()
    empresas_df = pd.DataFrame(empresas_list.data)

    # Creamos un diccionario {nombre_empresa: ruc}
    empresa_ruc_map = dict(zip(empresas_df['razon_social'], empresas_df['ruc']))

    # Lista de nombres de empresas
    empresa_nombres = list(empresa_ruc_map.keys())
    
    with col1:
        dni = st.text_input("DNI / CE")
        nombres = st.text_input("Nombres")
        apellidos = st.text_input("Apellidos")
    
    with col2:
        curso = st.selectbox("Curso", cursos)
        empresa = st.selectbox("Empresa a la que pertenece", empresa_nombres)
        telefono = st.text_input("Teléfono de contacto", max_chars=9)
    
    # El usuario marca su propia fecha aquí
    fecha_prog = st.date_input("Fecha Programada", value=date.today())

    submit = st.form_submit_button("Registrar Inscripción")

    if submit:
        if dni and nombres and apellidos:
            data_ins = {
                "dni": dni,
                "nombres": nombres,
                "apellidos": apellidos,
                "curso": curso,
                "empresa": empresa,
                "telefono": telefono,
                "fecha_programada": str(fecha_prog)
            }
            
            try:
                res = supabase.table("inscripciones").insert(data_ins).execute()
                st.success(f"✅ Inscripción registrada para {nombres} {apellidos}")
            except Exception as e:
                st.error(f"Error al guardar: {e}")
        else:
            st.warning("Por favor, completa los campos obligatorios (DNI, Nombres, Apellidos).")
