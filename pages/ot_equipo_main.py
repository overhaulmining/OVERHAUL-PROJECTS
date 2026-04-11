import streamlit as st
from db import supabase
import login as login
import pandas as pd

login.generarLogin("pages/ot_equipo_main.py")

if login.existUser():

    st.set_page_config(page_title="Orden Trabajo Equipo", layout="wide")
    
    col1, col2 = st.columns([4,1])

    with col1:
        st.header("OT Equipos")

    with col2:
        if st.button("➕ Nueva OT"):
            res_new_ot = supabase.table("ordenes_trabajo").insert({}).execute()

            if res_new_ot:
                new_ot_id = res_new_ot.data[0]["id"]
                new_ot_n_ot = res_new_ot.data[0]["n_ot"]
                
                res_new_ot_eq = supabase.table("ot_equipos").insert({"ot_id": new_ot_id, "estado": "Pendiente"}).execute()
                id_res_new_ot_eq = res_new_ot_eq.data[0]["id_ot_equipo"]
                st.toast(f"Se creó nueva OT: {new_ot_n_ot}",icon="✅")
                st.session_state["id_ot_equipo"] = id_res_new_ot_eq
                # Cambiar de página
                st.switch_page("pages/ot_equipo_edit.py")
            else:
                st.error("Error al crear la OT")

    response = (
        supabase
        .table("ot_equipos")
        .select("ordenes_trabajo(n_ot), *")
        .execute()
    )

    df = pd.json_normalize(response.data)

    # dataframe visible
    ot_equipos = df.drop(columns=[
        "created_at",
        "ordenes_trabajo.created_at",
        "ot_id",
        "id_ot_equipo"
    ], errors="ignore")
    

    ot_equipos = ot_equipos.rename(columns={
        "ordenes_trabajo.n_ot": "N° Orden",
        "fecha_servicio": "Fecha Servicio",
    })
    
    res_equipos = (
        supabase
        .table("ot_equipos")
        .select(
            "id_ot_equipo, ot_id, empresa, ruc, fecha_servicio, certificadora, "
            "equipos(id, tipo_unidad, tipo_servicio, placa, inspector), "
            "ordenes_trabajo(n_ot)"
        )
        .execute()
    )
    
    df_equipos = pd.json_normalize(
        res_equipos.data,
        record_path=['equipos'],  # desanida la lista de equipos
        meta=["id_ot_equipo",'ot_id', 'empresa', 'ruc', 'fecha_servicio', 'certificadora', ['ordenes_trabajo','n_ot']],
        errors='ignore'
    )


    tab1, tab2 = st.tabs(["Ordenes Trabajo", "Equipos"])

    with tab1:
        
        boton_detalle = st.empty()

        event = st.dataframe(
            ot_equipos,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row"
        )

        seleccion = event.selection.rows

        if seleccion:

            indice = seleccion[0]

            # usamos df original para no perder el id
            ot_equipo = df.iloc[indice]
            st.session_state["id_ot_equipo"] = ot_equipo["id_ot_equipo"]

            with boton_detalle:
                if st.button("✏️ Editar OT"):
                    st.switch_page("pages/ot_equipo_edit.py")
                    
    with tab2:
        
        boton_detalle = st.empty()
        
        event = st.dataframe(
            df_equipos,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row"
        )

        seleccion = event.selection.rows

        if seleccion:

            indice = seleccion[0]

            # usamos df original para no perder el id
            ot_equipo = df_equipos.iloc[indice]
            
            st.session_state["id_ot_equipo"] = ot_equipo["id_ot_equipo"]

            with boton_detalle:
                if st.button("✏️ Editar OT"):
                    st.switch_page("pages/ot_equipo_edit.py")