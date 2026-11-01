"""Los DSS y DSD de los documentos se muestran como imagen (PNG del repositorio) y su código Mermaid queda
debajo, plegado. Este módulo es la única que conoce esa forma:

    plegar(texto)     pone la imagen sobre cada bloque ```mermaid cuyo título es el de un `diagramas/{DSS,DSD,ER,MOD}_*.mmd`
                      y lo mete en un <details>; si el bloque ya tenía su pie «**Figura N — …**» debajo, el pie
                      sube y queda entre la imagen y el código
    desplegar(texto) deshace lo anterior; es lo que leen los generadores (sitio, Word, HTML para Drive) y
                      `numerar-figuras.py`, así ven cada diagrama una sola vez, como siempre
    verificar()       los errores del gate: todo CU con su DSS y su DSD como imagen, toda imagen existe y todo PNG
                      es el de su .mmd vigente

`plegar(desplegar(t)) == plegar(t)`: se puede correr las veces que se quiera. Los `.mmd` siguen siendo la fuente.
"""
import glob, hashlib, json, os, re

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
import sys
sys.path.insert(0, D + "herramientas")
from cu_esenciales import CON_DSS, ARCHIVOS_DSD
DOCS_CU = ("Casos-de-Uso.md", "2-Analisis.md", "3-Diseño.md")
DOCS_TODOS = ("0-Plan_Del_Proyecto.md", "0.1-Planificacion_Iteraciones.md", "1-Requisitos.md", "2-Analisis.md",
              "3-Diseño.md", "Casos-de-Uso.md")
PREFIJOS = "DSS DSD ER MOD".split()     # DSS/DSD por caso de uso, ER = modelo de datos por contexto, MOD = diagrama de módulo
MANIFIESTO = D + "diagramas/fuentes-png.json"
RESUMEN = "Ver código del diagrama"

_TITULO = re.compile(r'^\s*title (.+)$', re.M)
_BLOQUE = r'```mermaid\n(.*?)\n```'
_PIE = r'\*\*Figura \d+(?:\.\d+)? — [^\n]*\*\*'
_PLEGADO = re.compile(
    r'!\[(?P<alt>[^\]]*)\]\(\.\./diagramas/png/(?P<stem>(?:DSS|DSD|ER|MOD)_[^)\s]+)\.png\)\n\n'
    r'(?:(?P<pie>' + _PIE + r')\n\n)?'
    r'<details><summary>' + RESUMEN + r'</summary>\n\n(?P<codigo>' + _BLOQUE.replace('(.*?)', '.*?') + r')\n\n</details>',
    re.S)
_SUELTO = re.compile(_BLOQUE + r'(?:\n\n(?P<pie>' + _PIE + r')(?=\n|$))?', re.S)


