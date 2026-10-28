#!/usr/bin/env bash
# Regenera el sitio y lo publica en https://splg-atlas.netlify.app
#   ./publicar.sh               arma publicar/ y lo sube a Netlify
#   ./publicar.sh --solo-armar  arma publicar/ igual que para subir, sin subirlo
#                               (para verlo en local: python3 -m http.server -d publicar)
set -euo pipefail
cd "$(dirname "$0")"

# Versiones congeladas: sitio/versiones.json lista cada una con su `ref` (el tag
# de git de la documentacion, p. ej. v1.4.0). Cada una se publica en /<id>/ con
# SU propio generador. SPLG_REF_<ID> (p. ej. SPLG_REF_V1=v1.4.0) pisa el `ref`
# del json sin tocar el archivo. Si algun ref no existe se corta antes de armar
# nada: no se publica a medias.
echo "→ resolviendo las versiones congeladas"
VERSIONES=$(python3 - <<'PY'
import json, os
for v in json.load(open("sitio/versiones.json", encoding="utf-8"))["versiones"]:
    if v.get("congelada"):
        print(v["id"], os.environ.get("SPLG_REF_" + v["id"].upper()) or v.get("ref") or "-")
PY
)
while read -r id ref; do
  [ -z "${id:-}" ] && continue
  if [ "$ref" = "-" ]; then
    echo "✗ la version $id no tiene ref: completar \"ref\" en sitio/versiones.json o exportar SPLG_REF_$(echo "$id" | tr a-z A-Z)" >&2
    exit 1
  fi
  if ! git rev-parse --verify --quiet "$ref^{commit}" >/dev/null; then
    echo "✗ la version $id apunta a '$ref', que no existe en este repo (git fetch --tags?). No se publica nada." >&2
    exit 1
  fi
done <<< "$VERSIONES"

echo "→ regenerando el sitio"
python3 sitio/generar-sitio.py

echo "→ validando el script de la pagina"
validar_js() {
  python3 - "$1" <<'PY'
import sys
t = open(sys.argv[1], encoding="utf-8").read()
open("/tmp/_splg_check.js", "w", encoding="utf-8").write(
    t.split("<script>")[-1].split("</script>")[0])
PY
  node --check /tmp/_splg_check.js
}
validar_js sitio/splg-documentacion.html

# Todo lo que el sitio referencia. Estaba escrito a mano y se quedo corto: al
# sumar el visor, publicar habria dejado la pagina sin visor.css ni visor.js
# —404 en silencio—.
ARCHIVOS="splg-documentacion.html index.html branching.html versionado.html paginas.css visor.css visor.js"
copiar_sitio() {  # origen destino
  for f in $ARCHIVOS; do cp "$1/$f" "$2/"; done
}

echo "→ armando la carpeta"
rm -rf publicar && mkdir -p publicar
copiar_sitio sitio publicar
cp sitio/versiones.json publicar/

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
while read -r id ref; do
  [ -z "${id:-}" ] && continue
  echo "→ version $id ($ref)"
  mkdir -p "$TMP/$id" "publicar/$id"
  git archive "$ref" | tar -x -C "$TMP/$id"
  python3 "$TMP/$id/sitio/generar-sitio.py" >/dev/null
  validar_js "$TMP/$id/sitio/splg-documentacion.html"
  copiar_sitio "$TMP/$id/sitio" "publicar/$id"
done <<< "$VERSIONES"

echo "→ comprobando que no falte nada"
python3 - <<'PY'
import re, os, sys
faltan = []
for raiz, _, archivos in os.walk("publicar"):
    for f in archivos:
        if not f.endswith(".html"): continue
        ruta = os.path.join(raiz, f)
        txt = open(ruta, encoding="utf-8").read()
        for ref in set(re.findall(r'(?:src|href)="(?!https?:|#|data:)([^"?#]+)', txt)):
            if "'" in ref or "\\" in ref: continue   # los que arma el JS
            destino = os.path.join("publicar", ref.lstrip("/")) if ref.startswith("/") \
                else os.path.join(raiz, ref)
            if not os.path.exists(destino):
                faltan.append(ruta + " → " + ref)
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

if [ "${1:-}" = "--solo-armar" ]; then
  echo "✓ armado en publicar/ (sin subir)"
  exit 0
fi

echo "→ publicando"
netlify deploy --dir=publicar --prod --site=811911b2-758b-450a-a621-8bbe4911fec7
