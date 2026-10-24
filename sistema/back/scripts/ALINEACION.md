# Herramientas de la alineación a Nest

Se usan en cada módulo de las tandas (ver `CONVENCIONES.md` y
`splg-docs/material-de-trabajo/DONDE-QUEDAMOS.md`).

| Archivo                              | Qué hace                                                                                                                                                    |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `modulo.sh <etiqueta> <carpetas>`    | Prettier, tsc, ESLint de las carpetas, jest, batería de Postman y comparación de formas contra la última corrida aceptada (o `newman-base1.json` si no hay) |
| `aceptar.sh <etiqueta>`              | Después de revisar y commitear un módulo, su corrida pasa a ser la referencia del siguiente                                                                 |
| `verificar.sh <etiqueta>`            | Compila, levanta el back en :3100 (el 3000 lo usa el MCP de Excalidraw), corre la colección y la apaga                                                      |
| `formas-de.py <corrida.json> <ruta>` | Muestra la forma de las respuestas 2xx de una ruta                                                                                                          |
| `tiempo-real.mjs <url> <env.json>`   | Conecta cliente, chofer y admin por socket, corre el recorrido del pedido y cuenta los eventos                                                              |
| `dsd.py CU-XXX cambios.json`         | Aplica un cambio a un DSD en sus **tres** copias (`.mmd`, `3-Diseño.md`, `Casos-de-Uso.md`)                                                                 |
| `validar-mermaid.mjs <archivos.mmd>` | Valida la sintaxis con el parser de Mermaid 10.9.1, la versión del sitio. Necesita `npm i mermaid@10.9.1 jsdom@24` en una carpeta aparte                    |
| `newman-base1.json`                  | La corrida de referencia, tomada antes de tocar los módulos. **No se versiona** (trae las contraseñas de siembra y tokens): vive sólo en esta máquina       |

Los resultados van a `$SPLG_TMP` (por defecto `/tmp/splg-alineacion`). Antes de
empezar: `mkdir -p /tmp/splg-alineacion && cp newman-base1.json /tmp/splg-alineacion/`.