def sha(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def mmds():
    return sorted(p for pre in PREFIJOS for p in glob.glob(D + f"diagramas/{pre}_*.mmd"))


def fuentes():
    """clave del diagrama -> nombre base del .mmd (y del .png). La clave es el `title` (DSS y DSD) o, si el
    diagrama no lo tiene (ER y MOD), su propio código."""
    o = {}
    for f in mmds():
        t = open(f, encoding="utf-8").read()
        m = _TITULO.search(t)
        o[m.group(1).strip() if m else t.strip("\n")] = os.path.basename(f)[:-4]
    return o


def clave(cuerpo):
    t = _TITULO.search(cuerpo)
    return t.group(1).strip() if t else cuerpo.strip("\n")


def desplegar(texto):
    def vuelve(m):
        pie = m.group("pie")
        return m.group("codigo") + ("\n\n" + pie if pie else "")
    return _PLEGADO.sub(vuelve, texto)


def _alt(texto):
    return re.sub(r'\s+', ' ', texto.replace("[", "(").replace("]", ")")).strip()


def plegar(texto):
    por_titulo = fuentes()
    texto = desplegar(texto)

    def pliega(m):
        t = _TITULO.search(m.group(1))
        stem = por_titulo.get(clave(m.group(1)))
        if not stem or not os.path.exists(D + f"diagramas/png/{stem}.png"):
            return m.group(0)
        pie = m.group("pie")
        alt = _alt(re.sub(r'^\*\*Figura \d+(?:\.\d+)? — |\*\*$', '', pie)) if pie else _alt(t.group(1) if t else stem)
        bloque = "```mermaid\n" + m.group(1) + "\n```"
        return (f"![{alt}](../diagramas/png/{stem}.png)\n\n" + (pie + "\n\n" if pie else "")
                + f"<details><summary>{RESUMEN}</summary>\n\n{bloque}\n\n</details>")
    return _SUELTO.sub(pliega, texto)


def _leer(nombre):
    return open(DOC + nombre, encoding="utf-8").read()


def _nombres_de_stem(cu):
    mmd = [os.path.basename(p)[:-4] for p in glob.glob(D + "diagramas/DS[SD]_*.mmd")]
    dss = sorted(s for s in mmd if s.startswith(f"DSS_{cu}_"))
    dsd = sorted(s for s in mmd if s.startswith("DSD_") and re.search(r'(?<![\d-])%s(?![\d])' % cu, s))
    return dss, dsd


def estilo_actual():
    import sys
    sys.path.insert(0, D + "herramientas")
    from estilo_vp import MERMAID
    return sha(json.dumps(MERMAID, sort_keys=True))


def registrar(stems):
    """Anota con qué fuente y qué estilo se dibujó cada PNG (lo llama renderizar-dsd.py)."""
    m = json.load(open(MANIFIESTO, encoding="utf-8")) if os.path.exists(MANIFIESTO) else {"estilo": "", "png": {}}
    m["estilo"] = estilo_actual()
    for s in stems:
        m["png"][s] = sha(open(D + f"diagramas/{s}.mmd", encoding="utf-8").read())
    m["png"] = dict(sorted(m["png"].items()))
    json.dump(m, open(MANIFIESTO, "w", encoding="utf-8"), indent=0, ensure_ascii=False)
    open(MANIFIESTO, "a").write("\n")


def verificar():
    """Errores del gate; lista vacía si todo está en orden."""
    err = []
    cat = _leer("Casos-de-Uso.md")
    casos = sorted(set(m.group(1) for m in re.finditer(r'^\| (CU-\d{3}) [^|]+ \| SS-\d\d \|', cat, re.M)))
    docs = {d: _leer(d) for d in DOCS_CU}
    imgs = {d: set(re.findall(r'!\[[^\]]*\]\(\.\./diagramas/png/(DS[SD]_[^)\s]+)\.png\)', t)) for d, t in docs.items()}
    # cada CU con su DSS y su DSD como imagen, en Casos-de-Uso.md y en el documento que le toca
    for cu in casos:
        dss, dsd = _nombres_de_stem(cu)
        if not dss: err.append(f"{cu}: no hay .mmd del DSS")
        if not dsd: err.append(f"{cu}: no hay .mmd del DSD")
        for s in dss:
            for d in ("Casos-de-Uso.md", "2-Analisis.md"):
                if d == "2-Analisis.md" and cu not in CON_DSS: continue    # el Documento 2 sólo lleva los DSS de los casos con interacción del actor
                if s not in imgs[d]: err.append(f"{cu}: {d} no muestra la imagen de {s}")
        for s in dsd:
            for d in ("Casos-de-Uso.md", "3-Diseño.md"):
                if d == "3-Diseño.md" and s + ".mmd" not in ARCHIVOS_DSD: continue    # el Documento 3 sólo lleva los DSD de los casos dinámicos
                if s not in imgs[d]: err.append(f"{cu}: {d} no muestra la imagen de {s}")
    # ningún bloque Mermaid de los documentos queda sin su imagen, ésta existe y encabeza el código de su propio .mmd
    por_clave = fuentes()
    todos = {d: _leer(d) for d in DOCS_TODOS}
    for d, t in todos.items():
        for s in set(re.findall(r'!\[[^\]]*\]\(\.\./diagramas/png/((?:DSS|DSD|ER|MOD)_[^)\s]+)\.png\)', t)):
            if not os.path.exists(D + f"diagramas/png/{s}.png"):
                err.append(f"{d}: la imagen diagramas/png/{s}.png no existe")
        sueltos = len(_SUELTO.findall(desplegar(t)))
        plegados = len(_PLEGADO.findall(t))
        if sueltos != plegados:
            err.append(f"{d}: {sueltos - plegados} bloques Mermaid sin imagen (con .mmd en diagramas/ y PNG: incrustar-imagenes-cu.py --aplicar; "
                       "los de ER y MOD salen de herramientas/extraer-mmd-modelos.py)")
        for m in _PLEGADO.finditer(t):
            if por_clave.get(clave(re.sub(r'^```mermaid\n|\n```$', '', m.group("codigo")))) != m.group("stem"):
                err.append(f"{d}: la imagen {m.group('stem')} está sobre el código de otro diagrama")
    # cada PNG es el de su .mmd vigente
    man = json.load(open(MANIFIESTO, encoding="utf-8")) if os.path.exists(MANIFIESTO) else {"estilo": "", "png": {}}
    if man["estilo"] != estilo_actual():
        err.append("el estilo de los diagramas (estilo_vp.py) cambió desde que se dibujaron los PNG: volver a dibujarlos")
    for p in mmds():
        s = os.path.basename(p)[:-4]
        if man["png"].get(s) != sha(open(D + f"diagramas/{s}.mmd", encoding="utf-8").read()):
            err.append(f"diagramas/png/{s}.png no es el de su .mmd vigente: python3 herramientas/renderizar-dsd.py diagramas/{s}.mmd")
        if not os.path.exists(D + f"diagramas/svg/{s}.svg"):
            err.append(f"diagramas/svg/{s}.svg no existe")
    return err
