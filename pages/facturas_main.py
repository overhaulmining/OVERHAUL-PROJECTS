import streamlit as st
from db import supabase
import login as login
import pandas as pd
from login import existUser

login.generarLogin("pages/facturas_main.py")

if existUser():

    st.set_page_config(page_title="Orden Trabajo Equipo", layout="wide")

    col1, col2 = st.columns([4,1])

    with col1:
        st.header("Facturas")

    # with col2:
        # if st.button("➕ Nueva OT"):
        #     res_new_ot = supabase.table("ordenes_trabajo").insert({}).execute()
            
            
        #     if res_new_ot:
        #         new_ot_id = res_new_ot.data[0]["id"]
        #         new_ot_n_ot = res_new_ot.data[0]["n_ot"]
                
        #         res_new_ot_eq = supabase.table("ot_equipos").insert({"ot_id": new_ot_id}).execute()
        #         id_res_new_ot_eq = res_new_ot_eq.data[0]["id_ot_equipo"]
        #         st.toast(f"Se creó nueva OT: {new_ot_n_ot}",icon="✅")
        #         st.session_state["id_ot_equipo"] = id_res_new_ot_eq
        #         # Cambiar de página
        #         st.switch_page("pages/ot_equipo_edit.py")
        #     else:
        #         st.error("Error al crear la OT")

    res_facturas = (
        supabase
        .table("facturas")
        .select("*")
        .execute()
    )

    facturas = pd.DataFrame(res_facturas.data)


    tab2, tab3, tab1 = st.tabs([ "Equipos", "Personas","All"])

    with tab1:
        
        boton_detalle = st.empty()

        event = st.dataframe(
            facturas,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row"
        )

        seleccion = event.selection.rows

        if seleccion:

            indice = seleccion[0]

            # usamos df original para no perder el id
            factura = facturas.iloc[indice]
            with boton_detalle:
                url_ot_facturas=f"facturas_ot?id_factura={factura["id_factura"]}&id_ot={factura['id_ot']}&tipo_ot=ot_equipos"
                st.markdown(f"""
                    <a href="{url_ot_facturas}" target="_blank" style="text-decoration: none;">
                        <button style="
                            padding: 6px 12px; 
                            font-size: 15px; 
                            font-weight: bold;
                            color: white; 
                            background-color: #ff7f50; 
                            border: none; 
                            border-radius: 8px; 
                            cursor: pointer;
                            transition: background-color 0.3s;
                            margin-bottom:10px
                        "
                        onmouseover="this.style.backgroundColor='#ff6347';" 
                        onmouseout="this.style.backgroundColor='#ff7f50';"
                        >
                            ✏️ Editar
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
    with tab2:
        
        res_facturas_equipos = supabase.rpc("obtener_reporte_detallado_facturacion").execute()
        if res_facturas_equipos.data:
            df_facturas_equipos = pd.DataFrame(res_facturas_equipos.data)
            # Convertir a formato de fecha de Python para que Streamlit lo muestre bien
            df_facturas_equipos['fecha_emision'] = pd.to_datetime(df_facturas_equipos['fecha_emision'])
            st.dataframe(df_facturas_equipos,use_container_width=True,
            on_select="rerun",
            selection_mode="single-row")
            
    #         boton_detalle = st.empty()
            
    #         event = st.dataframe(
    #             df_equipos,
    #             use_container_width=True,
    #             on_select="rerun",
    #             selection_mode="single-row"
    #         )

    #         seleccion = event.selection.rows

    #         if seleccion:

    #             indice = seleccion[0]

    #             # usamos df original para no perder el id
    #             ot_equipo = df_equipos.iloc[indice]

    #             st.session_state.ot_equipo_select = ot_equipo.to_dict()

    #             with boton_detalle:
    #                 if st.button("✏️ Editar OT"):
    #                     st.switch_page("pages/ot_equipo_edit.py")    