import login as login
import pandas as pd
from streamlit_redirect import redirect
from db import supabase
import streamlit as st
from login import existUser

login.generarLogin("pages/empresa_nuevo.py")

from datetime import date
if existUser():

    with st.form("form_empresa_nuevo", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            ruc = st.text_input("RUC", max_chars=10)
        
        with col2:
            razon_social = st.text_input("Razon Social")
        
        submit = st.form_submit_button("Registrar Nueva empresa")

        if submit:
            if razon_social and ruc:
                data_ins = {
                    "ruc": ruc,
                    "razon_social": razon_social
                }
                
                try:
                    res = supabase.table("empresas").insert(data_ins).execute()
                    st.success(f"✅ Registrado")
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
            else:
                st.warning("Por favor, completa los campos obligatorios.")