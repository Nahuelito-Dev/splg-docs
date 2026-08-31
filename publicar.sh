#!/usr/bin/env bash
# Regenera el atlas y lo publica en https://splg-atlas.netlify.app
set -euo pipefail
cd "$(dirname "$0")"

echo "→ regenerando el atlas"
python3 generar-atlas.py

echo "→ validando el script de la pagina"
python3 - <<'PY'
t = open("atlas-casos-de-uso.html", encoding="utf-8").read()
open("/tmp/_atlas_check.js", "w", encoding="utf-8").write(
    t.split("<script>")[-1].split("</script>")[0])
PY
node --check /tmp/_atlas_check.js

echo "→ armando la carpeta"
rm -rf publicar && mkdir -p publicar
cp atlas-casos-de-uso.html index.html publicar/
cat > publicar/netlify.toml <<'TOML'
[build]
  publish = "."
TOML
printf '/*\n  X-Frame-Options: SAMEORIGIN\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n' > publicar/_headers

echo "→ publicando"
netlify deploy --dir=publicar --prod --site=811911b2-758b-450a-a621-8bbe4911fec7
