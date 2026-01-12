# BiblioTech - Sistema de Biblioteca Universitaria

## Integrantes
- Díaz Torres Jair
- Lecona Plata Oswaldo

## Descripción
Administra el ciclo de vida completo del material bibliográfico y los usuarios de una universidad. 
El sistema permite gestionar:

Catálogo: Libros, autores, editoriales y categorización temática.

Usuarios: Perfiles diferenciados (Estudiantes, Profesores, Investigadores).

Circulación: Registro histórico de préstamos y devoluciones.

Fiscalización: Generación y seguimiento de multas por retrasos o pérdidas.

# Esquema de Base de Datos
El proyecto cumple con el requisito de mínimo 8 relaciones, implementando el siguiente esquema en PostgreSQL:

AUTORES: Datos de los escritores.

EDITORIALES: Casas publicadoras.

CATEGORIAS: Clasificación de libros (Ciencia, Novela, etc.).

LIBROS: Tabla principal del inventario.

USUARIOS: Beneficiarios del sistema.

PRESTAMOS: Tabla transaccional principal.

MULTAS: Sanciones aplicadas a préstamos.

LIBRO_AUTOR: Tabla pivote para la relación N:M entre Libros y Autores.

# Diagrama Entidad-Relación (EER)
erDiagram
    AUTORES ||--o{ LIBRO_AUTOR : escribe
    LIBROS ||--o{ LIBRO_AUTOR : tiene
    EDITORIALES ||--|{ LIBROS : publica
    CATEGORIAS ||--|{ LIBROS : clasifica
    USUARIOS ||--o{ PRESTAMOS : realiza
    LIBROS ||--o{ PRESTAMOS : es_prestado
    PRESTAMOS ||--o| MULTAS : genera

# Modelo relacional 
Tabla,Clave Primaria (PK),Claves Foráneas (FK),Descripción
AUTORES,id_autor,-,Datos de los escritores
EDITORIALES,id_editorial,-,Casas publicadoras
CATEGORIAS,id_categoria,-,"Clasificación (Ciencia, Novela...)"
LIBROS,id_libro,"id_editorial, id_categoria",Inventario principal
USUARIOS,id_usuario,-,Beneficiarios del sistema
PRESTAMOS,id_prestamo,"id_usuario, id_libro",Transacciones de circulación
MULTAS,id_multa,id_prestamo,Sanciones aplicadas
LIBRO_AUTOR,"(id_libro, id_autor)","id_libro, id_autor",Tabla pivote (Relación N:M)

# Detalle de tablas y claves foráneas:

Tabla,Clave Primaria (PK),Claves Foráneas (FK),Descripción
AUTORES,id_autor,-,Datos de los escritores
EDITORIALES,id_editorial,-,Casas publicadoras
CATEGORIAS,id_categoria,-,"Clasificación (Ciencia, Novela...)"
LIBROS,id_libro,"id_editorial, id_categoria",Inventario principal
USUARIOS,id_usuario,-,Beneficiarios del sistema
PRESTAMOS,id_prestamo,"id_usuario, id_libro",Transacciones de circulación
MULTAS,id_multa,id_prestamo,Sanciones aplicadas
LIBRO_AUTOR,"(id_libro, id_autor)","id_libro, id_autor",Tabla pivote (Relación N:M)

# Consultas complejas 
El proyecto implementa 20 consultas complejas distribuidas según la rúbrica. Cada consulta se expresa en los 4 lenguajes formales:

SQL (Implementación práctica)

Álgebra Relacional

Cálculo de Tuplas

Cálculo de Dominios

Grupo,Tipo,Cantidad,Descripción
A,Operadores Básicos,5,"Selección (σ), Proyección (π), Unión (∪), Diferencia (−)"
B,Reuniones (Joins),5,"Inner Joins, N:M Joins, Joins de 3+ tablas"
C,Agrupación,5,"Funciones de agregación (COUNT, SUM, AVG) y HAVING"
D,División,3,"Consultas de totalidad (""Usuarios que han leído todos los libros..."")"
E,Cuantificadores,2,Lógica de predicados con cuantificador universal (∀)

## Instalación y Ejecución (Docker)

Este proyecto está contenerizado. Para ejecutarlo:

1. Asegúrate de tener **Docker Desktop** instalado y corriendo.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta el siguiente comando:

\`\`\`bash
docker-compose up --build
\`\`\`

4. Una vez que inicie, verás el menú interactivo en tu terminal.
5. **IMPORTANTE:** La primera vez, selecciona la **Opción 9** para generar los datos de prueba.

## Consultas Incluidas
El sistema incluye 20 consultas complejas distribuidas en:
- Operadores Básicos
- Reuniones
- Agrupación y Agregación
- División
- Cuantificadores Universales
