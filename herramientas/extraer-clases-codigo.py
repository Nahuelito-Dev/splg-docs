#!/usr/bin/env python3
"""Extrae, del código del backend, las clases que necesita el diagrama de clases de
diseño del Documento 3: entidades de TypeORM (atributos y relaciones), servicios,
casos de uso, gateways y puertos con sus operaciones públicas y privadas.

    python3 herramientas/extraer-clases-codigo.py

Escribe `catedra/material-de-trabajo/clases-codigo.json`. Es la fuente única que usan
`generar-clases-dominio.py`, `generar-clases-servicios.py` y
`cruzar-dsd-clases.py`: todos leen el código una sola vez y comparten el resultado,
así que no hay manera de que el diagrama de clases diga algo que el código no dice.

No se editan `.ts` ni se ejecuta nada del backend: solo se lee texto con expresiones
regulares. Es aproximado (no es un parser de TypeScript), pero suficiente para lo
que hace falta: nombre de la clase, sus atributos/relaciones y la firma de cada
método.
"""
import re, os, json, glob, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
BACK = os.path.abspath(D + "../splg-app-backend") + "/src/"
if not os.path.isdir(BACK):
    sys.exit(f"No se encuentra el backend en {BACK}")

manifest = {}

# --------------------------------------------------------------- utilidades
def hallar_cierre(s, i):
    """Dado s[i] == '(', devuelve el indice del ')' que cierra, respetando
    parentesis anidados, generics <...> y strings."""
    profundidad = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == '(':
            profundidad += 1
        elif c == ')':
            profundidad -= 1
            if profundidad == 0:
                return j
        j += 1
    return len(s) - 1

def firma_metodo(src, nombre_inicio, paren_inicio):
    """Dado donde empieza el nombre del metodo y la posicion del '(' que le
    sigue, devuelve (parametros_en_una_linea, tipo_de_retorno_o_None)."""
    cierre = hallar_cierre(src, paren_inicio)
    params = src[paren_inicio + 1:cierre]
    params = re.sub(r'\s+', ' ', params).strip()
    params = re.sub(r',\s*$', '', params)
    resto = src[cierre + 1:cierre + 200]
    m = re.match(r'\s*:\s*([^{;=]+?)\s*[{;=]', resto)
    ret = m.group(1).strip() if m else None
    return params, ret

MODIFICADORES = ('public', 'private', 'protected', 'static', 'async', 'abstract',
                 'readonly', 'override', 'get', 'set')

def extraer_metodos(cuerpo_clase, offset_es_interfaz=False):
    """Recorre el cuerpo de una clase/interfaz (ya balanceado) y devuelve la
    lista de metodos: nombre, parametros, retorno y visibilidad (+/-)."""
    metodos = []
    # Constructor: se ignora como metodo, pero sus parametros con
    # `private readonly nombre: Tipo` declaran dependencias (se usan aparte).
    for m in re.finditer(r'^\s{2}((?:public |private |protected |static |async |'
                        r'abstract |readonly |override )*)'
                        r'(\w+)\s*(<[^>]*>)?\s*\(', cuerpo_clase, re.M):
        mods, nombre = m.group(1), m.group(2)
        if nombre == 'constructor':
            continue
        if nombre in ('if', 'for', 'while', 'switch', 'catch'):
            continue
        paren_inicio = m.end() - 1
        params, ret = firma_metodo(cuerpo_clase, m.start(2), paren_inicio)
        vis = '-' if 'private' in mods else ('#' if 'protected' in mods else '+')
        if any(x in metodos and 0 for x in ()):  # no-op, deja el bloque legible
            pass
        metodos.append({"nombre": nombre, "parametros": params, "retorno": ret,
                        "visibilidad": vis, "estatico": 'static' in mods,
                        "abstracto": 'abstract' in mods})
    return metodos

def dependencias_constructor(cuerpo_clase):
    """Tipos que recibe el constructor (para las dependencias del diagrama)."""
    m = re.search(r'constructor\s*\(', cuerpo_clase)
    if not m: return []
    cierre = hallar_cierre(cuerpo_clase, m.end() - 1)
    params = cuerpo_clase[m.end():cierre]
    deps = []
    for pm in re.finditer(r':\s*([A-Z]\w+)(?:<[^>]*>)?(?:\s*\|\s*null)?', params):
        deps.append(pm.group(1))
    return deps

def bloque_clase(src, ini_llave):
    """Dado el indice de la '{' que abre la clase, devuelve el cuerpo balanceado."""
    prof, j = 0, ini_llave
    while j < len(src):
        if src[j] == '{': prof += 1
        elif src[j] == '}':
            prof -= 1
            if prof == 0: return src[ini_llave + 1:j]
        j += 1
    return src[ini_llave + 1:]

# ---------------------------------------------------------- 1. entidades
TIPO_TS = {"string": "string", "number": "number", "boolean": "boolean",
          "Date": "Date"}

