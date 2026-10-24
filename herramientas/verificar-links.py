#!/usr/bin/env python3
"""Recorre los .md y los .html del repo y verifica que cada ruta local que enlazan exista.

    python3 herramientas/verificar-links.py            # todo menos archivo/
    python3 herramientas/verificar-links.py --todo     # también archivo/

Revisa `[texto](ruta)` e `![alt](ruta)` en los .md y `src="..."` / `href="..."` en los .html.
Ignora URLs, anclas, data: y lo que arma el JavaScript de la página. Sale 1 si hay alguna rota.
"""
import collections, os, re, sys, urllib.parse

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALTAR_DIRS = {".git", "node_modules", "publicar", "__pycache__"}
EXTERNA = re.compile(r'(https?:|data:|mailto:|tel:|javascript:|#)')
todo = "--todo" in sys.argv

rotos = collections.defaultdict(set)
revisadas = 0
for raiz, dirs, archivos in os.walk(D):
    rel = os.path.relpath(raiz, D)
    dirs[:] = [d for d in dirs if d not in SALTAR_DIRS and not (not todo and rel == "." and d == "archivo")]
    for nombre in archivos:
        if not nombre.endswith((".md", ".html")):
            continue
        ruta = os.path.join(raiz, nombre)
        texto = open(ruta, encoding="utf-8", errors="replace").read()
        if nombre.endswith(".md"):
            refs = re.findall(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)', texto)
        else:
            refs = re.findall(r'(?:src|href)="([^"]+)"', texto)
        for ref in set(refs):
            if EXTERNA.match(ref) or any(c in ref for c in "'\\{$"):
                continue
            local = urllib.parse.unquote(ref.split("#")[0].split("?")[0])
            if not local:
                continue
            revisadas += 1
            destino = os.path.normpath(os.path.join(D, local.lstrip("/")) if local.startswith("/")
                                       else os.path.join(raiz, local))
            if not os.path.exists(destino):
                rotos[os.path.relpath(ruta, D)].add(ref)

total = sum(len(v) for v in rotos.values())
print(f"{revisadas} rutas locales revisadas, {total} rotas en {len(rotos)} archivos")
for archivo, refs in sorted(rotos.items()):
    for ref in sorted(refs):
        print(f"  {archivo} -> {ref}")
sys.exit(1 if total else 0)
