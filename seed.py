import os
import random
import psycopg2
from faker import Faker

def run_seeder():
    # Configuración de conexión desde variables de entorno
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'bibliotech_db'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASS', 'adminpassword')
    )
    cur = conn.cursor()
    fake = Faker(['es_ES'])

    print("🌱 Iniciando la siembra de datos (Seeding)...")

    # Limpiar datos anteriores (opcional, cuidado en producción)
    tables = ['MULTAS', 'PRESTAMOS', 'LIBRO_AUTOR', 'LIBROS', 'USUARIOS', 'CATEGORIAS', 'EDITORIALES', 'AUTORES']
    for t in tables:
        cur.execute(f"TRUNCATE TABLE {t} RESTART IDENTITY CASCADE;")

    # 1. Autores (20)
    print("   -> Generando Autores...")
    for _ in range(20):
        cur.execute("INSERT INTO AUTORES (nombre, nacionalidad) VALUES (%s, %s)", (fake.name(), fake.country()))

    # 2. Editoriales (10)
    print("   -> Generando Editoriales...")
    for _ in range(10):
        cur.execute("INSERT INTO EDITORIALES (nombre, pais) VALUES (%s, %s)", (fake.company(), fake.country()))

    # 3. Categorias (8)
    print("   -> Generando Categorías...")
    cats = ['Novela', 'Ciencia', 'Historia', 'Tecnología', 'Arte', 'Matemáticas', 'Fantasía', 'Biografía']
    for c in cats:
        cur.execute("INSERT INTO CATEGORIAS (nombre_cat, descripcion) VALUES (%s, %s)", (c, fake.text()))
    
    conn.commit()

    # 4. Libros (50)
    print("   -> Generando Libros...")
    for _ in range(50):
        cur.execute("""
            INSERT INTO LIBROS (titulo, precio, fecha_publicacion, id_editorial, id_categoria) 
            VALUES (%s, %s, %s, %s, %s)""", 
            (fake.sentence(nb_words=4), round(random.uniform(10, 100), 2), fake.date_between(start_date='-10y'), random.randint(1,10), random.randint(1,8))
        )
    
    # 5. Usuarios (30)
    print("   -> Generando Usuarios...")
    tipos = ['Estudiante', 'Profesor', 'Investigador', 'Externo']
    for _ in range(30):
        cur.execute("INSERT INTO USUARIOS (nombre, email, ciudad, tipo_usuario) VALUES (%s, %s, %s, %s)", 
                    (fake.name(), fake.email(), fake.city(), random.choice(tipos)))
    
    conn.commit()

    # 6. Relaciones y Préstamos
    print("   -> Generando Préstamos, Multas y Relaciones Libro-Autor...")
    
    # Libro-Autor
    for i in range(1, 51): # Para cada libro
        cur.execute("INSERT INTO LIBRO_AUTOR (id_libro, id_autor) VALUES (%s, %s)", (i, random.randint(1, 20)))

    # Préstamos (40)
    for _ in range(40):
        cur.execute("""
            INSERT INTO PRESTAMOS (id_usuario, id_libro, fecha_prestamo, fecha_devolucion) 
            VALUES (%s, %s, %s, %s) RETURNING id_prestamo""",
            (random.randint(1, 30), random.randint(1, 50), fake.date_this_year(), 
             random.choice([fake.date_this_year(), None])) # A veces devuelto, a veces no
        )
        id_prestamo = cur.fetchone()[0]

        # Generar multa aleatoria para algunos préstamos
        if random.random() > 0.7:
            cur.execute("""
                INSERT INTO MULTAS (id_prestamo, monto, estado, descripcion) 
                VALUES (%s, %s, %s, %s)""",
                (id_prestamo, round(random.uniform(5, 50), 2), random.choice(['pendiente', 'pagada']), "Retraso en devolución")
            )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ ¡Base de datos poblada con éxito! (+100 tuplas creadas)")

if __name__ == "__main__":
    run_seeder()