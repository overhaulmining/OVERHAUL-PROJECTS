import streamlit as st
from db import supabase
import login as login
import pandas as pd
from streamlit_redirect import redirect

login.generarLogin("pages/inscripciones_main.py")

if 'usuario' in st.session_state:
    st.set_page_config(page_title="Inscripciones", layout="wide")

    col1, col2 = st.columns([4,1])

    with col1:
        st.header("Inscripciones")

    with col2:
        st.markdown(f"[➕ Nueva inscripción]({"inscripciones_nuevo"})", unsafe_allow_html=True)
            
    response = (
        supabase
        .table("inscripciones")
        .select("*")
        .execute()
    )
    df_empresas = pd.DataFrame(response.data)
    
    df_tbl_empresas = df_empresas.drop(columns=[
        "id"
    ], errors="ignore")
    
    st.dataframe(df_tbl_empresas)
    
    