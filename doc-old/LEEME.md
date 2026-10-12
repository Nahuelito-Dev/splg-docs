# doc-old

Material que ya no forma parte de la documentación vigente de SPLG. Se conserva acá, con
la misma ruta relativa que tenía, para consulta: notas de trabajo superadas, auditorías y
estados de fechas anteriores, capturas y diagramas reemplazados.

Nada de esta carpeta se publica en el sitio ni lo leen los scripts de generación y
verificación. Si algo vuelve a usarse, se mueve de nuevo a su ruta original.

## diagramas-clases-codigo/

El diagrama de clases de diseño que se generaba del código del backend (clases con decoradores de
TypeScript, sin operaciones en el dominio): su generador (`generar-clases-codigo.py`, que necesita
`material-de-trabajo/extraer-clases-codigo.py`), las fuentes Mermaid (`mmd/`), el índice y los
`.xml` de draw.io. Lo reemplaza el diagrama derivado de los DSD (`3-Diseño.md` §5); la
correspondencia con el código queda en las tablas de implementación de cada DSD.
