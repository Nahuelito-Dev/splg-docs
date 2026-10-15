#!/usr/bin/env python3
"""Trazabilidad CU <-> IRQ y CU <-> OBJ de la matriz del Documento 1.

    python3 material-de-trabajo/trazabilidad-cu-irq.py             informa las diferencias
    python3 material-de-trabajo/trazabilidad-cu-irq.py --aplicar   reescribe las listas de los IRQ y la matriz

La fuente es el caso de uso expandido: su campo «Requisitos asociados» dice a qué requisitos de
información (IRQ) responde y su campo «Objetivos asociados», qué objetivos (OBJ) alcanza. De ahí salen:

  - el campo «Requisitos asociados» de cada IRQ (§6 del Documento 1): los casos que lo citan;
  - las filas de los casos de uso de la matriz de rastreabilidad (§9): las marcas de sus objetivos.

Las dos direcciones tienen que cerrar: un IRQ que lista un caso que no lo cita, o un caso que cita un
IRQ que no lo lista, es una diferencia. El gate (`verificar-conformidad.py`) la controla con `verificar()`.
"""
import os, re, sys

D = os.path.dirname(os.path.abspath(__file__)) + "/../"
DOC = D + "1-Requisitos.md"


def _leer():
    return open(DOC, encoding="utf-8").read()


def casos_expandidos(txt):
    """{CU: (irqs, objs)} de los CUE de la sección 7."""
    a = txt.index("\n## 7. "); b = txt.index("\n## 8. ")
    sec = txt[a:b]
    out = {}
    for m in re.finditer(r'^#### [^\n]*?(CU-\d+) — [^\n]*\n(.*?)(?=^#{1,4} |\Z)', sec, re.M | re.S):
        cuerpo = m.group(2)
        irq = re.search(r'\| \*\*Requisitos asociados\*\* \| ([^|]*?) \|', cuerpo)
        obj = re.search(r'\| \*\*Objetivos asociados\*\* \| ([^|]*?) \|', cuerpo)
        out[m.group(1)] = (re.findall(r'IRQ-\d+', irq.group(1)) if irq else [],
                           re.findall(r'OBJ-\d+', obj.group(1)) if obj else [])
    return out


def irqs_listados(txt):
    """{IRQ: [CU...]} del campo «Requisitos asociados» de cada IRQ en la sección 6."""
    a = txt.index("\n## 6. "); b = txt.index("\n## 7. ")
    sec = txt[a:b]
    out = {}
    for m in re.finditer(r'^### (IRQ-\d+) — [^\n]*\n(.*?)(?=^### |\Z)', sec, re.M | re.S):
        r = re.search(r'\| \*\*Requisitos asociados\*\* \| ([^|]*?) \|', m.group(2))
        out[m.group(1)] = re.findall(r'CU-\d+', r.group(1)) if r else []
    return out


def num(c): return int(c.split("-")[1])


def calcular(txt=None):
    txt = txt or _leer()
    cue = casos_expandidos(txt)
    listados = irqs_listados(txt)
    esperado = {i: sorted({c for c, (irq, _) in cue.items() if i in irq}, key=num) for i in listados}
    return cue, listados, esperado


def diferencias(txt=None):
    txt = txt or _leer()
    cue, listados, esperado = calcular(txt)
    errores = []
    for i, lst in listados.items():
        falt = sorted(set(esperado[i]) - set(lst), key=num)
        sobr = sorted(set(lst) - set(esperado[i]), key=num)
        if falt: errores.append(f"{i} no lista {len(falt)} caso(s) que lo citan: {', '.join(falt[:8])}{'…' if len(falt) > 8 else ''}")
        if sobr: errores.append(f"{i} lista {len(sobr)} caso(s) que no lo citan: {', '.join(sobr[:8])}{'…' if len(sobr) > 8 else ''}")
    inexistentes = sorted({x for irq, _ in cue.values() for x in irq if x not in listados})
    if inexistentes: errores.append(f"casos que citan IRQ inexistentes: {inexistentes}")
    sin_irq = sorted(c for c, (irq, _) in cue.items() if not irq)
    if sin_irq: errores.append(f"casos sin IRQ: {sin_irq}")
    # matriz: la fila de cada caso sale de sus objetivos
    objs = sorted({o for _, (_, ob) in cue.items() for o in ob}, key=lambda x: int(x.split("-")[1]))
    m = re.search(r'^\|\s*\| (OBJ-01 \|.*)$', txt, re.M)
    cols = re.findall(r'OBJ-\d+', m.group(0)) if m else []
    filas = {r.group(1): [c.strip() for c in r.group(0).split("|")[2:-1]]
             for r in re.finditer(r'^\| \*\*(CU-\d+)\*\* \|.*\|$', txt, re.M)}
    for c, (_, ob) in cue.items():
        esp = [("●" if o in ob else "") for o in cols]
        if c not in filas:
            errores.append(f"la matriz no tiene la fila de {c}")
        elif filas[c] != esp:
            errores.append(f"la fila de {c} en la matriz no es la de sus objetivos {ob}")
    for c in filas:
        if c not in cue: errores.append(f"la matriz tiene la fila de {c}, que no existe")
    return errores


def aplicar():
    txt = _leer()
    cue, listados, esperado = calcular(txt)
    # 1. lista de casos de cada IRQ
    a = txt.index("\n## 6. "); b = txt.index("\n## 7. ")
    sec = txt[a:b]
    for i, lst in esperado.items():
        sec = re.sub(r'(### %s — [^\n]*\n(?:(?!### ).*\n)*?\| \*\*Requisitos asociados\*\* \| )[^|]*?( \|)' % i,
                     lambda m: m.group(1) + ", ".join(lst) + m.group(2), sec, count=1)
    txt = txt[:a] + sec + txt[b:]
    # 2. filas de los casos en la matriz
    m = re.search(r'^\|\s*\| (OBJ-01 \|.*)$', txt, re.M)
    cols = re.findall(r'OBJ-\d+', m.group(0))
    a = txt.index("\n## 9. "); b = txt.index("\n## 10. ")
    sec = txt[a:b]
    filas = [l for l in sec.split("\n") if re.match(r'^\| \*\*CU-\d+\*\* \|', l)]
    nuevas = [f"| **{c}** | " + " | ".join(("●" if o in ob else "") for o in cols) + " |" for c, (_, ob) in sorted(cue.items(), key=lambda kv: num(kv[0]))]
    if filas:
        ini = sec.index(filas[0]); fin = sec.index(filas[-1]) + len(filas[-1])
        sec = sec[:ini] + "\n".join(nuevas) + sec[fin:]
    txt = txt[:a] + sec + txt[b:]
    open(DOC, "w", encoding="utf-8").write(txt)


def verificar():
    """(errores, cantidad de casos) para el gate."""
    return diferencias(), len(casos_expandidos(_leer()))


if __name__ == "__main__":
    if "--aplicar" in sys.argv:
        aplicar(); print("aplicado")
    errs = diferencias()
    for e in errs[:40]: print("  ✗", e)
    print(f"{len(errs)} diferencias")
    sys.exit(1 if errs else 0)
