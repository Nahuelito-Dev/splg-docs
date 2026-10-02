#!/usr/bin/env python3
"""Genera el diagrama de clases de diseño del Documento 3 §5 desde
`clases-codigo.json` (que a su vez sale del código real del backend).

    python3 material-de-trabajo/extraer-clases-codigo.py
    python3 material-de-trabajo/generar-clases-diseno.py

Sale:
  diagramas/lucidchart/SPLG-clases-dominio.mmd      las 39 entidades, por contexto
  diagramas/lucidchart/clases/SPLG-clases-<modulo>.mmd   un archivo por módulo del backend
  material-de-trabajo/indice-clases-servicios.md    el índice con el recuento de cada uno,
                                                     para pegar en 3-Diseño.md §5.2

No se edita ningún `.mmd` a mano: si el código cambia, se corren los dos scripts de
nuevo y se vuelve a pegar el resultado en el Documento 3 (los `.md` son la fuente).
"""
import json, os, re, sys, collections

D = os.path.dirname(os.path.abspath(__file__)) + "/../"
MANIFIESTO = D + "material-de-trabajo/clases-codigo.json"
if not os.path.exists(MANIFIESTO):
    sys.exit("Falta clases-codigo.json: corré primero extraer-clases-codigo.py")
m = json.load(open(MANIFIESTO, encoding="utf-8"))

# ---------------------------------------------------------- 1. clases de dominio
CONTEXTOS = [
  ("Organización y acceso", ["Distributor", "Role", "User", "Admin", "ModuleConfig", "AuditLog"]),
  ("Clientes", ["Customer", "UserAddress", "RepurchaseInvitation"]),
  ("Catálogo e inventario de envases", ["GasCylinder", "GasCylinderPromotion", "Cylinder", "CylinderMovement",
                                        "CylinderInspection", "CylinderRecoveryCase", "CylinderRecoveryNotice"]),
  ("Venta y pedidos", ["Cart", "CartItem", "Order", "OrderItem", "OrderStatusHistory",
                       "OrderAddressChange", "CoverageZone", "TimeSlot"]),
  ("Pagos", ["Payment"]),
  ("Despacho y logística", ["DispatchOffer", "RouteBatch", "RouteBatchStop", "RouteBatchOffer"]),
  ("Flota y choferes", ["Delivery", "Car", "VehicleAssignment", "MaintenancePlan", "MaintenanceTask",
                        "MaintenanceTaskAttachment", "MaintenanceWindowProposal", "VehicleUsageLog"]),
  ("Posventa", ["Claim", "Incident", "Rating"]),
]
_todas = {c for _, cs in CONTEXTOS for c in cs}
_ents = {c for c, v in m.items() if v["kind"] == "entity"}
_sin = sorted(_ents - _todas); _sobra = sorted(_todas - _ents)
if _sin or _sobra:
    sys.exit(f"CONTEXTOS de diseño: entidades sin contexto {_sin} · inexistentes {_sobra}")

def tipo_mmd(t):
    t = re.sub(r'\s*\|\s*null', '', t).strip()
    t = {"string": "string", "number": "number", "boolean": "boolean",
        "Date": "Date"}.get(t, t)
    # Mermaid classDiagram no acepta llaves ni comillas en el tipo de un
    # atributo (los objetos/arrays de objetos, como el JSON de un pedido
    # sugerido). Se deja el tipo TS tal cual en el nombre, sin el detalle.
    if re.search(r'[{}"\']', t):
        return "Json"
    if t.startswith("Array<"):
        return re.sub(r'^Array<(.+)>$', r'\1[]', t)
    return re.sub(r'[<>]', lambda mm: {"<": "~", ">": "~"}[mm.group()], t)

def es_lista(destino_tipo):
    return destino_tipo in ("OneToMany", "ManyToMany")

# pares (padre, hijo) cubiertos por una relacion OneToMany/ManyToMany: la
# ManyToOne inversa en el hijo NO se vuelve a dibujar.
cubiertas = set()
for c, v in m.items():
    if v["kind"] != "entity": continue
    for r in v["relaciones"]:
        if es_lista(r["tipo"]):
            cubiertas.add((c, r["destino"]))

def cuerpo_entidad(clase):
    v = m[clase]
    ids_con_relacion = {r["campo"] + "Id" for r in v["relaciones"]}
    ln = [f"    class {clase} {{"]
    for a in v["atributos"]:
        nombre = a["nombre"]
        if nombre in ids_con_relacion or nombre == "id":
            continue
        marca = "/" if False else "+"
        ln.append(f"        {marca}{nombre}: {tipo_mmd(a['tipo'])}" + ("?" if a["nulo"] else ""))
    ln.append("    }")
    return "\n".join(ln)

