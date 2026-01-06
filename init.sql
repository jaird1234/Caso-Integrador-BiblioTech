-- Crear tablas si no existen
CREATE TABLE IF NOT EXISTS AUTORES (
    id_autor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS EDITORIALES (
    id_editorial SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS CATEGORIAS (
    id_categoria SERIAL PRIMARY KEY,
    nombre_cat VARCHAR(50) NOT NULL,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS LIBROS (
    id_libro SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    precio DECIMAL(10,2),
    fecha_publicacion DATE,
    id_editorial INT REFERENCES EDITORIALES(id_editorial),
    id_categoria INT REFERENCES CATEGORIAS(id_categoria)
);

CREATE TABLE IF NOT EXISTS LIBRO_AUTOR (
    id_libro INT REFERENCES LIBROS(id_libro),
    id_autor INT REFERENCES AUTORES(id_autor),
    PRIMARY KEY (id_libro, id_autor)
);

CREATE TABLE IF NOT EXISTS USUARIOS (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    ciudad VARCHAR(50),
    tipo_usuario VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS PRESTAMOS (
    id_prestamo SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES USUARIOS(id_usuario),
    id_libro INT REFERENCES LIBROS(id_libro),
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion TIMESTAMP
);

-- Tipo ENUM para Postgres
DO $$ BEGIN
    CREATE TYPE estado_multa_enum AS ENUM ('pendiente', 'pagada', 'perdonada');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS MULTAS (
    id_multa SERIAL PRIMARY KEY,
    id_prestamo INT UNIQUE REFERENCES PRESTAMOS(id_prestamo),
    monto DECIMAL(10,2),
    estado estado_multa_enum,
    descripcion VARCHAR(255)
);