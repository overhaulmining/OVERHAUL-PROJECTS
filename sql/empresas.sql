-- Crear tabla
CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    ruc VARCHAR(11) NOT NULL,
    razon_social TEXT NOT NULL
);
