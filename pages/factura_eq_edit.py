import streamlit as st
from db import supabase
import login as login
import pandas as pd

login.generarLogin("pages/facturas_ot.py")

if 'usuario' in st.session_state:
    params = st.experimental_get_query_params() if hasattr(st, "experimental_get_query_params") else st.query_params

    id_ot = params.get("id_ot", [""])       # devuelve '1'
    tipo_ot = params.get("tipo_ot", [""])   # devuelve 'ot_equipos'
    id_factura = params.get("id_factura", [""])   # devuelve 'ot_equipos'
    
    res_ot = supabase.table("ot_equipos").select("*").eq("id_ot_equipo", id_ot).single().execute()
    res_factura = supabase.table("facturas").select("*").eq("id_factura", id_factura).single().execute()
    res_equipos = supabase.table("equipos").select("*").eq("ot_equipo_id", id_ot).execute()
    
    if res_ot.data["certificadora"] == "OVERHAUL":
            st.subheader("OVERHAUL MINING E.I.R.L.")
            st.write("20602129749")
            st.write("AV. MANCO CAPAC NRO. 1346 BAL.BAÑOS DEL INCA LOS BAÑOS DEL INCA CAJAMARCA CAJAMARCA")

    
    factura = res_factura.data
    with st.form("form_factura"):

        n_factura = st.text_input("N° Factura", value=factura["n_factura"])

        
        col1, col2 = st.columns(2)

        cliente = col1.text_input("Cliente", value=res_ot.data["empresa"])
        ruc = col2.text_input("RUC", value=res_ot.data["ruc"])

        fecha_emision = col1.date_input("Fecha Emisión")
        moneda = col2.selectbox("Moneda", options=["PEN", "USD"])

        facturo = st.checkbox("Facturo?")
        pagado = st.checkbox("Pago?")
        pago_detraccion=st.checkbox("Pago detracción?")
        submit = st.form_submit_button("Guardar")

    if submit:
        res = (
            supabase
            .table("facturas")
            .update({
                "n_factura": n_factura,
                "fecha_emision": fecha_emision.isoformat(),
                "razon_social" : cliente,
                "ruc" : ruc,
                "moneda": moneda,
                "facturo":facturo,
                "pagado" : pagado,
                "pago_detraccion" : pago_detraccion
            })
            .eq("id_factura", factura["id_factura"])
            .execute()
        )

        st.success("Factura actualizada")
    
    st.markdown("---")
    
    res_detalles_fact = supabase.table("facturas_detalle").select("*").eq("factura_id", id_factura).execute()
    
    if res_detalles_fact.data:
        df_detalles_fact = pd.DataFrame(res_detalles_fact.data)
        st.dataframe(df_detalles_fact)
    
    equipos = pd.DataFrame(res_equipos.data)
    
    list_equipos = equipos[["tipo_unidad","tipo_servicio", "placa", "id"]]
    # array_textos = list_equipos.apply(lambda row: f"{row['placa']} | {row['tipo_servicio']} | {row['tipo_unidad']}", axis=1).tolist()
    mapeo_equipos = {
        f"{row['placa']} | {row['tipo_servicio']} | {row['tipo_unidad']}": row['id']
        for _, row in list_equipos.iterrows()
    }
    if st.button("➕ Agregar item"):
        @st.dialog("Agregar nuevo item")
        def modal_agregar_item():
            equipo = st.selectbox("Equipo", options=list(mapeo_equipos.keys()))
            id_seleccionado_equipo = mapeo_equipos[equipo]
            
            input1 , input2 = st.columns(2)
            valor_unit = input1.number_input("Valor unitario")
            
            igv = input2.number_input("IGV 18%", value=(valor_unit * 0.18), disabled=True)
            total = input2.number_input("Total", value=(valor_unit + igv), disabled=True)
            st.text_area("Descripción")
            
            
            col1, col2 = st.columns(2)
            guardar = col1.button("💾 Guardar")
            cancelar = col2.button("❌ Cancelar")

            if guardar:
                res_new_fact_detail = supabase.table("facturas_detalle").insert(
                    {
                        "factura_id": id_factura,
                        "igv" : igv,
                        "precio_unitario": valor_unit,
                        "descripcion" : equipo,
                        "total": total,
                        "id_equipo" : id_seleccionado_equipo
                    }
                    ).execute()
                
                res_update_fact_total = (
                    supabase
                    .table("facturas")
                    .update({
                        "sin_igv": factura["total"] + valor_unit,
                        "total" : factura["total"] + total,
                        "igv" : factura["igv"] + igv,
                    })
                    .eq("id_factura", factura["id_factura"])
                    .execute()
                )
                
                if res_new_fact_detail and res_update_fact_total:
                    st.success("Item agregado correctamente")
                    st.rerun()


            if cancelar:
                st.rerun()

        modal_agregar_item()
    st.markdown("---")
    
    st.write("Op. Gravada", factura["sin_igv"])
    st.write("IGV", factura["igv"])
    st.write("Importe total", factura["total"])
    
    st.set_page_config(page_title="Factura", layout="wide")
    