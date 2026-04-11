import streamlit as st
from db import supabase
import login as login
import pandas as pd
from streamlit_redirect import redirect
from pages.editar_equipo import editar_ot
from pages.nuevo_equipo import agregar_nuevo_equipo

login.generarLogin("pages/ot_equipo_main.py")

if login.existUser():

    st.set_page_config(page_title="Editar OT", layout="wide")

    if "id_ot_equipo" not in st.session_state:
        st.warning("No hay orden seleccionada")
        st.stop()
    id_ot_equipo = st.session_state.id_ot_equipo
    
    res_ot = (
        supabase
        .table("ot_equipos")
        .select("ordenes_trabajo(n_ot), *")
        .eq("id_ot_equipo",id_ot_equipo)
        .execute()
    )
    ot = pd.json_normalize(res_ot.data[0])
    
    n_ot = ot['ordenes_trabajo.n_ot'][0]
    st.session_state.n_ot = n_ot

    st.subheader(f"Orden {n_ot}")

    with st.form("editar_ot"):
        empresas_list = supabase.table("empresas").select("*").execute()
        empresas_df = pd.DataFrame(empresas_list.data)

        # Creamos un diccionario {nombre_empresa: ruc}
        empresa_ruc_map = dict(zip(empresas_df['razon_social'], empresas_df['ruc']))

        # Lista de nombres de empresas
        empresa_nombres = list(empresa_ruc_map.keys())

        input1, input2 = st.columns([2,1])
        # Selectbox para razón social
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
        
        col1, col2, col3 = st.columns(3)
        
        estado = col1.selectbox("Estado",["Abierta", "Cerrado"])
        
        fecha_servicio = col2.date_input("Fecha servicio",value=ot["fecha_servicio"][0])
        
        opciones_certificadora = ["OVERHAUL", "PREXA"]
        certificadora = col3.selectbox(
            "Certificadora",
            opciones_certificadora,
            index=opciones_certificadora.index(ot["certificadora"][0]) if ot["certificadora"][0] in opciones_certificadora else 0
        )

        submit = st.form_submit_button("Guardar cambios")

    if submit:

        supabase.table("ot_equipos").update({
            "empresa" : empresa_seleccionada,
            "ruc" : ruc,
            "fecha_servicio": str(fecha_servicio),
            "certificadora" : certificadora,
            "estado" : estado
        }).eq("ot_id", ot["ot_id"][0]).execute()

        st.success("Orden actualizada correctamente")

        if st.button("Volver"):
            st.switch_page("pages/ot_equipo_main.py")
            
    st.write("Equipos")
    
    option1, option2, _ = st.columns([1,1,6])
    
    if option1.button("➕ Equipo"):
    # Esto abrirá el diálogo automáticamente
        agregar_nuevo_equipo()  # función decorada con @st.dialog
    
    res_equipos = (
        supabase
        .table("equipos")
        .select("*")
        .eq("ot_equipo_id", ot["id_ot_equipo"][0])
        .execute()
    )
    
    boton_detalle = option2.empty()
    
    equipos = pd.DataFrame(res_equipos.data)
    
    if not equipos.empty:
        event_eq = st.dataframe(equipos, width='stretch',
        on_select="rerun",
        selection_mode="single-row")
    
        seleccion = event_eq.selection.rows

        if seleccion:

            indice = seleccion[0]

            # usamos df original para no perder el id
            equipo_i = equipos.iloc[indice]

            st.session_state.equipo_select = equipo_i.to_dict()

            with boton_detalle:
                if st.button("✏️ Editar"):
                    editar_ot()
                    
    else:
        st.info("No hay equipos registrados todavía.")

    
    
    st.write("Facturas")
    
    res_facturas = (
        supabase
        .table("facturas")
        .select("*")
        .eq("id_ot",id_ot_equipo)
        .execute()
    )
    
    if st.button("➕ Factura"):
        res_new_factura = supabase.table("facturas").insert({"id_ot":int(id_ot_equipo), "razon_social" : empresa_seleccionada, "ruc" :ruc }).execute()
        if res_new_factura.data:
            new_factura = res_new_factura.data[0]
            st.toast(f"Nueva factura para: {n_ot}",icon="✅")
            url_ot_facturas=f"facturas_ot?id_factura={new_factura["id_factura"]}&id_ot={new_factura['id_ot']}&tipo_ot=ot_equipos"
            redirect(url_ot_facturas)

    
    boton_detalle_fac = st.empty()
    
    facturas = pd.DataFrame(res_facturas.data)
    
    # Verificamos si el DataFrame tiene filas
    if not facturas.empty:
        facturas_eq = st.dataframe(
            facturas,
            width='stretch',
            on_select="rerun",
            selection_mode="single-row"
        )
        seleccion = facturas_eq.selection.rows
        
        
        if seleccion:
            indice = seleccion[0]
            factura_seleccionada = facturas.iloc[indice]
            
            with boton_detalle_fac:
                url_ot_facturas=f"facturas_ot?id_factura={factura_seleccionada["id_factura"]}&id_ot={factura_seleccionada['id_ot']}&tipo_ot=ot_equipos"
                st.markdown(f"[✏️ Editar Factura]({url_ot_facturas})", unsafe_allow_html=True)
                    
    else:
        st.info("No hay facturas registradas todavía.")
    
    
    
