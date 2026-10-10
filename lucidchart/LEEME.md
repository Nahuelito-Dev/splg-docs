# Archivos para Lucidchart

## Base de datos (CSV / TSV)

| Archivo | Contenido |
|---|---|
| `SPLG-base-de-datos-lucidchart.csv` / `.tsv` | La base real: 48 tablas, con PK y FK |
| `SPLG-base-de-datos-con-planificadas-lucidchart.csv` / `.tsv` | La base con los módulos planificados: 82 tablas |

En Lucidchart: **Archivo → Importar datos → Entity Relationship (ERD) → Importar desde: SQL Database → PostgreSQL**. Saltear el paso de correr la consulta (ya está corrida: es `material-de-trabajo/lucidchart-erd-postgresql.sql`) y **subir el CSV** (o pegar el contenido del TSV). Las tablas aparecen en el panel lateral y se arrastran al lienzo con sus relaciones.

## Modelo conceptual y clases (texto)

En `texto/` están las fuentes en **Mermaid** (`*-mermaid.txt`) y **PlantUML** (`*-plantuml.txt`). En Lucidchart: **Insertar → Diagrama como código** (Mermaid o PlantUML) y pegar el contenido. También quedan los `.xml` de draw.io (Archivo → Importar → Draw.io) para quien tenga esa opción.

Todo se regenera con `python3 generar-lucidchart.py` (necesita la base corriendo en Docker).

---

# Lucidchart — los archivos para importar

El modelo conceptual y el diagrama de clases de diseño los genera `generar-lucidchart.py`.
El diagrama de clases de diseño **se deriva de los DSD** (`material-de-trabajo/generar-clases-diseno.py`
lee `diagramas/DSD_*.mmd` y el modelo conceptual y escribe las fuentes `.mmd`). Nada se edita a
mano: si cambia un DSD, se corren de nuevo.

```bash
python3 generar-modelo-conceptual.py        # el .mmd del modelo conceptual, desde modelo_conceptual.py
python3 material-de-trabajo/generar-clases-diseno.py   # el diagrama de clases de diseño, desde los DSD
python3 generar-lucidchart.py
```

## Qué es cada uno

| Archivo | Diagrama | Cómo entra a Lucidchart |
|---|---|---|
| `SPLG-modelo-conceptual.xml` | Modelo conceptual del dominio, 80 conceptos | Archivo · Importar |
| `SPLG-diagrama-de-clases-dominio.xml` | Las 80 clases de dominio con atributos tipados, operaciones y navegabilidad | Archivo · Importar |
| `clases/SPLG-diagrama-de-clases-<vista>.xml` | Controladores, fabricaciones puras, puertos y colecciones de un módulo (o grupo de módulos), con sus operaciones | Archivo · Importar |
| `SPLG-diagrama-de-base-de-datos.sql` | Entidad-relación de lo implementado: las 43 tablas que tiene la base y sus 96 claves foráneas | Importar datos · ERD |
| `SPLG-diagrama-de-base-de-datos-con-planificadas.sql` | Entidad-relación de lo implementado más lo planificado: las 43 tablas de la base y las 36 de los módulos de personal, flota ampliada, stock y compras, y caja y rendición (79 tablas y 215 claves foráneas) | Importar datos · ERD |

Las clases de diseño no entran en un solo diagrama: `generar-clases-diseno.py` las reparte en
vistas por módulo (por ejemplo `Pedidos-alta`, `Despacho`, `Flota-tareas`). Las cifras y la lista
de vistas están en `material-de-trabajo/indice-clases-diseno.md`. Las imágenes del diagrama,
con la notación UML completa (estereotipos, interfaces, navegabilidad), están en
`diagramas/clases-diseno/` y las muestra el Documento 3 §5.

## Importar los `.xml`

1. Entrar a Lucidchart.
2. **Archivo · Importar diagrama**.
3. Elegir el origen **Draw.io** y subir el `.xml`.
4. Lucidchart abre el diagrama con las cajas ya acomodadas y las relaciones
   dibujadas.

Los `.xml` son diagramas de draw.io, que es uno de los formatos que Lucidchart
importa de fábrica junto con Visio, Gliffy y OmniGraffle. Se eligió ese y no
Mermaid porque Mermaid en Lucidchart no es una importación: hay que pegar el
código dentro del editor y no admite estilos.

## Importar el `.sql`

1. **Importar datos · Entity Relationship (ERD)**.
2. Origen **PostgreSQL**.
3. Pegar o subir el archivo.

Lucidchart arma una tabla por cada `CREATE TABLE` y una línea por cada clave
foránea. Hay dos archivos y se importa el que se necesite, no los dos juntos:

- `SPLG-diagrama-de-base-de-datos.sql` es el estado real de la base (`splg_db`): las tablas
  implementadas, con las de adjuntos, numeración de comprobantes y archivos pendientes de borrar.
- `SPLG-diagrama-de-base-de-datos-con-planificadas.sql` suma las tablas de los módulos que todavía
  no se construyeron. Es la imagen completa del sistema una vez terminadas las iteraciones I-11 a I-14.

Los dos son SQL portable: sólo `CREATE TABLE` con sus claves primarias, únicas y foráneas, sin tipos
enumerados ni de PostGIS, que el importador no entiende. Se cargan sin errores en un PostgreSQL
común. El detalle de qué trae cada volcado está en `diagramas/base-de-datos/LEEME.md`.

## La notación que sale dibujada

| Relación | Cómo se ve |
|---|---|
| Asociación | Línea sin punta, con la multiplicidad en cada extremo |
| Composición | Rombo relleno del lado del todo |
| Agregación | Rombo hueco del lado del todo |
| Generalización | Punta triangular hueca hacia la clase padre |
| Dependencia | Línea punteada con punta abierta |

La visibilidad va escrita en cada atributo y cada operación: `+` público,
`-` privado, `#` protegido. Los estereotipos van entre comillas francesas, como
`«enumeration»`.
