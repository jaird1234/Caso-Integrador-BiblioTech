import os
import time
import psycopg2
from tabulate import tabulate
import seed # Importamos el script de seed


DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'bibliotech_db'),
    'user': os.environ.get('DB_USER', 'admin'),
    'password': os.environ.get('DB_PASS', 'adminpassword')
  
}

def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# --- DICCIONARIO DE CONSULTAS (LAS 20 COMPLETAS) ---
CONSULTAS = {
    # --- GRUPO A: OPERADORES BÁSICOS (5 Consultas) ---
    "1": {
        "titulo": "1. [Básica] Usuarios 'Estudiante' en ciudad específica (Selección)",
        "sql": "SELECT nombre, email, ciudad FROM USUARIOS WHERE tipo_usuario = 'Estudiante' AND ciudad LIKE '%a%' LIMIT 5;",
        "algebra": "π(nombre, email) (σ(tipo='Estudiante' ∧ ciudad LIKE '%a%') (USUARIOS))",
        "calculo": "{ t[nombre, email] | t ∈ USUARIOS ∧ t[tipo] = 'Estudiante' }",
        "dominio": "{ <n, e, c> | ∃id, t (<id, n, e, c, t> ∈ USUARIOS ∧ t = 'Estudiante' ∧ c LIKE '%a%') }"
    },
    "2": {
        "titulo": "2. [Básica] Libros publicados después de 2020 (Selección)",
        "sql": "SELECT titulo, fecha_publicacion FROM LIBROS WHERE fecha_publicacion > '2020-01-01' LIMIT 5;",
        "algebra": "π(titulo, fecha) (σ(fecha > '2020-01-01') (LIBROS))",
        "calculo": "{ t[titulo, fecha] | t ∈ LIBROS ∧ t[fecha] > '2020' }",
        "dominio": "{ <t, f> | ∃id, p, e, c (<id, t, p, f, e, c> ∈ LIBROS ∧ f > '2020-01-01') }"
    },
    "3": {
        "titulo": "3. [Básica] Autores o Usuarios (Unión)",
        "sql": "SELECT nombre as persona, 'Autor' as tipo FROM AUTORES UNION SELECT nombre, 'Usuario' FROM USUARIOS LIMIT 5;",
        "algebra": "π(nombre)(AUTORES) ∪ π(nombre)(USUARIOS)",
        "calculo": "{ t | t ∈ AUTORES ∨ t ∈ USUARIOS }",
        "dominio": "{ <n> | ∃id, nac (<id, n, nac> ∈ AUTORES) ∨ ∃id, e, c, t (<id, n, e, c, t> ∈ USUARIOS) }"
    },
    "4": {
        "titulo": "4. [Básica] Libros que NO son de la Editorial 1 (Diferencia)",
        "sql": "SELECT titulo FROM LIBROS WHERE id_editorial != 1 LIMIT 5;",
        "algebra": "LIBROS - σ(id_editorial=1)(LIBROS)",
        "calculo": "{ t | t ∈ LIBROS ∧ t[id_editorial] ≠ 1 }",
        "dominio": "{ <t> | ∃id, p, f, e, c (<id, t, p, f, e, c> ∈ LIBROS ∧ e ≠ 1) }"
    },
    "5": {
        "titulo": "5. [Básica] Proyección de correos únicos (Proyección)",
        "sql": "SELECT DISTINCT email FROM USUARIOS WHERE email IS NOT NULL LIMIT 5;",
        "algebra": "π(email)(USUARIOS)",
        "calculo": "{ t[email] | t ∈ USUARIOS }",
        "dominio": "{ <e> | ∃id, n, c, t (<id, n, e, c, t> ∈ USUARIOS) }"
    },

    # --- GRUPO B: REUNIONES / JOINS (5 Consultas) ---
    "6": {
        "titulo": "6. [Reunión] Libros y nombre de su Editorial",
        "sql": "SELECT L.titulo, E.nombre as editorial FROM LIBROS L JOIN EDITORIALES E ON L.id_editorial = E.id_editorial LIMIT 5;",
        "algebra": "π(titulo, nom_edit) (LIBROS ⨝ EDITORIALES)",
        "calculo": "{ <l.titulo, e.nombre> | l ∈ LIBROS ∧ e ∈ EDITORIALES ∧ l.id_e = e.id_e }",
        "dominio": "{ <t, ne> | ∃id_l, p, f, id_e, id_c, id_e2, pais (<id_l, t, p, f, id_e, id_c> ∈ LIBROS ∧ <id_e2, ne, pais> ∈ EDITORIALES ∧ id_e = id_e2) }"
    },
    "7": {
        "titulo": "7. [Reunión] Préstamos detallados (Usuario y Libro)",
        "sql": "SELECT U.nombre, L.titulo, P.fecha_prestamo FROM PRESTAMOS P JOIN USUARIOS U ON P.id_usuario = U.id_usuario JOIN LIBROS L ON P.id_libro = L.id_libro LIMIT 5;",
        "algebra": "π(nom_usu, titulo) (PRESTAMOS ⨝ USUARIOS ⨝ LIBROS)",
        "calculo": "Relación ternaria entre Préstamos, Usuarios y Libros",
        "dominio": "{ <nu, tl, fp> | ∃id_p, id_u, id_l, fd (<id_p, id_u, id_l, fp, fd> ∈ PRESTAMOS ∧ <id_u, nu...> ∈ USUARIOS ∧ <id_l, tl...> ∈ LIBROS) }"
    },
    "8": {
        "titulo": "8. [Reunión] Multas pendientes y nombre del usuario",
        "sql": "SELECT U.nombre, M.monto FROM MULTAS M JOIN PRESTAMOS P ON M.id_prestamo = P.id_prestamo JOIN USUARIOS U ON P.id_usuario = U.id_usuario WHERE M.estado = 'pendiente' LIMIT 5;",
        "algebra": "π(nombre, monto) (σ(estado='pendiente')(MULTAS ⨝ PRESTAMOS ⨝ USUARIOS))",
        "calculo": "{ <u.nombre, m.monto> | ∃p (m ∈ MULTAS ∧ p ∈ PRESTAMOS ... ) }",
        "dominio": "{ <nu, m> | ∃id_m, id_p, est, desc, id_u, id_l, fp, fd (<id_m, id_p, m, est, desc> ∈ MULTAS ∧ est='pendiente' ∧ <id_p, id_u, id_l, fp, fd> ∈ PRESTAMOS ∧ <id_u, nu...> ∈ USUARIOS) }"
    },
    "9": {
        "titulo": "9. [Reunión] Autores y sus Libros (N:M)",
        "sql": "SELECT A.nombre, L.titulo FROM AUTORES A JOIN LIBRO_AUTOR LA ON A.id_autor = LA.id_autor JOIN LIBROS L ON LA.id_libro = L.id_libro LIMIT 5;",
        "algebra": "π(nom_aut, titulo) (AUTORES ⨝ LIBRO_AUTOR ⨝ LIBROS)",
        "calculo": "Relación N:M resuelta por tabla intermedia",
        "dominio": "{ <na, tl> | ∃id_a, id_l (<id_a, na...> ∈ AUTORES ∧ <id_l, id_a> ∈ LIBRO_AUTOR ∧ <id_l, tl...> ∈ LIBROS) }"
    },
    "10": {
        "titulo": "10. [Reunión] Categoría de libros prestados",
        "sql": "SELECT DISTINCT C.nombre_cat, L.titulo FROM PRESTAMOS P JOIN LIBROS L ON P.id_libro = L.id_libro JOIN CATEGORIAS C ON L.id_categoria = C.id_categoria LIMIT 5;",
        "algebra": "π(nom_cat, titulo) (PRESTAMOS ⨝ LIBROS ⨝ CATEGORIAS)",
        "calculo": "{ <c.nombre, l.titulo> | l fue prestado }",
        "dominio": "{ <nc, tl> | ∃id_p, id_u, id_l, id_c, desc (<id_p, id_u, id_l...> ∈ PRESTAMOS ∧ <id_l, tl..., id_c> ∈ LIBROS ∧ <id_c, nc, desc> ∈ CATEGORIAS) }"
    },

    # --- GRUPO C: AGRUPACIÓN Y AGREGACIÓN (5 Consultas) ---
    "11": {
        "titulo": "11. [Agrupación] Total de libros por Categoría",
        "sql": "SELECT C.nombre_cat, COUNT(L.id_libro) as total FROM CATEGORIAS C LEFT JOIN LIBROS L ON C.id_categoria = L.id_categoria GROUP BY C.nombre_cat;",
        "algebra": "nombre_cat ℑ COUNT(id_libro) (CATEGORIAS ⨝ LIBROS)",
        "calculo": "Función de agregación count()",
        "dominio": "{ <nc, COUNT(id_l)> | <id_c, nc...> ∈ CATEGORIAS ∧ <id_l... id_c> ∈ LIBROS }"
    },
    "12": {
        "titulo": "12. [Agrupación] Precio promedio de libros por Editorial",
        "sql": "SELECT E.nombre, ROUND(AVG(L.precio), 2) as precio_promedio FROM EDITORIALES E JOIN LIBROS L ON E.id_editorial = L.id_editorial GROUP BY E.nombre;",
        "algebra": "nom_edit ℑ AVG(precio) (EDITORIALES ⨝ LIBROS)",
        "calculo": "Función de agregación avg()",
        "dominio": "{ <ne, AVG(p)> | <id_e, ne...> ∈ EDITORIALES ∧ <id_l, t, p... id_e> ∈ LIBROS }"
    },
    "13": {
        "titulo": "13. [Agrupación] Usuarios con más de 2 préstamos (Having)",
        "sql": "SELECT U.nombre, COUNT(P.id_prestamo) FROM USUARIOS U JOIN PRESTAMOS P ON U.id_usuario = P.id_usuario GROUP BY U.nombre HAVING COUNT(P.id_prestamo) > 2;",
        "algebra": "σ(count > 2) (nombre ℑ COUNT(id_prestamo) (USUARIOS ⨝ PRESTAMOS))",
        "calculo": "Agregación con condición posterior",
        "dominio": "{ <nu, COUNT(id_p)> | <id_u, nu...> ∈ USUARIOS ∧ <id_p, id_u...> ∈ PRESTAMOS ∧ COUNT(id_p) > 2 }"
    },
    "14": {
        "titulo": "14. [Agrupación] Monto total de multas por estado",
        "sql": "SELECT estado, SUM(monto) as total_deuda FROM MULTAS GROUP BY estado;",
        "algebra": "estado ℑ SUM(monto) (MULTAS)",
        "calculo": "Función de agregación sum()",
        "dominio": "{ <est, SUM(m)> | <id_m, id_p, m, est, desc> ∈ MULTAS }"
    },
    "15": {
        "titulo": "15. [Agrupación] El libro más caro de cada categoría",
        "sql": "SELECT C.nombre_cat, MAX(L.precio) FROM CATEGORIAS C JOIN LIBROS L ON C.id_categoria = L.id_categoria GROUP BY C.nombre_cat;",
        "algebra": "nom_cat ℑ MAX(precio) (CATEGORIAS ⨝ LIBROS)",
        "calculo": "Función de agregación max()",
        "dominio": "{ <nc, MAX(p)> | <id_c, nc...> ∈ CATEGORIAS ∧ <id_l, t, p... id_c> ∈ LIBROS }"
    },

    # --- GRUPO D: DIVISIÓN (3 Consultas) ---
    "16": {
        "titulo": "16. [División] Usuarios que han pedido TODOS los libros de 'Matemáticas'",
        "sql": """
            SELECT U.nombre FROM USUARIOS U
            WHERE NOT EXISTS (
                SELECT L.id_libro FROM LIBROS L JOIN CATEGORIAS C ON L.id_categoria = C.id_categoria
                WHERE C.nombre_cat = 'Matemáticas'
                AND NOT EXISTS (
                    SELECT P.id_prestamo FROM PRESTAMOS P
                    WHERE P.id_usuario = U.id_usuario AND P.id_libro = L.id_libro
                )
            );
        """,
        "algebra": "(π(id_usu, id_lib)(PRESTAMOS)) ÷ (π(id_lib)(σ(cat='Matemáticas')(LIBROS)))",
        "calculo": "{ u | ∀l (l ∈ LibrosMatematicas → ∃p (p ∈ Prestamos ∧ p.usu = u ∧ p.lib = l)) }",
        "dominio": "{ <nu> | ∃id_u (<id_u, nu...> ∈ USUARIOS ∧ ∀id_l ( (∃nc ( ... nc='Matemáticas')) → ∃id_p (<id_p, id_u, id_l...> ∈ PRESTAMOS) ) ) }"
    },
    "17": {
        "titulo": "17. [División] Usuarios que han leído al menos un libro de TODAS las Editoriales",
        "sql": """
            SELECT U.nombre FROM USUARIOS U
            WHERE NOT EXISTS (
                SELECT E.id_editorial FROM EDITORIALES E
                WHERE NOT EXISTS (
                    SELECT P.id_prestamo FROM PRESTAMOS P
                    JOIN LIBROS L ON P.id_libro = L.id_libro
                    WHERE P.id_usuario = U.id_usuario AND L.id_editorial = E.id_editorial
                )
            );
        """,
        "algebra": "(π(id_usu, id_editorial)(PRESTAMOS ⨝ LIBROS)) ÷ (π(id_editorial)(EDITORIALES))",
        "calculo": "{ u | ∀e (e ∈ Editoriales → u ha prestado libro de e) }",
        "dominio": "{ <nu> | ∃id_u (<id_u, nu...> ∈ USUARIOS ∧ ∀id_e ( <id_e...> ∈ EDITORIALES → ∃id_l, id_p (<id_p, id_u, id_l...> ∈ PRESTAMOS ∧ <id_l... id_e> ∈ LIBROS) ) ) }"
    },
    "18": {
        "titulo": "18. [División] Autores que han escrito libros en TODAS las categorías",
        "sql": """
            SELECT A.nombre FROM AUTORES A
            WHERE NOT EXISTS (
                SELECT C.id_categoria FROM CATEGORIAS C
                WHERE NOT EXISTS (
                    SELECT LA.id_libro FROM LIBRO_AUTOR LA
                    JOIN LIBROS L ON LA.id_libro = L.id_libro
                    WHERE LA.id_autor = A.id_autor AND L.id_categoria = C.id_categoria
                )
            );
        """,
        "algebra": "(π(id_autor, id_cat)(LIBRO_AUTOR ⨝ LIBROS)) ÷ (π(id_cat)(CATEGORIAS))",
        "calculo": "{ a | ∀c (c ∈ Categorias → a escribió libro de c) }",
        "dominio": "{ <na> | ∃id_a (<id_a, na...> ∈ AUTORES ∧ ∀id_c (<id_c...> ∈ CATEGORIAS → ∃id_l (<id_l, id_a> ∈ LIBRO_AUTOR ∧ <id_l... id_c> ∈ LIBROS) ) ) }"
    },

    # --- GRUPO E: CUANTIFICADORES (2 Consultas) ---
    "19": {
        "titulo": "19. [Cuant. Universal] Editoriales con TODOS sus libros > $15",
        "sql": """
            SELECT E.nombre FROM EDITORIALES E
            WHERE NOT EXISTS (
                SELECT L.id_libro FROM LIBROS L
                WHERE L.id_editorial = E.id_editorial AND L.precio <= 15
            ) AND EXISTS (SELECT 1 FROM LIBROS L WHERE L.id_editorial = E.id_editorial);
        """,
        "algebra": "Editoriales - π(id_edit)(σ(precio <= 15)(LIBROS))",
        "calculo": "{ e | ∀l (l.id_edit = e.id_edit → l.precio > 15) }",
        "dominio": "{ <ne> | ∃id_e (<id_e, ne...> ∈ EDITORIALES ∧ ∀p (<...p, id_e...> ∈ LIBROS → p > 15)) }"
    },
    "20": {
        "titulo": "20. [Cuant. Universal] Categorías donde TODOS los libros han sido prestados",
        "sql": """
            SELECT C.nombre_cat FROM CATEGORIAS C
            WHERE NOT EXISTS (
                SELECT L.id_libro FROM LIBROS L
                WHERE L.id_categoria = C.id_categoria AND NOT EXISTS (
                    SELECT P.id_prestamo FROM PRESTAMOS P WHERE P.id_libro = L.id_libro
                )
            );
        """,
        "algebra": "Categorias - π(id_cat)(LIBROS - π(id_libro)(PRESTAMOS))",
        "calculo": "{ c | ∀l (l.id_cat = c.id_cat → ∃p (p.id_libro = l.id_libro)) }",
        "dominio": "{ <nc> | ∃id_c (<id_c, nc...> ∈ CATEGORIAS ∧ ∀id_l (<id_l... id_c> ∈ LIBROS → ∃id_p (<id_p... id_l...> ∈ PRESTAMOS)) ) }"
    }
}

