# Modelo de datos de SPLG — qué es cada archivo

Todo lo que hay en esta carpeta lo genera `generar-modelo-datos.py`, que está en
la raíz del repo y lee la base en ejecución (contenedor `splg-bd`). No se
edita nada a mano: si cambia la base, se vuelve a correr.

```bash
python3 generar-modelo-datos.py
```

## Los archivos

| Archivo | Qué es | Para qué sirve |
|---|---|---|
| `SPLG-base-de-datos.sql` | Volcado de `pg_dump`, esquema completo | Recrear la base tal cual está |
| `SPLG-base-de-datos-lucidchart.sql` | Sólo lo implementado, en SQL portable | Diagramar el estado actual |
| `SPLG-base-de-datos-propuesta.sql` | Sólo los agregados de la cátedra | Boceto de la migración que falta |
| `SPLG-base-de-datos-completa-lucidchart.sql` | Actual + propuesta, en SQL portable | **El que se importa en Lucidchart** |
| `SPLG-modelo-fisico.png` / `.svg` | Entidad-relación con tablas y columnas | La lámina técnica |
| `SPLG-modelo-conceptual.png` / `.svg` | Entidades del negocio y cardinalidades | La lámina para la defensa |
| `SPLG-modelo-de-datos.md` | Diccionario de datos y sustento escrito | El texto del informe |

En los dos diagramas, lo que ya está implementado va en blanco con borde oscuro
y lo propuesto en celeste con el estereotipo `<<propuesto>>`. Las relaciones que
existen en el dominio pero que la base no declara como clave foránea van con
línea punteada y la etiqueta «sin FK»; en el modelo físico, la columna que las
sostiene lleva la marca `<<ref>>` en lugar de `<<FK>>`.

`SPLG-base-de-datos-propuesta.sql` es PostgreSQL válido: agrega tipos, columnas
y tablas sobre el esquema que ya está, sin tocar los datos existentes.

## Importar en Lucidchart

1. Entrar a Lucidchart y abrir un documento en blanco.
2. En el panel izquierdo, **Import Data** (o *Archivo · Importar datos*).
3. Elegir **Entity Relationship (ERD)**.
4. Elegir el origen **PostgreSQL**.
5. Pegar el contenido de `SPLG-base-de-datos-completa-lucidchart.sql`
   (o subir el archivo, según lo que ofrezca la versión).
6. **Import**. Lucidchart arma una tabla por cada `CREATE TABLE` y una línea por
   cada `FOREIGN KEY`.

Notas para que la importación salga limpia:

- Usar el archivo `-lucidchart.sql`, no `SPLG-base-de-datos.sql`: el volcado de
  `pg_dump` trae `CREATE TYPE`, `CREATE EXTENSION postgis`, índices y funciones
  que el importador no entiende.
- En los archivos portables los tipos enumerados se escriben `varchar(32)` y las
  columnas geográficas de PostGIS `varchar(255)`. La lista de valores de cada
  enumerado está en `SPLG-modelo-de-datos.md`.
- Lucidchart dibuja todas las relaciones iguales: la distinción entre
  implementado, propuesto y «sin FK» sólo se ve en los diagramas de esta carpeta
  y está escrita en el `.md`.
- Si se quiere el estado actual sin los agregados, importar
  `SPLG-base-de-datos-lucidchart.sql`.

## Qué pegarle a Gemini

Para que revise el modelo, el archivo que conviene pasarle es
**`SPLG-modelo-de-datos.md`**: es el único que trae, en un solo texto, el
diccionario de datos, las relaciones que faltan declarar y los agregados
pedidos, cada uno con el motivo por el que está.

Si además se quiere que revise el DDL, sumar
**`SPLG-base-de-datos-completa-lucidchart.sql`**, que es el modelo entero en
menos de 22 KB.
No conviene pegar `SPLG-base-de-datos.sql`: son 74 KB
en su mayoría de índices y funciones de PostGIS que no aportan al análisis del
modelo.

Un pedido que funciona bien:

> Adjunto el modelo de datos de un sistema de pedidos y logística de garrafas de
> gas. Revisá normalización, integridad referencial, cardinalidades y nombres.
> Señalá redundancias y relaciones que falten. Tené en cuenta que la sección
> «Modelo propuesto» todavía no está implementada.
