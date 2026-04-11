import streamlit as st
from db import supabase
import login as login
import pandas as pd
from login import existUser

login.generarLogin("pages/cursos_main.py")

if existUser():
    st.set_page_config(page_title="Empresas", layout="wide")

    col1, col2 = st.columns([4,1])

    with col1:
        st.header("Cursos")

    with col2:
        if st.button("➕ Curso"):
            st.switch_page("pages/curso_nuevo.py")
            
    response = (
        supabase
        .table("cursos")
        .select("*")
        .execute()
    )
    df_empresas = pd.DataFrame(response.data)
    
    df_tbl_empresas = df_empresas.drop(columns=[
        "id"
    ], errors="ignore")
    
    st.dataframe(df_tbl_empresas)
    
    