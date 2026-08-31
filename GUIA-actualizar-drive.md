# Cómo actualizar los documentos del Drive

Los documentos de este repositorio están verificados contra el código y cumplen las
plantillas de la cátedra. Los que están en Drive son de mayo y describen otro sistema.
Esta guía es el procedimiento para pasarlos.

---

## Lo que hay hoy en Drive

`Mi unidad / Proyecto de Software 2026 / Documentacion/`

| Archivo en Drive | Estado | Qué hacer |
|---|---|---|
| `TF - 2026 - Plan Del Proyecto - Wagner Nahuel .docx` | v1.2, 3 de mayo | Reemplazar contenido |
| `0.1Planificación_Iteración.docx` | v1.2, 3 de mayo | Reemplazar contenido |
| `TF - 2026 - Requerimientos - Wagner Nahuel.docx` | v1.2, 3 de mayo | Reemplazar contenido |
| `2.-Análisis.doc` | Plantilla vacía de 2023 | Convertir y completar |
| `3.-Diseño.doc` | Plantilla vacía de 2023 | Convertir y completar |

> Los tres primeros describen **45 casos de uso y cuatro actores**. Los nuestros tienen
> **108 casos y cinco actores**. No es una actualización de detalles: es otro contenido.

## Antes de empezar

**Sacá una copia de seguridad.** En Drive, clic derecho sobre la carpeta `Documentacion`
→ *Hacer una copia*. Si algo sale mal, volvés en un segundo.

**Los `.doc` de 2023 no se pueden editar directamente.** Son formato Word 97. Hay que
abrirlos con Documentos de Google, que crea una copia editable; el `.doc` original queda
como estaba.

---

## El procedimiento, documento por documento

Hacelo en este orden. Cada uno es independiente, así que podés parar y seguir después.

### 1 · Abrir el documento nuestro

En `splg-docs/drive/` hacé doble clic en el HTML que corresponde. Se abre en el navegador
con el formato ya aplicado: títulos, tablas y todo.

| Documento de la cátedra | Archivo local |
|---|---|
| 0 — Plan del Proyecto | `drive/0-Plan-del-Proyecto.html` |
| 0.1 — Planificación de Iteraciones | `drive/0.1-Planificacion-Iteraciones.html` |
| 1 — Requisitos | `drive/1-Requisitos.html` |
| 2 — Análisis | `drive/2-Analisis.html` |
| 3 — Diseño | `drive/3-Diseno.html` |

### 2 · Copiar

`Cmd+A` para seleccionar todo, `Cmd+C` para copiar. Al pegar en Documentos de Google, los
títulos y las tablas se conservan.

### 3 · Pegar en el documento de Drive

Abrí el documento de Drive, seleccioná el cuerpo —**dejando la carátula si la tiene**— y
pegá encima.

Si el documento tiene **cajas de instrucciones de la cátedra**, no las borres: movelas al
final o dejalas donde están. Son las que el profe usa para corregir.

### 4 · Insertar las imágenes

En el texto que pegaste vas a ver recuadros como este:

> **[ INSERTAR IMAGEN: DSS_CU-005_Crear-Pedido.png ]**

Cada uno te dice exactamente qué archivo va ahí. Están en `diagramas/png/` y en
`diagramas/uml/`, con el código y el nombre del caso de uso en el nombre del archivo.

En Google Docs: *Insertar → Imagen → Subir desde la computadora*, y borrás el recuadro.

| Documento | Cuántas imágenes |
|---|---|
| 0 — Plan del Proyecto | 1 (el diagrama de casos de uso del sistema) |
| 1 — Requisitos | 20 (el del sistema, el de subsistemas y los 18 por subsistema) |
| 2 — Análisis | 110 (los diagramas de secuencia del sistema) |
| 3 — Diseño | 119 (los diagramas de interacción) |

`INDICE-IMAGENES.md` tiene la correspondencia completa, caso por caso.

### 5 · Revisar el índice

*Insertar → Índice*. Si los títulos quedaron bien, el índice sale ordenado. Si aparece
algo raro, es que un título quedó con el nivel equivocado al pegar.

---

## Qué mirar al terminar

- La carátula conserva el formato de la cátedra
- Las cajas de instrucciones siguen ahí
- El índice se genera bien
- No queda ningún recuadro `[ INSERTAR IMAGEN: ... ]` sin resolver
- La Lista de Cambios tiene la entrada del 30 de agosto

## Si hay que regenerar

Si se corrige algo en los `.md`, los HTML se rehacen con:

```bash
python3 generar-html-drive.py
```

Y conviene correr antes `python3 verificar-conformidad.py`, que chequea que los
artefactos sigan cumpliendo las plantillas.
