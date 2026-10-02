#!/usr/bin/env python3
"""Numera las figuras de los documentos y arma el índice que pide la cátedra.

    python3 numerar-figuras.py            muestra lo que haría
    python3 numerar-figuras.py --aplicar  escribe los documentos

La plantilla rotula cada figura como «Figura # - Descripción» y pide un Índice de
Figuras. Los documentos tenían 303 diagramas y 5 epígrafes. El rótulo sale del
encabezado que ya nombra a cada diagrama, así que no hay que escribir 303 títulos.
"""
import re, sys, os

D = os.path.dirname(os.path.abspath(__file__)) + "/"
DOCS = ["0-Plan_Del_Proyecto.md", "0.1-Planificacion_Iteraciones.md",
        "1-Requisitos.md", "2-Analisis.md", "3-Diseño.md"]

RE_EPIGRAFE = re.compile(r'^\s*\*{0,2}Figura\s+\d+\s*[—-]\s*(.+?)\*{0,2}\s*$', re.I)
# Las vistas parciales de un mismo diagrama (el modelo conceptual por área, por
# ejemplo) se rotulan «Figura N.k»: cuelgan de la figura N y no desplazan la
# numeración del resto del documento.
RE_SUBFIGURA = re.compile(r'^\s*\*{0,2}Figura\s+\d+\.\d+\s*[—-]\s*(.+?)\*{0,2}\s*$', re.I)
# Algunos documentos ya traian el epigrafe escrito a mano y sin numerar, encima
# de la figura. Su texto suele ser mejor que el del encabezado, asi que se lo
# adopta y se quita, para no terminar con la figura rotulada dos veces.
RE_SIN_NUMERO = re.compile(r'^\s*\*{0,2}Figura\s*[—-]\s*(.+?)\*{0,2}\s*$', re.I)

def limpiar(t):
    t = re.sub(r'^\d+(\.\d+)*\.?\s+', '', t)
    t = re.sub(r'\*\*|`', '', t)
    t = re.sub(r'\b(Crítico|Importante|Secundario)\s*·?\s*(automático)?\s*[—-]?\s*', '', t, flags=re.I)
    t = re.sub(r'^(Especificado|Pendiente|Implementado|Planificado)[^·]*·\s*', '', t, flags=re.I)
    t = re.sub(r'\s*[—-]\s*(DSS|DSD)\s*[—-]\s*', ' ', t)
    t = re.sub(r'^(DSS|DSD)\s*[—-]\s*', r'\1 ', t)
    return t.strip()

# Un encabezado como «Diagrama de Interacción» no identifica nada: se repite en
# cada caso de uso real. Cuando el más cercano no nombra el artefacto, se sube
# hasta el que sí lo hace y se combinan.
IDENTIFICA = re.compile(r'(CU-\d+|SS-\d+|M\d+\b|IRQ-|NFR-|OBJ-)')

def rotulo(lineas, i):
    """El encabezado que identifica al diagrama, mirando hacia arriba."""
    cercano = None
    for j in range(i - 1, -1, -1):
        m = re.match(r'^(#{2,6})\s+(.*)$', lineas[j])
        if not m: continue
        t = limpiar(m.group(2))
        if not t: continue
        if IDENTIFICA.search(t):
            return f"{t} — {cercano}" if cercano and cercano.lower() not in t.lower() else t
        if cercano is None:
            cercano = t
        elif len(m.group(1)) <= 2:
            # se llegó a una sección de primer nivel sin encontrar un código
            return cercano
    return cercano or "Diagrama"

