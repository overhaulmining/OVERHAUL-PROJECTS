import streamlit as st
from datetime import date
import pandas as pd
from db import supabase

st.title("📖 Libro de Reclamación Virtual")

fecha_emision = st.date_input("Fecha de emisión de hoja de reclamo", disabled=True)


res = supabase.table("libro_reclamaciones") \
    .select("id") \
    .order("id", desc=True) \
    .limit(1) \
    .execute()

ultimo_id = res.data[0]["id"] if res.data else 0

n_hoja_value = str(ultimo_id + 1).zfill(6)

n_hoja = st.text_input("N° Hoja", disabled=True, value=n_hoja_value)

st.markdown("""
- RUC: 20602129749
- Razón Social: OVERHAUL MINING E.I.R.L..
- Dirección Comercial: AV. MANCO CAPAC NRO. 1346 BAL. BAÑOS DEL INCA (ULTIMO PARADERO LINEA 14-FRENTE AL GRIFO) CAJAMARCA - CAJAMARCA - LOS BAÑOS DEL INCA          
""")

with st.form("form_inscripcion", clear_on_submit=True):
    
    st.text("1. Identificación del consumidor reclamante")
    col1, col2 = st.columns(2)
    
    nombres = col1.text_input("nombres")
    apellidos = col2.text_input("apellidos")
    
    col3, col4, col5 = st.columns(3)
    
    tipo_documento = col3.selectbox("Tipo de documento *", ["DNI","CE", "RUC", "PASAPORTE"])
    n_documento = col4.text_input("N° Documento")
    celular = col5.text_input("Celular")
    
    col5, col6, col7 = st.columns(3)
    
    departamento = col5.text_input("Departamento")
    provincia = col6.text_input("Provincia")
    distrito = col7.text_input("Distrito")
    
    col7, col8 = st.columns(2)
    
    direccion = col7.text_input("Direccion")
    referencia = col8.text_input("Referencia")
    correo = st.text_input("Correo")
    
    menor_edad = st.radio("Menor edad?", ["si", "no"])
    
    st.text("2. Identificación del Bien Contratado")
    
    tipo_consumo = st.selectbox("Tipo de consumo *", ["Producto","Servicio"])
    
    n_pedido = st.text_input("N° de pedido")
    fecha_incidente = st.date_input("Fecha del incidente")
    
    monto_producto = st.number_input("Monto del producto o servicio contratado objeto")
    
    descripcion = st.text_area("Descripción")
    
    st.text("3. Detalle de la reclamación y pedido del consumidor")
    
    tipo_reclamo = st.radio("Tipo de Reclamo", ["Reclamo: Disconformidad relacionada a los productos o servicios.", "Queja: Disconformidad no relacionada a los productos o servicios o malestar o descontento respecto a la atención al público."])
    
    detalle_reclamacion = st.text_area("Detalle de la reclamación o queja: *")
    
    pedido_concreto = st.text_area("Pedido concreto del consumidor respecto al hecho que motiva el reclamo o queja: *")
    
    st.text("4. Observaciones y acciones adoptadas por el proveedor")
    
    observacion_acciones_proveedor = st.text_area("")
    
    conformidad_terminos = st.checkbox("Me encuentro conforme con los términos de mi reclamo o queja.")
    
    st.markdown("""
                - En caso que el consumidor no consigne como mínimo su nombre, DNI, domicilio o correo electrónico y el detalle del reclamo o queja, de conformidad con el artículo 5 del Reglamento del Libro de Reclamaciones, estos se considerarán como no presentados
                - La formulación del reclamo no excluye el recurso a otros medios de resolución de controversias ni es un requisito previo para presentar una denuncia ante el Indecopi.
                - El proveedor deberá dar respuesta al reclamo en un plazo no mayor a quince (15) días calendario, pudiendo extender el plazo hasta quince días.
                - Con la firma de este documento, el cliente autoriza a ser contactado después de la tramitación de la reclamación para evaluar la calidad y satisfacción del proceso de atención de reclamaciones.
                """)
    
    submit = st.form_submit_button("Enviar hoja de reclamación")

    if submit:
        try:
            # Validación mínima obligatoria
            if not nombres or not apellidos or not n_documento:
                st.warning("❌ Completa nombres, apellidos y documento.")
                st.stop()

            if not detalle_reclamacion or not pedido_concreto:
                st.warning("❌ Debes completar el detalle del reclamo y el pedido.")
                st.stop()

            data = {
                # consumidor
                "nombres": nombres,
                "apellidos": apellidos,
                "tipo_documento": tipo_documento,
                "numero_documento": n_documento,
                "celular": celular,
                "departamento": departamento,
                "provincia": provincia,
                "distrito": distrito,
                "direccion": direccion,
                "referencia": referencia,
                "correo": correo,
                "menor_edad": True if menor_edad == "si" else False,

                # hoja reclamo
                "numero_hoja": n_hoja,
                "fecha_emision": fecha_emision.isoformat(),

                # bien contratado
                "tipo_consumo": tipo_documento,  # (OJO: aquí en tu form está mal nombrado)
                "numero_pedido": n_pedido,
                "fecha_incidente": fecha_incidente.isoformat(),
                "monto": float(monto_producto) if monto_producto else None,
                "descripcion": descripcion,

                # reclamo
                "tipo_reclamo": tipo_reclamo,
                "detalle_reclamacion": detalle_reclamacion,
                "pedido_concreto": pedido_concreto,

                # proveedor
                "observaciones_proveedor": observacion_acciones_proveedor,

                # conformidad
                "conformidad_terminos": conformidad_terminos,
            }

            res = supabase.table("libro_reclamaciones").insert(data).execute()

            if res.data:
                st.success("✅ Reclamo registrado correctamente")
            else:
                st.error("❌ No se pudo registrar el reclamo")

        except Exception as e:
            st.error(f"Error al guardar: {str(e)}")