for ruta in sorted(glob.glob(BACK + "**/*.entity.ts", recursive=True)):
    src = open(ruta, encoding="utf-8").read()
    me = re.search(r"@Entity\(\s*['\"]([a-zA-Z_]+)['\"]", src)
    if not me: continue
    tabla = me.group(1)
    mc = re.search(r'export\s+class\s+(\w+)[^{]*\{', src)
    if not mc: continue
    nombre_clase, ini = mc.group(1), mc.end() - 1
    cuerpo = bloque_clase(src, ini)
    rel_ini_clase = mc.end()

    atributos, relaciones = [], []
    props = list(re.finditer(r'^ {2}(\w+)[!?]?\s*:\s*([^;=]+);', cuerpo, re.M))
    for pm in props:
        nombre, tipo = pm.group(1), pm.group(2).strip()
        segmento = cuerpo[max(0, pm.start() - 400):pm.start()]
        seg_decoradores = segmento[segmento.rfind('\n\n') + 1:] if '\n\n' in segmento else segmento
        es_relacion = re.search(r'@(ManyToOne|OneToMany|OneToOne|ManyToMany)\(\s*\(\)\s*=>\s*(\w+)',
                                 seg_decoradores[-300:])
        if es_relacion:
            kind, target = es_relacion.group(1), es_relacion.group(2)
            nullable = 'nullable: true' in seg_decoradores[-300:] or '| null' in tipo
            relaciones.append({"campo": nombre, "destino": target, "tipo": kind,
                               "nulo": nullable})
            continue
        if nombre[0].isupper():
            continue
        tipo_simple = re.sub(r'\s*\|\s*null', '', tipo).strip()
        atributos.append({"nombre": nombre, "tipo": tipo_simple,
                          "nulo": '| null' in tipo})
    manifest[nombre_clase] = {"kind": "entity", "file": os.path.relpath(ruta, BACK),
                              "tabla": tabla, "atributos": atributos,
                              "relaciones": relaciones}

# --------------------------------------------- 2. servicios, casos de uso, etc
PATRONES_CLASE = [
    (r'export\s+class\s+(\w+)[^{]*\{', 'service'),
]

def clasificar(ruta):
    if '.entity.ts' in ruta: return None
    if re.search(r'\.(spec|module|dto|enum)\.ts$', ruta): return None
    if '/dto/' in ruta or '/entities/' in ruta: return None
    if '.port.ts' in ruta: return 'port'
    if '.gateway.ts' in ruta: return 'gateway'
    if '.use-case.ts' in ruta: return 'usecase'
    if '.controller.ts' in ruta: return 'controller'
    if '.guard.ts' in ruta: return 'guard'
    if '.interceptor.ts' in ruta: return 'interceptor'
    if '.listener.ts' in ruta or '.subscriber.ts' in ruta: return 'listener'
    if '.mapper.ts' in ruta: return 'mapper'
    if '.provider.ts' in ruta: return 'service'
    if '.health.ts' in ruta: return 'service'
    if ('.service.ts' in ruta or '.repository.ts' in ruta or '.adapter.ts' in ruta
            or '.strategy.ts' in ruta or '.machine.ts' in ruta): return 'service'
    return None

for ruta in sorted(glob.glob(BACK + "**/*.ts", recursive=True)):
    kind = clasificar(ruta)
    if not kind: continue
    src = open(ruta, encoding="utf-8").read()
    for mc in re.finditer(r'export\s+(?:abstract\s+)?class\s+(\w+)(?:\s+(?:extends|implements)\s+[\w<>, ]+)?\s*\{', src):
        nombre_clase = mc.group(1)
        ini = mc.end() - 1
        cuerpo = bloque_clase(src, ini)
        metodos = extraer_metodos(cuerpo)
        deps = dependencias_constructor(cuerpo)
        estereotipo = {"port": "interface", "usecase": "usecase", "gateway": "gateway",
                      "controller": "controller", "guard": "guard",
                      "interceptor": "interceptor", "listener": "listener",
                      "mapper": "mapper"}.get(kind)
        manifest.setdefault(nombre_clase, {"kind": kind, "file": os.path.relpath(ruta, BACK),
                                           "metodos": [], "dependencias": [],
                                           "estereotipo": estereotipo})
        manifest[nombre_clase]["metodos"] = metodos
        manifest[nombre_clase]["dependencias"] = deps
    # las interfaces (los puertos que no son clase abstracta) tambien cuentan
    for mi in re.finditer(r'export\s+(?:abstract\s+class|interface)\s+(\w+)\s*\{', src):
        pass  # ya cubierto por el patron de arriba para 'abstract class'; las
              # interfaces puras (no abstract class) se agregan aparte:
    for mi in re.finditer(r'export\s+interface\s+(\w+)\s*\{', src):
        nombre_clase = mi.group(1)
        if nombre_clase in manifest: continue
        ini = mi.end() - 1
        cuerpo = bloque_clase(src, ini)
        metodos = []
        for m in re.finditer(r'^\s{2}(\w+)\s*\(', cuerpo, re.M):
            paren_inicio = m.end() - 1
            params, ret = firma_metodo(cuerpo, m.start(1), paren_inicio)
            metodos.append({"nombre": m.group(1), "parametros": params, "retorno": ret,
                            "visibilidad": "+", "estatico": False, "abstracto": True})
        if metodos:
            manifest[nombre_clase] = {"kind": kind, "file": os.path.relpath(ruta, BACK),
                                      "metodos": metodos, "dependencias": [],
                                      "estereotipo": "interface"}

out = D + "catedra/material-de-trabajo/clases-codigo.json"
json.dump(manifest, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import collections as _c
por_kind = _c.Counter(v["kind"] for v in manifest.values())
print(f"clases-codigo.json: {len(manifest)} clases —", ", ".join(f"{k}: {n}" for k, n in sorted(por_kind.items())))
