#!/usr/bin/env python3
"""Verifica que los casos de uso de alto nivel (descripción) y los expandidos estén en lenguaje de negocio.

    python3 material-de-trabajo/verificar-lenguaje-esencial.py

Un caso de uso esencial dice qué hace el actor y qué responde el sistema, sin tecnología: no lleva rutas, métodos
HTTP, códigos de estado, nombres de clases, funciones o variables, ni enumeraciones en mayúsculas, ni
infraestructura (Redis, Firebase, caché, tokens, webhooks…). Los mensajes literales que ve el usuario van entre
«comillas angulares»: se controla que lo citado no lleve identificadores de código (camelCase, snake_case, rutas, constantes). Lo técnico de cada caso está en la «Tabla de implementación por caso de
uso» del Documento 3 (§4.25) y de Casos-de-Uso.md (§8).

Se controla la descripción de cada CUA (Documento 0 §7 y Casos-de-Uso.md §4) y todo el CUE, con su campo Estado
(Documento 1 §7 y Casos-de-Uso.md §5). Sale 0 si no hay ninguna palabra técnica, 1 y el detalle si hay alguna.
"""
import os, re, sys

D = os.path.dirname(os.path.abspath(__file__)) + "/../"


def leer(f):
    return open(D + f, encoding="utf-8").read()


def seccion(t, ini, fin):
    a = re.search(ini, t, re.M).start()
    m = re.search(fin, t[a + 1:], re.M) if fin else None
    return t[a: a + 1 + m.start() if m else len(t)]


SIGLAS = {"CUIT", "CUIL", "SPLG", "WEBP", "JPG", "PNG", "PDF", "GPS", "DNI", "CBU", "IVA", "AFIP", "SMS", "GLP", "ART",
          "ACT", "IRQ", "NFR", "OBJ", "UML", "QR", "MB", "AAAA"}
