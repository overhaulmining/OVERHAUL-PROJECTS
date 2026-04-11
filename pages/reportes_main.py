import streamlit as st
from db import supabase
import login as login
import pandas as pd
import plotly.express as px

login.generarLogin("pages/reportes_main.py")

if login.existUser():
    st.set_page_config(page_title="Reportes", layout="wide")

    col1, col2 = st.columns([4,1])

    with col1:
        st.header("Reportes")

    # with col2:
    #     if st.button("➕ Empresa"):
    #         st.switch_page("pages/Crear_OT.py")
            
    # response = (
    #     supabase
    #     .table("empresas")
    #     .select("*")
    #     .execute()
    # )
    # df_empresas = pd.DataFrame(response.data)
    
    # df_tbl_empresas = df_empresas.drop(columns=[
    #     "id"
    # ], errors="ignore")
    
    # st.dataframe(df_tbl_empresas)
    
    
    res_fact_empresa = supabase.rpc("resumen_facturacion_por_empresa").execute()
    st.subheader("📊 Resumen de Facturación por Empresa")

    if res_fact_empresa.data:
        # 2. Convertir a DataFrame
        df_resumen = pd.DataFrame(res_fact_empresa.data)
        
        # 3. Preparar los datos para la gráfica
        # Usamos set_index para que los nombres de las empresas aparezcan en el eje X
        df_grafica = df_resumen[['empresa', 'total_con_igv']].set_index('empresa')
        
        # 4. Mostrar la gráfica de barras
        st.bar_chart(df_grafica, color="#29b5e8") # Puedes elegir el color que prefieras
        
    else:
        st.info("No hay datos disponibles para generar la gráfica.")
        
        
    res_fact_mes = supabase.rpc("reporte_facturacion_por_mes").execute()
    st.subheader("📊 Facturación Mensual (Ventas por Mes)")

    if res_fact_mes.data:
        df_meses = pd.DataFrame(res_fact_mes.data)
    
        # Aseguramos que sea datetime en Python
        df_meses['mes'] = pd.to_datetime(df_meses['mes'])
        
        # Para que la gráfica sea más legible, podemos crear una columna con el nombre del mes
        # pero usaremos la fecha real para el índice para mantener el orden cronológico
        df_grafica = df_meses[['mes', 'total_mes']].set_index('mes')
        
        # Gráfica de barras
        st.bar_chart(df_grafica, color="#1f77b4")
        
    else:
        st.info("No hay datos disponibles para generar la gráfica.")
        
        
    
    res_totales_unidad = supabase.rpc("obtener_totales_por_unidad").execute()

    st.subheader("📊 Total por Equipo")

    # 2. Procesar los datos y graficar
    if res_totales_unidad.data:
        # Convertimos la respuesta de Supabase a DataFrame
        df_unidades = pd.DataFrame(res_totales_unidad.data)
        
        # Creamos el gráfico de barras
        fig = px.bar(
            df_unidades, 
            x='tipo_unidad', 
            y='total_por_unidad',
            text='total_por_unidad',
            labels={'tipo_unidad': 'Equipo', 'total_por_unidad': 'Total Facturado'},
            color='tipo_unidad',
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        
        # Estética del gráfico
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(showlegend=False, height=450)
        
        # Mostrar en la app
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar en el gráfico.")
    
    
    
    res_cert = supabase.rpc("reporte_totales_certificadoras").execute()

    st.subheader("🏆 Ventas Totales por Certificadora")

    if res_cert.data:
        # 2. Convertir a DataFrame
        df_cert = pd.DataFrame(res_cert.data)
        
        # 3. Preparar los datos para la gráfica
        # Ponemos la certificadora como índice para que Streamlit la use en el eje X
        df_grafica = df_cert[['certificadora', 'total_acumulado']].set_index('certificadora')
        
        
        # 4. Mostrar la gráfica de barras
        # Usamos un color distinto para diferenciar este reporte de los anteriores
        st.bar_chart(df_grafica, color="#ff4b4b", use_container_width=True)
        
        # 5. Mostrar métricas comparativas
        top_cert = df_cert.iloc[df_cert['total_acumulado'].idxmax()]
        st.success(f"La certificadora con mayor volumen es **{top_cert['certificadora']}** con S/ {top_cert['total_acumulado']:,.2f}")

    else:
        st.info("No hay datos vinculados entre OT Equipos y Facturas.")
        
    
    