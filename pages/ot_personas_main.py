import streamlit as st
from db import supabase
import login as login
import pandas as pd
from streamlit_redirect import redirect

login.generarLogin("pages/ot_personas_main.py")
if login.existUser():

    st.set_page_config(page_title="OT Personas", layout="wide")

    col1, col2 = st.columns([4,1])

    with col1:
        st.header("OT Personas")

    with col2:
        if st.button("➕ Nueva OT"):
            res_new_ot = supabase.table("ordenes_trabajo").insert({}).execute()
            
            if res_new_ot:
                new_ot_id = res_new_ot.data[0]["id"]
                new_ot_n_ot = res_new_ot.data[0]["n_ot"]
            
            res_new_ot_eq = supabase.table("ot_personas").insert({"ot_id": new_ot_id}).execute()
            id_res_new_ot_eq = res_new_ot_eq.data[0]["id_ot_persona"]
            st.toast(f"Se creó nueva OT: {new_ot_n_ot}",icon="✅")
            st.session_state["id_ot_persona"] = id_res_new_ot_eq
            redirect(f"ot_persona_edit?id_ot_persona={id_res_new_ot_eq}")

    response = (
        supabase
        .table("ot_personas")
        .select("ordenes_trabajo(n_ot), *")
        .execute()
    )

    df = pd.json_normalize(response.data)
    
    if not df.empty:
        # dataframe visible
        ot_personas = df.drop(columns=[
            "created_at",
            "ordenes_trabajo.created_at",
            "ot_id",
            "id_ot_equipo"
        ], errors="ignore")
        
        ot_equipos = ot_personas.rename(columns={
            "ordenes_trabajo.n_ot": "N° Orden",
            "fecha_servicio": "Fecha Servicio",
        })
        
            
        boton_detalle = st.empty()

        event = st.dataframe(
            df,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row"
        )

        seleccion = event.selection.rows

        if seleccion:

            indice = seleccion[0]

            # usamos df original para no perder el id
            ot_equipo = df.iloc[indice]

            with boton_detalle:
                if st.button("✏️ Editar OT"):
                    redirect(f"ot_persona_edit?id_ot_persona={ot_equipo["id_ot_persona"]}")
                    
    else:
        st.info("No hay órdenes registradas.")
