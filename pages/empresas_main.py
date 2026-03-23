import streamlit as st
from db import supabase
import login as login
import pandas as pd

login.generarLogin("pages/empresas_main.py")

if 'usuario' in st.session_state:
    st.set_page_config(page_title="Empresas", layout="wide")

    col1, col2 = st.columns([4,1])

    with col1:
        st.header("Empresas")

    with col2:
        if st.button("➕ Empresa"):
            st.switch_page("pages/empresa_nuevo.py")
            
    response = (
        supabase
        .table("empresas")
        .select("*")
        .execute()
    )
    df_empresas = pd.DataFrame(response.data)
    
    df_tbl_empresas = df_empresas.drop(columns=[
        "id"
    ], errors="ignore")
    
    st.dataframe(df_tbl_empresas)
    
    