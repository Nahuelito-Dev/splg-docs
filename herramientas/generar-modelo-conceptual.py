#!/usr/bin/env python3
"""Genera el modelo conceptual de SPLG (Larman) a partir de modelo_conceptual.py.

    python3 herramientas/generar-modelo-conceptual.py

Sale:

  diagramas/modelo-conceptual/MC_General.puml/.png/.svg      todos los conceptos, sin atributos
  diagramas/modelo-conceptual/MC_<área>.puml/.png/.svg       una vista por área, con atributos
  diagramas/modelo-conceptual/relaciones.md                  la tabla de relaciones (Doc 2, §1.3)

Va en PlantUML y no en Mermaid porque Mermaid no dibuja la dirección de lectura de una
asociación (el «▸» junto al nombre), ni la clase de asociación, ni las restricciones de un
conjunto de generalización: las tres cosas que pide la notación de Larman.
"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelo_conceptual import (CLASES, CONTEXTOS, GENERALIZACIONES, ASOCIACIONES,
                               CLASE_ASOCIACION, VISTAS)

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
SAL = D + "diagramas/modelo-conceptual/"
os.makedirs(SAL, exist_ok=True)

TINTA = "#2C4257"

CAB = f"""!include ../estilo-vp.iuml
skinparam nodesep 40
skinparam ranksep 55
skinparam packageStyle rectangle
hide circle
hide methods
hide empty members
"""

def declarar(nombre, con_atributos, referencia=False):
    c, atrs, abstracta = CLASES[nombre]
    tipo = "abstract class" if abstracta else "class"
    est = " #F1F1F1;line:8A97A3;text:55616C" if referencia else ""
    if referencia or not con_atributos or not atrs:
        return [f'{tipo} {nombre}{est}']
    return [f'{tipo} {nombre} {{'] + [f"  {a}" for a in atrs] + ["}"]

def relacion(a, ma, tipo, mb, b, nombre, con_texto=True):
    flecha = "*--" if tipo == "*" else "--"
    if not con_texto:
        return f'{a} {flecha} {b}'
    return f'{a} "{ma}" {flecha} "{mb}" {b} : {nombre} >'

def generalizaciones(nombres, foco):
    sal = []
    for padre, hijos, restr in GENERALIZACIONES:
        hs = [h for h in hijos if h in nombres and (padre in foco or h in foco)]
        if padre not in nombres or not hs: continue
        for k, h in enumerate(hs):
            sal.append(f'{padre} <|-- {h}' + (f' : {restr}' if k == 0 else ""))
    return sal

# Asociaciones que la vista general no dibuja: las que solo registran quién hizo algo
# (autoría). Cruzan todo el diagrama y lo
# vuelven ilegible; están en la vista de su área.
OMITIDAS_EN_GENERAL = set()
AUTORIA = {"origina", "efectúa", "ejecuta", "resuelve", "reporta", "realiza", "emite", "recibe"}

def asociaciones(nombres, foco, general=False):
    sal = []
    for a, ma, t, mb, b, n, _ in ASOCIACIONES:
        if general and (a in OMITIDAS_EN_GENERAL or (a == "Usuario" and n in AUTORIA and b != "AsientoAuditoria")):
            continue
        if a in nombres and b in nombres and (a in foco or b in foco):
            # también en la vista general: en Larman una asociación sin nombre ni
            # multiplicidades es un error de notación, aunque el diagrama quede denso
            sal.append((a, b, relacion(a, ma, t, mb, b, n, True)))
    return sal

def clase_de_asociacion(nombres):
    c, a, b = CLASE_ASOCIACION
    if {c, a, b} <= nombres:
        return [f"({a}, {b}) .. {c}"]
    return []

def vista(titulo, foco, ref, detalle=True, paquetes=False):
    nombres = set(foco) | set(ref)
    if CLASE_ASOCIACION[0] in foco:
        nombres.add(CLASE_ASOCIACION[0])
    lin = ["@startuml", CAB]
    if paquetes: lin += ["skinparam nodesep 18", "skinparam ranksep 35"]
    if paquetes:
        for clave, ttl in CONTEXTOS:
            miembros = [n for n in foco if CLASES[n][0] == clave]
            if not miembros: continue
            lin += sum((declarar(n, detalle) for n in miembros), [])
    else:
        for n in foco:
            lin += declarar(n, detalle)
        for n in ref:
            if n not in foco:
                lin += declarar(n, False, referencia=True)
    lin.append("")
    # generalizaciones primero: ordenan el diagrama de arriba hacia abajo
    lin += generalizaciones(nombres, set(foco))
    lin.append("")
    # PlantUML cuelga la clase de asociación del último vínculo declarado entre los dos conceptos: va justo
    # después de «usa», para que no quede sobre «tiene registrado»
    for a_, b_, l in asociaciones(nombres, set(foco), not detalle):
        lin.append(l)
        if (a_, b_) == CLASE_ASOCIACION[1:] and l.endswith(": usa >"):
            lin += clase_de_asociacion(nombres)
    if paquetes:
        lin += ["", "legend bottom right",
                "  Vista de conjunto: sin atributos (están en la vista de cada área). Se omiten las",
                "  asociaciones de Usuario que solo registran la autoría de un hecho;",
                "  figuran en la vista de su área.",
                "endlegend"]
    if ref and not paquetes:
        lin += ["", "legend bottom right",
                "  Las clases en gris pertenecen a otra vista; se muestran solo como referencia.",
                "endlegend"]
    lin.append("@enduml")
    return "\n".join(lin)

def escribir(nombre, texto):
    open(SAL + nombre + ".puml", "w", encoding="utf-8").write(texto + "\n")

# ------------------------------------------------------------------ las vistas
from cu_esenciales import CONCEPTOS_ESENCIALES
ESEN = set(CONCEPTOS_ESENCIALES)
todas = list(CLASES)
escribir("MC_General", vista("Modelo conceptual", todas, [], detalle=False, paquetes=True))
for titulo, archivo, foco, ref in VISTAS:
    escribir(archivo, vista(titulo, foco, ref))

# Documento 2: el mismo modelo recortado a los conceptos de los casos de uso esenciales
AREAS_ESEN = [("Usuarios y cuentas", "MC_Esenciales-Usuarios-y-cuentas", ["Usuarios y cuentas"]),
              ("Pedidos y pagos", "MC_Esenciales-Pedidos", ["Pedidos y pagos"]),
              ("Despacho y propuestas con vigencia", "MC_Esenciales-Despacho", ["Despacho y propuestas con vigencia"]),
              ("Flota y choferes", "MC_Esenciales-Flota", ["Flota y choferes"]),
              ("Envases y catálogo", "MC_Esenciales-Envases", ["Envases y catálogo"]),
              ("Stock, carga del camión y posventa", "MC_Esenciales-Stock-y-posventa",
               ["Stock físico", "Carga del camión", "Posventa", "Personal"])]
escribir("MC_Esenciales-General", vista("Modelo conceptual", [c for c in CLASES if c in ESEN], [], detalle=False, paquetes=True))
for titulo, archivo, origen in AREAS_ESEN:
    foco = [c for v in VISTAS if v[0] in origen for c in v[2] if c in ESEN]
    ref = [c for v in VISTAS if v[0] in origen for c in v[3] if c in ESEN and c not in foco]
    escribir(archivo, vista(titulo, foco, ref))

# ----------------------------------------------------- tabla de relaciones (Doc 2)
def tabla():
    fil = ["| Relación | Concepto A | Concepto B | Tipo | Multiplicidad | Categoría (Larman) |",
           "|----------|-----------|-----------|------|---------------|---------------------|"]
    for padre, hijos, _ in GENERALIZACIONES:
        for h in hijos:
            fil.append(f"| Es un tipo de | {h} | {padre} | Especialización | — | — |")
    for a, ma, t, mb, b, n, cat in ASOCIACIONES:
        if (a, b) == (CLASE_ASOCIACION[1], CLASE_ASOCIACION[2]) and n == "usa":
            tipo = f"Asociación (clase de asociación {CLASE_ASOCIACION[0]})"
        else:
            tipo = "Composición" if t == "*" else "Asociación"
        fil.append(f"| {n[0].upper() + n[1:]} | {a} | {b} | {tipo} | {ma} a {mb} | {cat} |")
    return "\n".join(fil) + "\n"

open(SAL + "relaciones.md", "w", encoding="utf-8").write(tabla())

n_gen = sum(len(h) for _, h, _ in GENERALIZACIONES)
print(f"  ✓ {len(CLASES)} conceptos, {len(ASOCIACIONES)} asociaciones, {n_gen} especializaciones")

# ------------------------------------------------------------------- render
entorno = dict(os.environ, PLANTUML_LIMIT_SIZE="32768")
nombres = ["MC_General"] + [v[1] for v in VISTAS] + ["MC_Esenciales-General"] + [a[1] for a in AREAS_ESEN]
for n in nombres:
    for fmt in ("png", "svg"):
        r = subprocess.run(["plantuml", "-t" + fmt, "-charset", "UTF-8", SAL + n + ".puml"],
                           capture_output=True, text=True, env=entorno)
        if r.returncode or "Error" in (r.stdout + r.stderr):
            print("  ✗", n, fmt, (r.stderr or r.stdout).strip()[:300])
    if os.path.exists(SAL + n + ".png"):
        print(f"  ✓ {n} ({os.path.getsize(SAL + n + '.png') // 1024} KB)")
