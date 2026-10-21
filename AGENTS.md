# splg-docs

Documentación de la tesis SPLG (Proceso Unificado, FCEQyN – UNaM) y el sitio publicado en
https://splg-atlas.netlify.app. Mapa del sistema: `../AGENTS.md`.

<!-- orq:gate: python3 verificar-conformidad.py && python3 generar-sitio.py -->

## Comandos

| Para | Comando |
|---|---|
| Gate: ¿cumple las plantillas de la cátedra? | `python3 verificar-conformidad.py` (32 chequeos, con el cruce de los DSD contra el código y los diagramas de los CU como imagen con su PNG al día) |
| DSS y DSD como imagen en `Casos-de-Uso.md`, `2-Analisis.md` y `3-Diseño.md` (Mermaid plegado debajo) | `python3 incrustar-imagenes-cu.py --aplicar` (idempotente; `--quitar` vuelve al bloque suelto). Tras tocar un `.mmd`: `material-de-trabajo/renderizar-dsd.py` y `sincronizar-diagramas.py --aplicar` |
| Regenerar el sitio | `python3 generar-sitio.py` → `splg-documentacion.html` |
| Regenerar los HTML para Drive | `python3 generar-html-drive.py` |
| Documentos de la cátedra en Word | `python3 generar-docx-catedra.py` → `entregables/catedra-docx/*.docx` (un archivo por documento; `SPLG_DOCX_LIMITE_MB=9.5` lo parte si se necesita un tope) y copia a `~/Desktop/SPLG-Documentacion-Catedra/` |
| Publicar en Netlify | `./publicar.sh` — **solo con el ok de nahue** |

## Reglas

- `README.md` explica qué archivo es qué. Los cinco documentos numerados son los que se
  entregan; `Casos-de-Uso.md` reúne los 338 CU con sus cuatro artefactos.
- Los `.md` son la fuente; los HTML se generan. No se editan HTML a mano.
- Toda afirmación sobre el sistema (endpoint, regla, estado) se comprueba contra la API
  corriendo antes de escribirla. Leer el código no alcanza.
- Diagramas: Mermaid embebido en los `.md`; MC, DER, DBD y DC también en `drawio/` (draw.io, uno por archivo).
- El sitio es el artefacto; la entrega formal de la cátedra la arma nahue en Drive.
