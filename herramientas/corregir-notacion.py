#!/usr/bin/env python3
"""Completa la notacion UML de los diagramas de secuencia.

    python3 herramientas/corregir-notacion.py            escribe la propuesta en /tmp y no toca nada
    python3 herramientas/corregir-notacion.py --aplicar  reescribe los .mmd y los documentos

Cuatro cosas que faltaban contra la notacion UML:

  1. El titulo del diagrama. Ninguno lo tenia.
  2. La activacion. Los diagramas de diseno no dibujaban el rectangulo de
     activacion sobre la linea de vida. Se empareja con una pila por
     participante: el mensaje que entra lo activa, su retorno lo desactiva.
  3. El mensaje asincrono. Un aviso push o un evento de WebSocket no espera
     respuesta: va con punta abierta, no con flecha llena.
  4. Un retorno dibujado con flecha llena.

El diagrama vive en tres lados —el .mmd suelto, el documento de la fase y el
archivo de consulta—, asi que cada cambio se replica en los tres.
"""
import re, os, sys, glob, json

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
DOCS = ["2-Analisis.md", "3-Diseño.md", "Casos-de-Uso.md"]
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "propuesta") + "/"

# ---------- 1. titulo ----------
def nombres_del_catalogo():
    """Nombre de cada caso de uso tal como figura en el catálogo de Casos-de-Uso.md §3."""
    t = open(DOC + "Casos-de-Uso.md", encoding="utf-8").read()
    return {m.group(1): m.group(2).strip()
            for m in re.finditer(r'^\| (CU-\d{3}) ([^|]+?) \| SS-\d\d \|', t, re.M)}

def titulo(base):
    m = re.match(r'(DSS|DSD)_((?:CU-\d+_)+)(.+)\.mmd$', base)
    if not m: return None
    tipo = "DSS" if m.group(1) == "DSS" else "DSD"
    cods = re.findall(r'CU-\d+', m.group(2))
    casos = " / ".join(cods)
    nombre = m.group(3).replace("-", " ").replace("_", " ").strip()
    if tipo == "DSS":
        # el título de un DSS lleva el nombre real del caso, con sus tildes
        nombre = nombres_del_catalogo().get(cods[0], nombre)
    return f"{tipo} — {casos} {nombre}"

# ---------- 3. mensajes que no esperan respuesta ----------
# El nombre solo no alcanza: se pide ademas que el destinatario no conteste.
AVISO = re.compile(r'\b(notify\w*|send\w*(Push|Notification|Confirmation|Offer\w*)|'
                   r'emit\w*|broadcast\w*|publish\w*)\s*\(', re.I)
AVISO_DSS = re.compile(r'^(aviso|notificar|notificaci|se le avisa|le llega)', re.I)

def responde(lineas, i, destino):
    """Mira si el destinatario contesta algo despues del mensaje i."""
    for l in lineas[i+1:]:
        s = l.strip()
        if re.match(rf'{destino}\s*--?->?>', s): return True
        if re.match(r'(end|else)\b', s): break
        if re.match(r'\w+\s*-->>', s) and not s.startswith(destino): continue
    return False

