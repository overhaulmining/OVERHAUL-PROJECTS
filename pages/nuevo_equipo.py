import uuid
import streamlit as st
from db import supabase
import login as login
import pandas as pd


@st.dialog("➕ Agregar Nuevo Equipo")
def agregar_nuevo_equipo():
    
    n_ot = st.session_state.get("n_ot")
    id_ot_equipo = st.session_state.id_ot_equipo
    with st.form("form_nuevo_equipo"):

        tipo_unidad = st.text_input("Tipo Unidad", value="", key="tipo_unidad")

        tipos_servicios = ["NDT", 'IZAJE', 'Mantto Industrial', 'Faraday', 'Metrología', 'Cálculo estructural']
        tipo_servicio = st.selectbox("Tipo Servicio", tipos_servicios, index=0)

        fecha_servicio = st.date_input("Fecha Servicio")

        placa = st.text_input("Placa", key="placa")
        inspector = st.text_input("Inspector", key="inspector")
        ubicacion = st.text_input("Ubicación", key="ubicacion")

        informe_campo = st.file_uploader("Subir Informe Campo (PDF)", type=["pdf"])
        informe_final = st.file_uploader("Subir Informe Final (PDF)", type=["pdf"])
        certificado = st.file_uploader("Subir Certificado (PDF)", type=["pdf"])

        descripcion_servicio = st.text_input("Descripcion servicio")

        col1, col2 = st.columns(2)
        guardar = col1.form_submit_button("💾 Guardar")
        cancelar = col2.form_submit_button("❌ Cancelar")

        if guardar:
            # Subir archivos a Supabase y obtener URLs públicas
            url_informe_campo, url_informe_final, url_certificado = "", "", ""

            if informe_campo:
                nombre_archivo = f"equipos/{n_ot}/informe_campo_{uuid.uuid4()}.pdf"
                supabase.storage.from_("ordenes_trabajo").upload(
                    nombre_archivo, informe_campo.getvalue(), {"content-type": "application/pdf"}
                )
                url_informe_campo = supabase.storage.from_("ordenes_trabajo").get_public_url(nombre_archivo)

            if informe_final:
                nombre_archivo = f"equipos/{n_ot}/informe_final_{uuid.uuid4()}.pdf"
                supabase.storage.from_("ordenes_trabajo").upload(
                    nombre_archivo, informe_final.getvalue(), {"content-type": "application/pdf"}
                )
                url_informe_final = supabase.storage.from_("ordenes_trabajo").get_public_url(nombre_archivo)

            if certificado:
                nombre_archivo = f"equipos/{n_ot}/certificado_{uuid.uuid4()}.pdf"
                supabase.storage.from_("ordenes_trabajo").upload(
                    nombre_archivo, certificado.getvalue(), {"content-type": "application/pdf"}
                )
                url_certificado = supabase.storage.from_("ordenes_trabajo").get_public_url(nombre_archivo)

            # Insertar nuevo registro en la tabla
            res_new = supabase.table("equipos").insert({
                "tipo_unidad": tipo_unidad,
                "tipo_servicio": tipo_servicio,
                "fecha_servicio" : fecha_servicio.isoformat(),
                "placa": placa,
                "inspector": inspector,
                "ubicacion": ubicacion,
                "informe_campo": url_informe_campo,
                "informe_final": url_informe_final,
                "certificado": url_certificado,
                "descripcion_servicio": descripcion_servicio,
                "ot_equipo_id" : int(id_ot_equipo)
            }).execute()

            # Mostrar toast y refrescar
            st.toast("Nuevo equipo agregado ✅")
            st.session_state["edit_mode"] = False
            st.rerun()

        if cancelar:
            st.session_state["edit_mode"] = False
            st.rerun()