def ejecutar_consulta(key):
    data = CONSULTAS.get(key)
    if not data:
        print("Consulta no definida.")
        return

    print(f"\n--- {data['titulo']} ---")
    print(f"\n[Álgebra Relacional]: {data['algebra']}")
    print(f"[Cálculo de Tuplas]: {data['calculo']}")
    print(f"[Cálculo de Dominios]: {data['dominio']}")
    print(f"[SQL]: {data['sql']}\n")

    conn = get_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute(data['sql'])
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        except Exception as e:
            print(f"Error SQL: {e}")
        conn.close()
    input("\nPresione Enter para continuar...")

def menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("╔════════════════════════════════════════╗")
        print("║      BIBLIOTECH - SISTEMA GESTOR       ║")
        print("╠════════════════════════════════════════╣")
        print("║ 1-5.   Operadores Básicos              ║")
        print("║ 6-10.  Reuniones / Joins               ║")
        print("║ 11-15. Agrupación y Agregación         ║")
        print("║ 16-18. División                        ║")
        print("║ 19-20. Cuantificadores Universales     ║")
        print("║                                        ║")
        print("║ 99. SEMBRAR DATOS (Reiniciar DB)       ║")
        print("║ 0. Salir                               ║")
        print("╚════════════════════════════════════════╝")
        
        opcion = input("Seleccione el número de consulta (1-20) o menú: ")

        if opcion == '0':
            print("Saliendo...")
            break
        elif opcion == '99':
            try:
                seed.run_seeder()
                input("Presione Enter...")
            except Exception as e:
                print(f"Error al sembrar datos: {e}")
                input("Presione Enter...")
        elif opcion in CONSULTAS:
            ejecutar_consulta(opcion)
        else:
            print("Opción no válida.")
            time.sleep(1)

if __name__ == "__main__":
    print("Esperando a la base de datos...")
    time.sleep(3)
    menu()