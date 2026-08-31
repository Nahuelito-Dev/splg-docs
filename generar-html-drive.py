#!/usr/bin/env python3
"""Convierte los documentos de entrega a HTML listo para abrir con Documentos de Google.
Uso:  python3 docs/generar-html-drive.py
Salida: docs/drive/*.html  (uno por documento de la cátedra)"""
import re, os, html

D = os.path.dirname(os.path.abspath(__file__)) + "/"
OUT = D + "drive/"
DOCS = [("0-Plan_Del_Proyecto.md","0-Plan-del-Proyecto.html","Plan del Proyecto - SPLG"),
        ("0.1-Planificacion_Iteraciones.md","0.1-Planificacion-Iteraciones.html","Planificacion de Iteraciones - SPLG"),
        ("1-Requisitos.md","1-Requisitos.html","Documento de Requisitos - SPLG"),
        ("2-Analisis.md","2-Analisis.html","Documento de Analisis - SPLG"),
        ("3-Diseño.md","3-Diseno.html","Documento de Diseno - SPLG"),
        ("Casos-de-Uso.md","Casos-de-Uso.html","Casos de Uso - SPLG")]

CSS = """body{font-family:Calibri,Arial,sans-serif;font-size:11pt;line-height:1.4}
h1{font-size:20pt}h2{font-size:16pt}h3{font-size:13pt}h4{font-size:12pt}h5,h6{font-size:11pt}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #999;padding:4px 6px;vertical-align:top;font-size:10pt}
th{background:#eee;text-align:left}
pre{background:#f5f5f5;border:1px solid #ddd;padding:8px;font-size:9pt;white-space:pre-wrap}
code{font-family:Consolas,monospace;font-size:10pt}
blockquote{border-left:3px solid #ccc;margin-left:0;padding-left:12px;color:#444}"""


import glob as _glob
_PNG = [os.path.basename(x) for x in _glob.glob(D+"diagramas/png/*.png")]
def _imagen_de(codigos, tipo):
    """Busca el PNG que corresponde a ese caso de uso y tipo de diagrama."""
    for f in _PNG:
        if f.startswith(tipo+"_") and all(c in f for c in codigos): return f
    for c in codigos:
        for f in _PNG:
            if f.startswith(tipo+"_") and c in f: return f
    return None

def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',
               lambda m: ('<strong>[ INSERTAR IMAGEN: %s ]</strong>' % os.path.basename(m.group(2))),
               t)
    t = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', t)
    return t

def convertir(md):
    out, i, lineas = [], 0, md.split("\n")
    ctx = {"cods": [], "tipo": _DEFECTO}
    while i < len(lineas):
        l = lineas[i]
        if l.strip().startswith("```"):                      # bloque de código / mermaid
            leng = l.strip().strip("`")
            i += 1; buf = []
            while i < len(lineas) and not lineas[i].strip().startswith("```"):
                buf.append(lineas[i]); i += 1
            i += 1
            if leng == "mermaid":
                cods, tipo = ctx["cods"], ctx["tipo"]
                img = _imagen_de(cods, tipo) if (cods and tipo) else None
                out.append('<p style="background:#fff3cd;border:1px solid #e0a800;padding:8px 12px">'
                           '<strong>[ INSERTAR IMAGEN: %s ]</strong></p>'
                           % (img or "ver diagramas/png/"))
                continue
            rot = f"<p><em>[{leng}]</em></p>" if leng else ""
            out.append(rot + "<pre>" + html.escape("\n".join(buf)) + "</pre>"); continue
        if re.match(r'^\|', l) and i+1 < len(lineas) and re.match(r'^\|[\s:\-|]+\|\s*$', lineas[i+1]):
            cab = [c.strip() for c in l.strip().strip("|").split("|")]
            i += 2; filas = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                filas.append([c.strip() for c in lineas[i].strip().strip("|").split("|")]); i += 1
            t = ["<table><tr>"] + [f"<th>{inline(c)}</th>" for c in cab] + ["</tr>"]
            for f in filas:
                t += ["<tr>"] + [f"<td>{inline(c)}</td>" for c in f] + ["</tr>"]
            out.append("".join(t + ["</table>"])); continue
        m = re.match(r'^(#{1,6})\s+(.*)$', l)
        if m:
            titulo = m.group(2)
            cods = sorted(set(re.findall(r'CU-\d+', titulo)))
            if cods:
                ctx["cods"] = cods
                if "DSD" in titulo: ctx["tipo"] = "DSD"
                elif "DSS" in titulo: ctx["tipo"] = "DSS"
            n = len(m.group(1)); out.append(f"<h{n}>{inline(titulo)}</h{n}>"); i += 1; continue
        if re.match(r'^---+\s*$', l): out.append("<hr>"); i += 1; continue
        if l.strip().startswith(">"):
            buf = []
            while i < len(lineas) and lineas[i].strip().startswith(">"):
                buf.append(lineas[i].strip().lstrip(">").strip()); i += 1
            out.append("<blockquote>" + inline(" ".join(buf)) + "</blockquote>"); continue
        if re.match(r'^\s*[-*]\s+', l) or re.match(r'^\s*\d+\.\s+', l):
            orden = bool(re.match(r'^\s*\d+\.\s+', l)); tag = "ol" if orden else "ul"; buf = []
            while i < len(lineas) and (re.match(r'^\s*[-*]\s+', lineas[i]) or re.match(r'^\s*\d+\.\s+', lineas[i])):
                buf.append(re.sub(r'^\s*(?:[-*]|\d+\.)\s+', '', lineas[i])); i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in buf) + f"</{tag}>"); continue
        if l.strip():
            buf = []
            while i < len(lineas) and lineas[i].strip() and not re.match(r'^(#{1,6}\s|\||>|```|---+\s*$|\s*[-*]\s|\s*\d+\.\s)', lineas[i]):
                buf.append(lineas[i].rstrip()); i += 1
            if not buf:                      # la linea no encajo en ningun bloque: emitirla y avanzar
                buf = [lineas[i].rstrip()]; i += 1
            out.append("<p>" + inline("<br>".join(buf)).replace("&lt;br&gt;", "<br>") + "</p>"); continue
        i += 1
    return "\n".join(out)

os.makedirs(OUT, exist_ok=True)
for src, dst, titulo in DOCS:
    _DEFECTO = "DSD" if src.startswith("3-") else "DSS"
    cuerpo = convertir(open(D+src, encoding="utf-8").read())
    open(OUT+dst, "w", encoding="utf-8").write(
        f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{titulo}</title>'
        f'<style>\n{CSS}\n</style></head><body>\n{cuerpo}\n</body></html>')
    print(f"  {dst}  ({len(cuerpo)//1024} KB)")
print(f"\n{len(DOCS)} documentos regenerados en docs/drive/")
