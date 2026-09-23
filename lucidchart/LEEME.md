# Lucidchart — los cuatro archivos para importar

Los genera `generar-lucidchart.py`, que está en la raíz del repositorio. No se
editan a mano: si cambia un diagrama, se vuelve a correr.

```bash
python3 generar-lucidchart.py
```

## Qué es cada uno

| Archivo | Diagrama | Cómo entra a Lucidchart |
|---|---|---|
| `SPLG-modelo-conceptual.xml` | Modelo conceptual del dominio, 22 conceptos | Archivo · Importar |
| `SPLG-diagrama-de-clases-dominio.xml` | Clases de dominio con atributos y multiplicidades | Archivo · Importar |
| `SPLG-diagrama-de-clases-servicios.xml` | Clases de servicio con las operaciones reales | Archivo · Importar |
| `SPLG-diagrama-de-base-de-datos.sql` | Entidad-relación, 25 tablas | Importar datos · ERD |

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
foránea. El detalle de qué trae ese volcado está en
`diagramas/base-de-datos/LEEME.md`.

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
