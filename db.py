import os
import streamlit as st
from supabase import create_client, Client

url: str = "https://qfqlipjkptsapzhvklsk.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmcWxpcGprcHRzYXB6aHZrbHNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI4MTg5NTcsImV4cCI6MjA4ODM5NDk1N30.XhRWnk25kzb3Bl_RMm3rOyNIhRrFQCdYrOfdzIKU4q8"

# Inicializamos el cliente (se recomienda usar st.cache_resource para no reconectar en cada clic)
@st.cache_resource
def init_connection():
    return create_client(url, key)

supabase = init_connection()