PROHIBIDO = [
    ("backtick", re.compile(r"`")),
    ("método HTTP", re.compile(r"\b(?:GET|POST|PUT|PATCH|DELETE)\b")),
    ("ruta", re.compile(r"(?<![\w»])/[a-z][\w:-]*(?:/[\w:{}-]+)*")),
    ("código de estado", re.compile(r"\b(?:400|401|403|404|405|409|410|413|415|422|429)\b|\b(?:error|código|status|HTTP)\s+(?:HTTP\s+)?[1-5]\d\d\b")),
    ("enumeración o constante", re.compile(r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b")),
    ("identificador camelCase", re.compile(r"\b[a-z]+[A-Z][A-Za-z]*\b")),
    ("identificador snake_case", re.compile(r"\b[a-z]+_[a-z_]+\b")),
    ("tecnología o infraestructura", re.compile(
        r"\b(?:Redis|Firebase|caché|cache|JWT|token|tokens|webhook|webhooks|endpoint|UUID|JSON|SQL|HTTPS?|REST|WebSocket|Socket\.IO|"
        r"S3|MinIO|Docker|TypeORM|NestJS|Nest|Postgres|PostgreSQL|PostGIS|Flutter|React|Stripe|API|interceptor|guard|"
        r"cron|idempotencia|idempotente|Idempotency|header|encabezado|decimal\.js|numeric|SELECT|INSERT|UPDATE|FOR UPDATE|"
        r"transacci[oó]n|transaccional|bloqueo (?:de fila|distribuido|pesimista|se libera)|se libera igual|"
        r"bloquea(?:n)? (?:la|las|el|los) (?:carga|garrafas?|fila|dep[oó]sito|franja|pedido|veh[ií]culo)|"
        r"se deshace(?:n)? (?:el cambio|la baja)|deshace todo|rollback|bucket|docs/\w+\.md|"
        r"lock|disparador|migraci[oó]n|columna|payload|DTO|enum)\b", re.I)),
    ("mayúsculas técnicas", None),
]


IDENT_CITADO = [("identificador camelCase", re.compile(r"\b[a-z]+[A-Z][A-Za-z]*\b")),
                ("identificador snake_case", re.compile(r"\b[a-z]+_[a-z_]+\b")),
                ("enumeración o constante", re.compile(r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b")),
                ("ruta", re.compile(r"(?<![\w»])/[a-z][\w:-]*(?:/[\w:{}-]+)*")),
                ("backtick", re.compile(r"`"))]


def limpiar(texto):
    """Quita los mensajes literales («…»), los códigos de documentación y las rutas internas de las tablas."""
    t = re.sub(r"«[^»]*»", " ", texto)
    t = re.sub(r"\b(?:CU|SS|ACT|IRQ|NFR|OBJ|PE|I)-\d+(?:\.\d+)?\b", " ", t)
    t = re.sub(r"\b[A-Z]{3,}-\d+\b", " ", t)
    return t


# Términos que no se admiten ni siquiera dentro de un mensaje citado entre «»: describen el mecanismo, no lo que ve el actor.
EN_CITADOS = re.compile(
    r"\b(?:header|X-Distributor|slug|UUID|HTTP|endpoint|bloqueándol\w*|antes de escribir|transacci[oó]n|"
    r"carácter nulo|byte nulo|Idempotency-Key)\b", re.I)


def revisar(nombre, texto, hallazgos):
    for m in EN_CITADOS.finditer(texto):
        hallazgos.append((nombre, "mecanismo técnico (también dentro de «»)", m.group(0)))
    for cita in re.findall(r"«([^»]*)»", texto):
        for etiqueta, rx in IDENT_CITADO:
            for m in rx.finditer(cita):
                hallazgos.append((nombre, etiqueta + " dentro de «»", m.group(0)))
    t = limpiar(texto)
    for etiqueta, rx in PROHIBIDO:
        if rx is None:
            for m in re.finditer(r"\b[A-Z]{4,}\b", t):
                if m.group(0) not in SIGLAS:
                    hallazgos.append((nombre, "mayúsculas técnicas", m.group(0)))
            continue
        for m in rx.finditer(t):
            hallazgos.append((nombre, etiqueta, m.group(0)))


def cua(t):
    out = {}
    for m in re.finditer(r"\*\*Código:\*\* (CU-\d+) \|[^\n]*\n\*\*Actor/es:\*\* ([^\n]*)\n\*\*Subsistema:\*\*[^\n]*\n\*\*Calificación:\*\*[^\n]*\n"
                         r"\*\*Descripción:\*\* (.*?)(?=\n\s*\n---|\n\*\*Código|\Z)", t, re.S):
        out[m.group(1)] = m.group(3)   # el nombre de los actores (incluido el proveedor de identidad) no se controla
    return out


def cue(t):
    out = {}
    for m in re.finditer(r"^#### [^\n]*?(CU-\d+) — [^\n]*\n(.*?)(?=^#{1,4} |\Z)", t, re.M | re.S):
        cuerpo = m.group(2)
        out[m.group(1)] = cuerpo
    return out


cas, plan, req = leer("Casos-de-Uso.md"), leer("0-Plan_Del_Proyecto.md"), leer("1-Requisitos.md")
fuentes = [
    ("Documento 0 §7 (CUA)", cua(seccion(plan, r"^## 7\. ", r"^## 8\. "))),
    ("Casos-de-Uso.md §4 (CUA)", cua(seccion(cas, r"^## 4\. ", r"^## 5\. "))),
    ("Documento 1 §7 (CUE)", cue(seccion(req, r"^## 7\. ", r"^## 8\. "))),
    ("Casos-de-Uso.md §5 (CUE)", cue(seccion(cas, r"^## 5\. ", r"^## 6\. "))),
]
hallazgos = []
total = 0
for etiqueta, casos in fuentes:
    if not casos:
        print(f"[FALLA] no pude leer ningún caso de {etiqueta}: no se da OK sobre una lectura vacía")
        sys.exit(1)
    for cu, texto in casos.items():
        total += 1
        revisar(f"{etiqueta} · {cu}", texto, hallazgos)

print(f"Textos revisados: {total} (CUA y CUE de los documentos 0 y 1 y de Casos-de-Uso.md)")
if hallazgos:
    print(f"\n{len(hallazgos)} palabra(s) técnica(s) en un caso de uso esencial:")
    por_caso = {}
    for n, e, p in hallazgos:
        por_caso.setdefault(n.split(" · ")[1], []).append((e, p))
    for cu, lst in sorted(por_caso.items())[:40]:
        print(f"  - {cu}: " + "; ".join(sorted({f'{e} «{p}»' for e, p in lst}))[:230])
    sys.exit(1)
print("Ningún caso de uso esencial nombra rutas, códigos, clases ni infraestructura.")
sys.exit(0)
