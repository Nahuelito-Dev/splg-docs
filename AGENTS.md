# splg-docs

Documentación de la tesis SPLG (Proceso Unificado, FCEQyN – UNaM) y el sitio publicado en
https://splg-atlas.netlify.app. Mapa del sistema: `../AGENTS.md`.

<!-- orq:gate: python3 herramientas/verificar-conformidad.py && python3 sitio/generar-sitio.py -->

## Comandos

| Para | Comando |
|---|---|
| Gate: ¿cumple las plantillas de la cátedra? | `python3 herramientas/verificar-conformidad.py` (33 chequeos, con el cruce de los DSD contra el código y los diagramas de los CU como imagen con su PNG al día) |
| DSS y DSD como imagen en `documentos/Casos-de-Uso.md`, `documentos/2-Analisis.md` y `documentos/3-Diseño.md` (Mermaid plegado debajo) | `python3 herramientas/incrustar-imagenes-cu.py --aplicar` (idempotente; `--quitar` vuelve al bloque suelto). Tras tocar un `.mmd`: `herramientas/renderizar-dsd.py` y `herramientas/sincronizar-diagramas.py --aplicar` |
| Regenerar el sitio | `python3 sitio/generar-sitio.py` → `sitio/splg-documentacion.html` |
| Regenerar los HTML para Drive | `python3 herramientas/generar-html-drive.py` → `catedra/drive/` |
| Documentos de la cátedra en Word | `python3 herramientas/generar-docx-catedra.py` → `catedra/entregables/catedra-docx/*.docx` (un archivo por documento; `SPLG_DOCX_LIMITE_MB=9.5` lo parte si se necesita un tope) y copia a `~/Desktop/SPLG-Documentacion-Catedra/` |
| ¿Algún link roto? | `python3 herramientas/verificar-links.py` (los .md y los .html; sale 1 si alguna ruta local no existe) |
| Publicar en Netlify | `./publicar.sh` — **solo con el ok de nahue**. Publica la raíz y cada versión congelada de `sitio/versiones.json` en `/<id>/`; falla antes de armar nada si un `ref` (tag) no existe. `SPLG_REF_V1=<tag>` pisa el `ref` de la v1 |

## Estructura

| Carpeta | Qué hay |
|---|---|
| `documentos/` | los cinco documentos de la cátedra, `Casos-de-Uso.md`, `INDICE-IMAGENES.md` y las guías |
| `modelos/` | `drawio/` (MC, DER, DBD, DC) y `base-de-datos/` (SQL, `SPLG-modelo.json`, DER por módulo) |
| `diagramas/` | DSS, DSD, CU y pantallas (`.mmd`, PNG, SVG, PlantUML) |
| `sistema/` | documentación técnica del código (back, Postman, setup); se mantiene acá, no en los repos de código |
| `capturas/` | capturas reales del panel y de las apps |
| `catedra/` | `drive/`, `entregables/`, `.catedra-ref/` y `material-de-trabajo/` |
| `sitio/` | generador y archivos del sitio publicado |
| `herramientas/` | los scripts de generación y verificación (`*.py`, `scripts/`) |
| `archivo/` | `doc-old/`, histórico |

## Reglas

- `README.md` explica qué carpeta es qué. Los cinco documentos numerados (en `documentos/`) son los que se
  entregan; `documentos/Casos-de-Uso.md` reúne los 338 CU con sus cuatro artefactos.
- Los links de los `.md` de `documentos/` a las imágenes son relativos a esa carpeta (`../diagramas/...`).
- Los `.md` son la fuente; los HTML se generan. No se editan HTML a mano.
- Toda afirmación sobre el sistema (endpoint, regla, estado) se comprueba contra la API
  corriendo antes de escribirla. Leer el código no alcanza.
- Diagramas: Mermaid embebido en los `.md`; MC, DER, DBD y DC también en `modelos/drawio/` (draw.io, uno por archivo).
- Versiones del sitio: v1 congelada el 24/10/2026 (tag + rama `release/v1`), v2 en `develop`. Para sumar una: tag, entrada en `sitio/versiones.json` (`congelada: true`) y `actual` con el título de la siguiente; el selector de la plantilla lee `/versiones.json`.
- El sitio es el artefacto; la entrega formal de la cátedra la arma nahue en Drive.
