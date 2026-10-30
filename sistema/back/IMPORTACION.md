# Importación masiva (API v2)

Carga de datos desde un archivo CSV o Excel en tres pasos: bajar la plantilla, subir el archivo y ver
la vista previa con los errores de cada fila, y confirmar. Nada se guarda hasta confirmar.

| Recurso | Qué hace |
|---|---|
| `garrafas` | Da de alta productos nuevos, con su stock inicial en el depósito predeterminado |
| `precios` | Cambia el precio de garrafas que ya existen, por tipo (la vista previa muestra el anterior y el nuevo) |
| `stock` | Suma o resta garrafas por depósito, tipo y condición (llena, vacía o defectuosa) |
| `proveedores` | Da de alta proveedores nuevos |

**Los clientes no se importan**: se registran solos desde la app (decisión del 28/10/2026).

## Endpoints

Base `/api/v2/imports`, sólo admin y superadmin (el superadmin con `X-Distributor`).

| Paso | Endpoint | Respuesta |
|---|---|---|
| Plantilla | `GET /:recurso/template?format=csv\|xlsx` | El archivo con el encabezado y una fila de ejemplo |
| Vista previa | `POST /:recurso/preview` (multipart, campo `file`) | `importId`, `estado` (`pending` o `with_errors`), `total`, `validas`, `errores` (fila, columna, mensaje), `vistaPrevia` y `venceEn` (24 horas) |
| Confirmar | `POST /:importId/confirm` | `estado: confirmed`, `resumen` y `yaConfirmada` |

## Reglas

- **Archivo**: CSV o `.xlsx`, hasta 5 MB y 5.000 filas. El encabezado tiene que coincidir con la
  plantilla (sin columnas de más ni faltantes). Se aceptan el BOM y la codificación de Windows.
- **Números en formato argentino**: la coma es el decimal y el punto agrupa miles (`12.500,50`; `12.500`
  es doce mil quinientos). Las celdas numéricas de Excel se leen tal cual.
- **Celdas de más**: si una fila tiene datos a la derecha de la última columna (casi siempre la coma
  decimal en un CSV separado por comas), se rechaza el archivo entero indicando las filas, para que
  nada quede corrido.
- **Se valida todo en la vista previa**: tipos y depósitos existentes, garrafas dadas de baja, precios
  mayores que cero, duplicados dentro del archivo y contra la base, y que un ajuste no deje el stock en
  negativo.
- **Confirmar** es todo o nada (una transacción). Con errores responde 400; vencida, 410; de otra
  distribuidora, 404. Repetirla no aplica nada de nuevo y devuelve `yaConfirmada: true`. El stock se
  mueve por el mismo caso de uso que los ajustes manuales, con su movimiento en el libro.
- **Limpieza**: las vistas previas no confirmadas que vencieron se borran todas las noches (3:30); las
  confirmadas quedan como historial.

Comprobado contra la API el 28/10/2026: vista previa con errores, confirmación, idempotencia, 404 de
otra distribuidora, `12.500`, fila con celdas de más y stock negativo.

## Panel

En el menú «Más» de **Garrafas** («Importar garrafas» e «Importar precios»), **Stock** («Importar
stock») y **Proveedores** («Importar proveedores»). El asistente:

1. Baja la plantilla (CSV o Excel) y recibe el archivo (arrastrar o elegir). Antes de subir controla
   el tipo y los 5 MB.
2. Muestra contadores, vencimiento, la tabla de errores y las filas válidas. Con errores, «Confirmar»
   queda apagado y pide corregir el archivo.
3. Confirma y muestra el resumen. Si la confirmación falla por vencida o con errores, pide volver a
   subir el archivo.

Al confirmar se refrescan las pantallas afectadas (garrafas, stock y sus vistas, proveedores). El
superadmin sin «Ver como» ve las opciones apagadas con el motivo.
