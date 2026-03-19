import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

url: str = os.getenv('DB_URL')
key: str = os.getenv('DB_KEY')

# Inicializamos el cliente (se recomienda usar st.cache_resource para no reconectar en cada clic)
@st.cache_resource
def init_connection():
    return create_client(url, key)

supabase = init_connection()