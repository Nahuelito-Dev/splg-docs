#!/usr/bin/env bash
# Regenera el sitio y lo publica en https://splg-atlas.netlify.app
set -euo pipefail
cd "$(dirname "$0")"

echo "→ regenerando el sitio"
python3 generar-sitio.py

echo "→ validando el script de la pagina"
python3 - <<'PY'
t = open("splg-documentacion.html", encoding="utf-8").read()
open("/tmp/_splg_check.js", "w", encoding="utf-8").write(
    t.split("<script>")[-1].split("</script>")[0])
PY
node --check /tmp/_splg_check.js

echo "→ armando la carpeta"
rm -rf publicar && mkdir -p publicar
# Todo lo que el sitio referencia. Estaba escrito a mano y se quedo corto: al
# sumar el visor y la pagina de agentes, publicar habria dejado la pagina sin
# visor.css ni visor.js —404 en silencio— y sin asistentes.html.
cp splg-documentacion.html index.html branching.html versionado.html asistentes.html \
   paginas.css visor.css visor.js publicar/

echo "→ comprobando que no falte nada"
python3 - <<'PY'
import re, os, sys
faltan = []
for f in os.listdir("publicar"):
    if not f.endswith(".html"): continue
    txt = open("publicar/" + f, encoding="utf-8").read()
    for ref in set(re.findall(r'(?:src|href)="(?!https?:|#|data:)([^"?#]+)', txt)):
        if "'" in ref or "\\" in ref: continue   # los que arma el JS
        if not os.path.exists("publicar/" + ref):
            faltan.append(f + " → " + ref)
if faltan:
    print("FALTAN archivos en la carpeta a publicar:", *sorted(set(faltan)), sep="\n  ")
    sys.exit(1)
print("  todas las referencias resuelven")
PY
# La direccion vieja quedo repartida en el Drive, en ClickUp y en Notion: se deja
# una redireccion para que ningun enlace publicado se rompa por el renombre.
cat > publicar/atlas-casos-de-uso.html <<'HTML'
<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=splg-documentacion.html">
<link rel="canonical" href="splg-documentacion.html">
<title>SPLG — Documentación del sistema</title></head>
<body><p>Esta página se mudó a <a href="splg-documentacion.html">splg-documentacion.html</a>.</p></body></html>
HTML

cat > publicar/netlify.toml <<'TOML'
[build]
  publish = "."
TOML
printf '/*\n  X-Frame-Options: SAMEORIGIN\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n' > publicar/_headers

echo "→ publicando"
netlify deploy --dir=publicar --prod --site=811911b2-758b-450a-a621-8bbe4911fec7
