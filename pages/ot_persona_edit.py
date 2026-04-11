import uuid

import streamlit as st
from db import supabase
import login as login
import pandas as pd
from streamlit_redirect import redirect
from pages.editar_equipo import editar_ot
from pages.nuevo_equipo import agregar_nuevo_equipo

login.generarLogin("pages/ot_persona_edit.py")

if login.existUser():
    
    st.set_page_config(page_title="Editar OT", layout="wide")
    
    params = st.experimental_get_query_params() if hasattr(st, "experimental_get_query_params") else st.query_params
    id_ot_persona = params.get("id_ot_persona", [""])
    
    res_ot = (
        supabase
        .table("ot_personas")
        .select("ordenes_trabajo(n_ot), *")
        .eq("id_ot_persona",id_ot_persona)
        .execute()
    )
    
    ot = pd.json_normalize(res_ot.data[0])
    n_ot = ot['ordenes_trabajo.n_ot'][0]
    st.subheader(f"Orden {n_ot}")
    
    with st.form("editar_ot"):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Empresa / Proyecto", "Datos Personal", "Curso", "Resultados", "Costos"])
        
        empresas_list = supabase.table("empresas").select("*").execute()
        empresas_df = pd.DataFrame(empresas_list.data)

        # Creamos un diccionario {nombre_empresa: ruc}
        empresa_ruc_map = dict(zip(empresas_df['razon_social'], empresas_df['ruc']))

        # Lista de nombres de empresas
        empresa_nombres = list(empresa_ruc_map.keys())
        
        cursos_list = supabase.table("cursos").select("nombre_curso").execute()
        cursos_df = pd.DataFrame(cursos_list.data)
        cursos = cursos_df["nombre_curso"].to_list()

        with tab1:
            # Selectbox para razón social
            
            input1, input2 = st.columns([2,1])
            empresa_seleccionada = input1.selectbox(
                "Empresa",
                empresa_nombres,
                index=empresa_nombres.index(ot["empresa"][0]) if ot["empresa"][0] in empresa_nombres else 0
            )
        
            # Auto-completar RUC según la empresa seleccionada
            ruc = input2.text_input(
                "RUC",
                value=empresa_ruc_map.get(empresa_seleccionada, "")
            )
            input1, input2 = st.columns(2)
            
            proyecto = input1.text_input("Proyecto")
            
            modalidad = input2.selectbox("Modalidad", ["Presencial", "Virtual"])
            
        with tab2:
            col1, col2, col3 = st.columns([2,2,1])
            nombres = col1.text_input("Nombres")    
            apellidos = col2.text_input("Apellidos")
            dni = col3.text_input("DNI", max_chars=8)
        
        with tab3:
            col1, col2 = st.columns(2)
            cursos = col1.selectbox("Cursos",cursos)
            instructor = col2.text_input("Instructor")
            
            col1, col2, col3 = st.columns(3)
            fecha_curso = col1.date_input("Fecha")
            n_veces = col2.selectbox("N° veces", ["1","2","3"])
            opciones_certificadora = ["OVERHAUL", "PREXA"]
            certificadora = col3.selectbox(
                "Certificadora",
                opciones_certificadora,
                index=opciones_certificadora.index(ot["certificadora"][0]) if ot["certificadora"][0] in opciones_certificadora else 0
            )
        with tab4:
            aprobo = st.selectbox("Aprobó?", ["Si", "No"])
            
            url_certificado =ot["certificado"][0]
        
            if url_certificado:
                st.markdown(f"[📄 Ver Certificado]({url_certificado})", unsafe_allow_html=True)
            
            certificado = st.file_uploader("Certificado")
            comentarios = st.text_area("Comentarios")

        with tab5:
            col1, col2 = st.columns(2)
            costo_soles = col1.number_input("Costo Soles")
            costo_dolares = col2.number_input("Costo Dolares")

        submit = st.form_submit_button("Guardar cambios")
    
    if submit:
        
        if certificado:
                nombre_archivo = f"personas/{n_ot}/certificado_{uuid.uuid4()}.pdf"
                supabase.storage.from_("ordenes_trabajo").upload(
                    nombre_archivo, certificado.getvalue(), {"content-type": "application/pdf"}
                )
                url_certificado = supabase.storage.from_("ordenes_trabajo").get_public_url(nombre_archivo)

        supabase.table("ot_personas").update({
            "empresa" : empresa_seleccionada,
            "ruc" : ruc,
            "certificadora" : certificadora,
            "modalidad": modalidad,
            "cursos" : cursos,
            "nombres" : nombres,
            "apellidos" : apellidos,
            "dni": dni,
            "fecha" : fecha_curso.isoformat(),
            "aprobo" : True if aprobo == "Si" else False,
            "certificadora" : certificadora,
            "proyecto" : proyecto,
            "instructor" : instructor,
            "certificado" : url_certificado,
            "n_veces" : n_veces,
            "costo_soles" : float(costo_soles),
            "costo_dolares" : float(costo_dolares),
            "comentarios" : comentarios
            
        }).eq("id_ot_persona", id_ot_persona).execute()

        st.success("Orden actualizada correctamente")

    