def transformar(src, base):
    lineas = src.split("\n")
    tipo = base.split("_")[0]
    cambios = {"titulo": 0, "activacion": 0, "asincrono": 0, "retorno": 0}

    # --- titulo, arriba de todo ---
    if not any(re.match(r'\s*title\s', l) for l in lineas):
        t = titulo(base)
        if t:
            j = next((k for k, l in enumerate(lineas) if l.strip() == "sequenceDiagram"), None)
            if j is not None:
                lineas.insert(j + 1, f"    title {t}")
                cambios["titulo"] = 1

    # --- retorno con flecha llena entre dos puntos de la misma linea de vida ---
    for i, l in enumerate(lineas):
        m = re.match(r'(\s*)(\w+)->>\2: (devuelve|retorna|responde)\b(.*)$', l)
        if m:
            lineas[i] = f"{m.group(1)}{m.group(2)}-->>{m.group(2)}: {m.group(3)}{m.group(4)}"
            cambios["retorno"] += 1

    # --- mensaje asincrono ---
    for i, l in enumerate(lineas):
        m = re.match(r'(\s*)(\w+)->>(\w+): (.+)$', l)
        if not m: continue
        sang, org, dst, txt = m.groups()
        if org == dst: continue
        es = AVISO.search(txt) if tipo == "DSD" else AVISO_DSS.match(txt.strip())
        if es and not responde(lineas, i, dst):
            lineas[i] = f"{sang}{org}-){dst}: {txt}"
            cambios["asincrono"] += 1

    # --- activacion, solo en los de diseno ---
    # Se usa activate/deactivate explicito y no el "+/-" pegado al mensaje: el
    # "+/-" exige que la pila cierre perfecto y en un diagrama con alt/else de
    # varias ramas nunca cierra, asi que 69 de 144 se quedaban sin activacion.
    # Con estado por participante se puede abrir en una rama y cerrar en otra, y
    # lo que quede abierto se cierra al terminar.
    if tipo == "DSD" and not any(re.match(r'\s*activate\b', l) for l in lineas):
        activo, salida, orden = {}, [], []
        for l in lineas:
            s = l.strip()
            sang = l[:len(l) - len(l.lstrip())] or "    "
            ret = re.match(r'(\w+)--(?:>>|\))(\w+)\s*:', s)
            env = re.match(r'(\w+)-(?:>>|\))(\w+)\s*:', s)
            if ret:
                salida.append(l)
                emisor = ret.group(1)
                if emisor != ret.group(2) and activo.get(emisor):
                    salida.append(f"{sang}deactivate {emisor}")
                    activo[emisor] = False
            elif env:
                destino = env.group(2)
                if destino != env.group(1) and not activo.get(destino):
                    salida.append(l)
                    salida.append(f"{sang}activate {destino}")
                    activo[destino] = True
                    if destino not in orden: orden.append(destino)
                else:
                    salida.append(l)
            else:
                salida.append(l)
        # lo que quedo abierto se cierra al final, del ultimo al primero
        cola = [p for p in reversed(orden) if activo.get(p)]
        for p in cola: salida.append(f"    deactivate {p}")
        cambios["activacion"] = sum(1 for l in salida if l.strip().startswith("activate "))
        lineas = salida

    return "\n".join(lineas), cambios

def main():
    aplicar = "--aplicar" in sys.argv
    os.makedirs(SALIDA, exist_ok=True)
    total = {"titulo": 0, "activacion": 0, "asincrono": 0, "retorno": 0}
    tocados, sin_activacion = 0, []
    mapa = {}

    for ruta in sorted(glob.glob(D + "diagramas/*.mmd")):
        base = os.path.basename(ruta)
        orig = open(ruta, encoding="utf-8").read()
        nuevo, c = transformar(orig.rstrip("\n"), base)
        if nuevo == orig.rstrip("\n"): continue
        tocados += 1
        for k in total: total[k] += c[k]
        if base.startswith("DSD") and not c["activacion"]: sin_activacion.append(base)
        mapa[base] = {"orig": orig.rstrip("\n"), "nuevo": nuevo}
        open(SALIDA + base, "w", encoding="utf-8").write(nuevo + "\n")

    json.dump(mapa, open(SALIDA + "_mapa.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(f"diagramas alcanzados: {tocados}")
    for k, v in total.items(): print(f"  {k:12} {v}")
    if sin_activacion:
        print(f"  sin activación (no cerraba la pila): {len(sin_activacion)}")
        for b in sin_activacion[:8]: print(f"     {b}")

    if not aplicar:
        print(f"\npropuesta escrita en {SALIDA} — nada se modificó todavía")
        return

    docs = {f: open(DOC + f, encoding="utf-8").read() for f in DOCS}
    sincronizados = huerfanos = 0
    for base, v in mapa.items():
        open(D + "diagramas/" + base, "w", encoding="utf-8").write(v["nuevo"] + "\n")
        hallado = False
        for f in docs:
            if v["orig"] in docs[f]:
                docs[f] = docs[f].replace(v["orig"], v["nuevo"]); hallado = True
        sincronizados += hallado; huerfanos += (not hallado)
    for f, t in docs.items(): open(DOC + f, "w", encoding="utf-8").write(t)
    print(f"\naplicado: {tocados} .mmd | {sincronizados} sincronizados en los documentos"
          f" | {huerfanos} sin copia en ningún documento")

if __name__ == "__main__":
    main()
