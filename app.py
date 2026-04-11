import streamlit as st
from db import supabase
from login import existUser, generarLogin

generarLogin("app.py")

if existUser():
    st.set_page_config(page_title="Dashboard", layout="wide")
    st.header(':orange[Dashboard]')
    
    option1, option2, option3, _ = st.columns(4)
    
    desde =  option1.date_input("Desde")
    hasta =  option2.date_input("Hasta")
    
    col1, col2, col3, col4 = st.columns(4)
    
    ord_trab = supabase.table("ordenes_trabajo") \
    .select("id", count="exact") \
    .execute()
    
    equipos = supabase.table("equipos") \
    .select("id", count="exact") \
    .execute()
    
    personas = supabase.table("ot_personas") \
    .select("id_ot_persona", count="exact") \
    .execute()
    
    col1.metric("Ordenes Trabajo", value=ord_trab.count)
    col2.metric("Equipos", value=equipos.count)
    col3.metric("Personas", value=personas.count)