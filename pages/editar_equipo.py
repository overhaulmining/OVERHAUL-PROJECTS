import streamlit as st
from db import supabase
import uuid
from login import existUser

@st.dialog("✏️ Editar Equipo")
def editar_ot():

    equipo = st.session_state.equipo_select
    n_ot = st.session_state.n_ot
    with st.form("form_editar_ot"):

        tipo_unidad = st.text_input(
            "Tipo Unidad",
            value=equipo.get("tipo_unidad", "")
        )

        tipos_servicios = ["NDT", 'IZAJE', 'Mantto Industrial', 'Faraday', 'Metrología', 'Cálculo estructural']
        tipo_servicio = st.selectbox(
            "Tipo Servicio",
            tipos_servicios,
            index=tipos_servicios.index(equipo["tipo_servicio"]) if equipo["tipo_servicio"] in tipos_servicios else 0
        )
        
        fecha_servicio = st.date_input(
            "Fecha Servicio",
            value=equipo["fecha_servicio"]
        )

        placa = st.text_input(
            "Placa",
            value=equipo.get("placa", "")
        )
        
        inspector = st.text_input(
            "Inspector",
            value=equipo.get("inspector", "")
        )
        
        ubicacion = st.text_input(
            "Ubicación",
            value=equipo.get("ubicacion", "")
        )
        
        url_informe_campo = equipo.get("informe_campo", "")

        # Mostrar enlace si existe
        if url_informe_campo:
            st.markdown(f"[📄 Ver Informe Campo]({url_informe_campo})", unsafe_allow_html=True)
                
        informe_campo = st.file_uploader(
            "Subir nuevo Informe Campo (PDF)",
            type=["pdf"]
        )
        
        url_informe_final = equipo.get("informe_final", "")

        # Mostrar enlace si existe
        if url_informe_final:
            st.markdown(f"[📄 Ver Informe Final]({url_informe_final})", unsafe_allow_html=True)
        
        informe_final = st.file_uploader(
            "Subir nuevo Informe Final (PDF)",
            type=["pdf"]
        )
        
        url_certificado = equipo.get("certificado", "")
        
        if url_certificado:
            st.markdown(f"[📄 Ver Certificado]({url_certificado})", unsafe_allow_html=True)
        
        
        certificado = st.file_uploader(
            "Subir nuevo Certificado (PDF)",
            type=["pdf"]
        )
        
        descripcion_servicio = st.text_input(
            "Descripcion servicio",
            value=equipo.get("descripcion_servicio", "")
        )

        col1, col2 = st.columns(2)

        guardar = col1.form_submit_button("💾 Guardar")
        cancelar = col2.form_submit_button("❌ Cancelar")

        if guardar:
            # -------- subir informe campo ----------
            if informe_campo:

                nombre_archivo = f"equipos/{n_ot}/informe_campo_{uuid.uuid4()}.pdf"

                supabase.storage.from_("ordenes_trabajo").upload(
                    nombre_archivo,
                    informe_campo.getvalue(),
                    {"content-type": "application/pdf"}
                )

                url_informe_campo = supabase.storage.from_("ordenes_trabajo").get_public_url(nombre_archivo)
            
                
            if informe_final:

                nombre_archivo = f"equipos/{n_ot}/informe_final_{uuid.uuid4()}.pdf"

                supabase.storage.from_("ordenes_trabajo").upload(
                    nombre_archivo,
                    informe_final.getvalue(),
                    {"content-type": "application/pdf"}
                )

                url_informe_final = supabase.storage.from_("ordenes_trabajo").get_public_url(nombre_archivo)

            if certificado:

                nombre_archivo = f"equipos/{n_ot}/certificado_{uuid.uuid4()}.pdf"

                supabase.storage.from_("ordenes_trabajo").upload(
                    nombre_archivo,
                    certificado.getvalue(),
                    {"content-type": "application/pdf"}
                )

                url_certificado = supabase.storage.from_("ordenes_trabajo").get_public_url(nombre_archivo)

            supabase.table("equipos").update({
                "tipo_unidad": tipo_unidad,
                "tipo_servicio": tipo_servicio,
                "fecha_servicio" : fecha_servicio.isoformat(),
                "placa": placa,
                "inspector": inspector,
                "ubicacion" :ubicacion,
                "informe_campo": url_informe_campo,
                "informe_final": url_informe_final,
                "certificado": url_certificado,
                "descripcion_servicio" : descripcion_servicio,
            }).eq("id", equipo["id"]).execute()

            st.success("Orden actualizada")
            st.rerun()

        if cancelar:
            st.rerun()
            st.session_state.edit_mode = False
            st.rerun()