def relaciones_entidad(clase):
    v = m[clase]
    out = []
    for r in v["relaciones"]:
        destino = r["destino"]
        if destino not in m or m[destino]["kind"] != "entity":
            continue
        if es_lista(r["tipo"]):
            out.append(f'    {clase} "1" *-- "0..*" {destino} : {r["campo"]}')
        else:
            if (destino, clase) in cubiertas:
                continue   # ya se dibuja como composicion desde el padre
            multB = "0..1" if r["nulo"] else "1"
            out.append(f'    {clase} "0..*" --> "{multB}" {destino} : {r["campo"]}')
    return out

SAL_LUCID = D + "diagramas/lucidchart/"
dom = ["classDiagram", "    direction TB", "",
       "    %% Generado por material-de-trabajo/generar-clases-diseno.py desde el código",
       "    %% real del backend (40 entidades de TypeORM). No se edita a mano.", ""]
todas_rel = []
for ctx, clases in CONTEXTOS:
    dom.append(f'    namespace {re.sub(r"[^A-Za-z]", "", ctx)} {{')
    for c in clases:
        dom.append(cuerpo_entidad(c))
    dom.append("    }")
    dom.append("")
for ctx, clases in CONTEXTOS:
    for c in clases:
        todas_rel += relaciones_entidad(c)
dom += todas_rel
open(SAL_LUCID + "SPLG-clases-dominio.mmd", "w", encoding="utf-8").write("\n".join(dom) + "\n")
print(f"  ✓ SPLG-clases-dominio.mmd  ({len(_ents)} entidades, {len(todas_rel)} relaciones)")

# ------------------------------------------------------ 2. clases de servicios
def sin_llaves(texto):
    """Mermaid no admite llaves ni punto y coma dentro del renglón de un método:
    los tipos literales de TypeScript (`{ lat: number; lng: number }`) y las
    desestructuraciones (`@Param() { term }`) cortaban el diagrama. Se muestran
    con corchetes y comas, que Mermaid sí acepta y que se leen igual."""
    return texto.replace("{", "[").replace("}", "]").replace(";", ",")

def firma(met):
    vis = met["visibilidad"]
    ret = met["retorno"] or ("void" if not met["abstracto"] else "void")
    ret = re.sub(r'\s+', ' ', ret)
    params = met["parametros"]
    return sin_llaves(f"{vis}{met['nombre']}({params}) {ret}")

ESTEREOTIPO_CLASE = {"port": "interface", "usecase": "usecase", "gateway": "gateway",
                     "controller": "controller", "guard": "guard", "interceptor": "interceptor",
                     "listener": "listener", "mapper": "mapper"}

def cuerpo_servicio(clase, v):
    ln = [f"    class {clase} {{"]
    est = v.get("estereotipo") or ESTEREOTIPO_CLASE.get(v["kind"])
    if est:
        ln.append(f"        <<{est}>>")
    for met in v["metodos"]:
        ln.append("        " + firma(met))
    ln.append("    }")
    return "\n".join(ln)

por_modulo = collections.defaultdict(list)
for c, v in m.items():
    if v["kind"] == "entity": continue
    modulo = v["file"].split("/")[0]
    por_modulo[modulo].append(c)

os.makedirs(SAL_LUCID + "clases/", exist_ok=True)
indice = ["| Módulo | Clases | Archivo |", "|---|---:|---|"]
for modulo in sorted(por_modulo):
    clases = sorted(por_modulo[modulo])
    cuerpo = ["classDiagram", "    direction LR", "",
             f"    %% Módulo `{modulo}` — generado por generar-clases-diseno.py", ""]
    for c in clases:
        cuerpo.append(cuerpo_servicio(c, m[c]))
        cuerpo.append("")
    # dependencias (del constructor) y realizacion de puertos, solo dentro del modulo
    # y hacia clases que existen en el manifiesto (si el puerto vive en otro modulo,
    # se anota aparte, no se dibuja la flecha para no mezclar diagramas).
    deps_cross = []
    for c in clases:
        for dep in m[c].get("dependencias", []):
            if dep == c: continue
            if dep in clases:
                cuerpo.append(f"    {c} ..> {dep} : usa")
            elif dep in m:
                deps_cross.append((c, dep, m[dep]["file"].split("/")[0]))
    if deps_cross:
        cuerpo.append("")
        cuerpo.append("    %% Dependencias hacia otros módulos (no se dibujan la flecha para no mezclar):")
        for c, dep, mod2 in sorted(set(deps_cross)):
            cuerpo.append(f"    %% {c} usa {dep} (módulo `{mod2}`)")
    archivo = f"SPLG-clases-{modulo}.mmd"
    open(SAL_LUCID + "clases/" + archivo, "w", encoding="utf-8").write("\n".join(cuerpo) + "\n")
    indice.append(f"| `{modulo}` | {len(clases)} | `diagramas/lucidchart/clases/{archivo}` |")

open(D + "material-de-trabajo/indice-clases-servicios.md", "w", encoding="utf-8").write("\n".join(indice) + "\n")
print(f"  ✓ {len(por_modulo)} archivos en diagramas/lucidchart/clases/ ({sum(len(v) for v in por_modulo.values())} clases)")
