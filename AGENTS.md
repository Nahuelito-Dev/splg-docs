# splg-docs

Documentación de la tesis SPLG (Proceso Unificado, FCEQyN – UNaM) y el sitio publicado en
https://splg-atlas.netlify.app. Mapa del sistema: `../AGENTS.md`.

<!-- orq:gate: python3 verificar-conformidad.py && python3 generar-sitio.py -->

## Comandos

| Para | Comando |
|---|---|
| Gate: ¿cumple las plantillas de la cátedra? | `python3 verificar-conformidad.py` (18 chequeos) |
| Regenerar el sitio | `python3 generar-sitio.py` → `splg-documentacion.html` |
| Regenerar los HTML para Drive | `python3 generar-html-drive.py` |
| Publicar en Netlify | `./publicar.sh` — **sólo con el ok de nahue** |

## Reglas

- `README.md` explica qué archivo es qué. Los cinco documentos numerados son los que se
  entregan; `Casos-de-Uso.md` reúne los 174 CU con sus cuatro artefactos.
- Los `.md` son la fuente; los HTML se generan. No se editan HTML a mano.
- Toda afirmación sobre el sistema (endpoint, regla, estado) se comprueba contra la API
  corriendo antes de escribirla. Leer el código no alcanza.
- Diagramas: Mermaid embebido en los `.md`; para Lucidchart sólo draw.io XML (MC, clases, BD).
- El sitio es el artefacto; la entrega formal de la cátedra la arma nahue en Drive.