def procesar(archivo):
    lineas = open(D + archivo, encoding="utf-8").read().split("\n")
    salida, indice, n, i = [], [], 0, 0
    sub = 0
    heredado = None
    while i < len(lineas):
        l = lineas[i]

        # epígrafe escrito a mano sin numerar, encima de la figura
        m0 = RE_SIN_NUMERO.match(l)
        if m0 and not RE_EPIGRAFE.match(l) and not l.strip().startswith(">"):
            heredado = m0.group(1).strip()
            i += 1
            continue

        # vista parcial: se renumera como N.k respecto de la última figura
        ms = RE_SUBFIGURA.match(l)
        if ms and not l.strip().startswith(">"):
            sub += 1
            salida.append(f"**Figura {n}.{sub} — {ms.group(1).strip()}**")
            indice.append((f"{n}.{sub}", ms.group(1).strip()))
            i += 1
            continue

        # un epígrafe que ya estaba: se renumera y se toma su texto
        m = RE_EPIGRAFE.match(l)
        if m and not l.strip().startswith(">"):
            n += 1
            sub = 0
            salida.append(f"**Figura {n} — {m.group(1).strip()}**")
            indice.append((n, m.group(1).strip()))
            i += 1
            continue

        # un bloque de código que no es un diagrama se copia entero: lo que haya
        # adentro son ejemplos, no figuras del documento
        if l.strip().startswith("```") and not l.strip().startswith("```mermaid"):
            fin = i + 1
            while fin < len(lineas) and not lineas[fin].strip().startswith("```"): fin += 1
            salida += lineas[i:fin + 1]
            i = fin + 1
            continue

        # bloque de diagrama
        if l.strip().startswith("```mermaid"):
            fin = i + 1
            while fin < len(lineas) and not lineas[fin].strip().startswith("```"): fin += 1
            inicio = i
            salida += lineas[i:fin + 1]
            i = fin + 1
            # si ya venía rotulado abajo, ese caso lo toma la rama de arriba
            sig = next((k for k in range(i, min(i + 3, len(lineas))) if lineas[k].strip()), None)
            if sig is not None and (RE_EPIGRAFE.match(lineas[sig]) or RE_SUBFIGURA.match(lineas[sig])): continue
            n += 1
            sub = 0
            t = heredado or rotulo(lineas, inicio); heredado = None
            indice.append((n, t))
            salida += ["", f"**Figura {n} — {t}**"]
            continue

        # imagen suelta
        if re.match(r'^\s*!\[', l):
            salida.append(l)
            i += 1
            sig = next((k for k in range(i, min(i + 3, len(lineas))) if lineas[k].strip()), None)
            if sig is not None and (RE_EPIGRAFE.match(lineas[sig]) or RE_SUBFIGURA.match(lineas[sig])): continue
            prev = next((s for s in reversed(salida[:-1]) if s.strip()), "")
            if RE_EPIGRAFE.match(prev) or RE_SUBFIGURA.match(prev): continue      # ya rotulada arriba
            n += 1
            sub = 0
            t = heredado or rotulo(lineas, i); heredado = None
            indice.append((n, t))
            salida += ["", f"**Figura {n} — {t}**"]
            continue

        salida.append(l)
        i += 1
    return "\n".join(salida), indice

def con_indice(texto, indice):
    """Mete el índice después del primer encabezado de nivel 1."""
    if not indice: return texto
    bloque = ["", "## Índice de Figuras", ""]
    bloque += [f"- Figura {k} — {t}" for k, t in indice]
    bloque += ["", "---"]
    lineas = texto.split("\n")
    # si ya existe, se reemplaza entero
    ini = next((i for i, l in enumerate(lineas) if l.strip() == "## Índice de Figuras"), None)
    if ini is not None:
        fin = next(i for i in range(ini + 1, len(lineas)) if lineas[i].strip() == "---")
        return "\n".join(lineas[:ini] + bloque[1:] + lineas[fin + 1:])
    corte = next((i for i, l in enumerate(lineas) if re.match(r'^##\s+\w', l)), 1)
    return "\n".join(lineas[:corte] + bloque + [""] + lineas[corte:])

def main():
    aplicar = "--aplicar" in sys.argv
    for f in DOCS:
        texto, indice = procesar(f)
        texto = con_indice(texto, indice)
        print(f"  {f}: {len(indice)} figuras")
        if aplicar: open(D + f, "w", encoding="utf-8").write(texto)
    print("aplicado" if aplicar else "\nnada se escribió todavía")

if __name__ == "__main__":
    main()
