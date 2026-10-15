#!/usr/bin/env python3
"""Renderiza diagramas Mermaid a SVG y PNG con el estilo del repositorio.

    python3 material-de-trabajo/renderizar-dsd.py diagramas/DSD_CU-025_resolverReclamo.mmd [...]
    python3 material-de-trabajo/renderizar-dsd.py --sitio diagramas/DSD_CU-025_resolverReclamo.mmd

Salida: `diagramas/svg/<nombre>.svg` y `diagramas/png/<nombre>.png` (mermaid-cli, tema
neutral, fondo blanco, escala 2). El PNG se dibuja al tamaño natural del diagrama:
mermaid-cli lo comprime a 800 px de ancho si no se le dice otra cosa, y un diagrama de
interacción con muchas líneas de vida queda ilegible.

Con `--sitio` además dibuja el diagrama con la versión de Mermaid que carga el sitio
(10.9.1) y su tema, y avisa si no renderiza: lo que se ve en el sitio es lo que se entrega.
Eso necesita `MERMAID_SITIO` apuntando al `mermaid.min.js` 10.9.1 (por ejemplo, el de
`npm i mermaid@10.9.1` en una carpeta fuera del repositorio).

Variables de entorno, solo si el entorno no es el de siempre:
    MMDC        ruta de `mmdc` (por omisión, el de la caché de npx o el del PATH)
    CHROMIUM    ruta del ejecutable de Chromium (por omisión, el de Playwright)
"""
import glob, json, os, re, shutil, subprocess, sys, tempfile

D = os.path.dirname(os.path.abspath(__file__)) + "/../"
sys.path.insert(0, D)
from estilo_vp import MERMAID   # estilo Visual Paradigm, el mismo que el del sitio
TEMA_MERMAID = os.path.join(tempfile.gettempdir(), "splg-mermaid-vp.json")
json.dump(MERMAID, open(TEMA_MERMAID, "w"))


def buscar_mmdc():
    if os.environ.get("MMDC"):
        return os.environ["MMDC"]
    if shutil.which("mmdc"):
        return shutil.which("mmdc")
    c = sorted(glob.glob(os.path.expanduser("~/.npm/_npx/*/node_modules/.bin/mmdc")))
    if c:
        return c[-1]
    sys.exit("No encuentro mmdc: instalá @mermaid-js/mermaid-cli o definí MMDC")


def buscar_chromium():
    if os.environ.get("CHROMIUM"):
        return os.environ["CHROMIUM"]
    c = sorted(glob.glob(os.path.expanduser(
        "~/Library/Caches/ms-playwright/chromium-*/chrome-mac-arm64/"
        "Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")))
    if c:
        return c[-1]
    sys.exit("No encuentro Chromium: definí CHROMIUM")


def renderizar(mmd, mmdc, cfg):
    base = os.path.splitext(os.path.basename(mmd))[0]
    svg = D + f"diagramas/svg/{base}.svg"
    png = D + f"diagramas/png/{base}.png"
    os.makedirs(os.path.dirname(svg), exist_ok=True)
    os.makedirs(os.path.dirname(png), exist_ok=True)
    base_cmd = [mmdc, "-p", cfg, "-c", TEMA_MERMAID, "-i", mmd, "-b", "white", "-q"]
    subprocess.run(base_cmd + ["-o", svg], check=True)
    vb = re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"', open(svg, encoding="utf-8").read())
    lado = int(max(float(vb.group(1)), float(vb.group(2)))) + 1
    subprocess.run(base_cmd + ["-o", png, "-s", "2", "--size", str(lado)], check=True)
    print(f"  {base}: svg {vb.group(1)}x{vb.group(2)} · png {os.path.getsize(png) // 1024} KB")


def verificar_en_sitio(archivos, chromium):
    js = os.environ.get("MERMAID_SITIO")
    if not js or not os.path.exists(js):
        sys.exit("--sitio necesita MERMAID_SITIO=<ruta a mermaid.min.js 10.9.1>")
    nodo = sorted(glob.glob(os.path.expanduser("~/.npm/_npx/*/node_modules/puppeteer")))
    if not nodo:
        sys.exit("No encuentro puppeteer (viene con mermaid-cli)")
    plantilla = open(D + "splg-plantilla.html", encoding="utf-8").read()
    tema = re.search(r'mermaid\.initialize\((\{.*?\})\);\s*\}\s*initM\(\)', plantilla, re.S)
    if not tema:
        sys.exit("No encuentro mermaid.initialize en splg-plantilla.html")
    script = f"""
const fs = require('fs');
const puppeteer = require({json.dumps(nodo[-1])});
(async () => {{
  const b = await puppeteer.launch({{executablePath: {json.dumps(chromium)}, args: ['--no-sandbox']}});
  const p = await b.newPage();
  await p.setContent('<html><body></body></html>');
  await p.addScriptTag({{path: {json.dumps(js)}}});
  await p.evaluate(() => mermaid.initialize({tema.group(1)}));
  let errores = 0, n = 0;
  for (const f of {json.dumps(archivos)}) {{
    const r = await p.evaluate(async (s, i) => {{
      try {{ await mermaid.render('m' + i, s); return null; }} catch (e) {{ return String(e.message || e); }}
    }}, fs.readFileSync(f, 'utf8'), n++);
    if (r) {{ errores++; console.log('  ERROR en el sitio:', f, r.slice(0, 160)); }}
  }}
  console.log(`  sitio (mermaid 10.9.1): ${{n}} diagramas, ${{errores}} errores`);
  await b.close();
  process.exit(errores ? 1 : 0);
}})();
"""
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as t:
        t.write(script)
    try:
        return subprocess.run(["node", t.name]).returncode
    finally:
        os.unlink(t.name)


def main():
    args = sys.argv[1:]
    sitio = "--sitio" in args
    archivos = [os.path.abspath(a) for a in args if not a.startswith("--")]
    if not archivos:
        sys.exit(__doc__)
    mmdc, chromium = buscar_mmdc(), buscar_chromium()
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as t:
        json.dump({"executablePath": chromium, "args": ["--no-sandbox"]}, t)
    try:
        for f in archivos:
            renderizar(f, mmdc, t.name)
    finally:
        os.unlink(t.name)
    if sitio:
        sys.exit(verificar_en_sitio(archivos, chromium))


if __name__ == "__main__":
    main()
