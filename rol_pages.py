import pandas as pd

pages_roles = pd.DataFrame([
    {"pagina": "app.py", "nombre": "Inicio", "icono": "home", "roles": ["administrador"]},
    {"pagina": "pages/ot_equipo_main.py", "nombre": "OT Equipos", "icono": "build", "roles": ["administrador"]},
    {"pagina": "pages/ot_personas_main.py", "nombre": "OT Personas", "icono": "engineering", "roles": ["administrador"]},
    {"pagina": "pages/facturas_main.py", "nombre": "Facturas", "icono": "receipt", "roles": ["administrador","contador"]},
    {"pagina": "pages/reportes_main.py", "nombre": "Reportes", "icono": "receipt", "roles": ["administrador","contador"]},
    {"pagina": "pages/inscripciones_main.py", "nombre": "Inscripciones", "icono": "receipt", "roles": ["administrador","contador"]},
    {"pagina": "pages/cursos_main.py", "nombre": "Cursos", "icono": "book", "roles": ["administrador","contador"]},
    {"pagina": "pages/ot_equipo_edit.py", "nombre": "OT Equipos", "icono": "build", "roles": ["administrador"], "sidebar": False},
    {"pagina": "pages/empresas_main.py", "nombre": "Empresas", "icono": "enterprise", "roles": ["administrador"]},
    # {"pagina": "pages/usuarios.py", "nombre": "Usuarios", "icono": "group", "roles": ["admin"]},
    # {"pagina": "pages/reportes.py", "nombre": "Reportes", "icono": "bar_chart", "roles": ["admin", "supervisor"]},
])
