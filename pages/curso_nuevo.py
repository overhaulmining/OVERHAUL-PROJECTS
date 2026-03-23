import streamlit as st
from db import supabase
from datetime import date
import login as login

# Asumiendo que ya tienes el login cargado arriba
login.generarLogin("pages/curso_nuevo.py")

st.header("📝 Registrar Nuevo Curso")

if 'usuario' in st.session_state:
    with st.form("form_curso_nuevo", clear_on_submit=True):
        # Fila 1: Nombre y Título
        col1, col2 = st.columns(2)
        with col1:
            nombre_curso = st.text_input("Nombre del Curso (Interno)", placeholder="Nuevo curso")

        # Fila 2: Fechas
        col3, col4 = st.columns(2)
        with col3:
            fecha_inicio = st.date_input("Fecha de Inicio", value=date.today())
        with col4:
            fecha_final = st.date_input("Fecha de Finalización", value=date.today())

        # Fila 3: Imagen y Descripción
        src_portada = st.text_input("URL de la Imagen de Portada", placeholder="https://ejemplo.com/imagen.jpg")
        descripcion = st.text_area("Descripción del Curso", placeholder="Escribe aquí de qué trata el curso...")

        submit = st.form_submit_button("🚀 Crear Curso")

        if submit:
            # Validación básica
            if nombre_curso and descripcion:
                if fecha_final < fecha_inicio:
                    st.error("❌ Error: La fecha final no puede ser anterior a la de inicio.")
                else:
                    data_ins = {
                        "nombre_curso": nombre_curso,
                        "src_portada": src_portada,
                        "descripcion": descripcion,
                        "fecha_inicio": str(fecha_inicio),
                        "fecha_final": str(fecha_final)
                    }

                    try:
                        with st.spinner("Guardando curso..."):
                            res = supabase.table("cursos").insert(data_ins).execute()
                            st.success(f"✅ ¡Curso '{nombre_curso}' creado exitosamente!")
                    except Exception as e:
                        if "23505" in str(e):
                            st.error("Error: Problema de duplicados en la base de datos.")
                        else:
                            st.error(f"Error al guardar: {e}")
            else:
                st.warning("⚠️ Por favor, completa todos los campos obligatorios (Nombre, Título y Descripción).")