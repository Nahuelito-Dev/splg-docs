#!/usr/bin/env python3
"""Genera los cinco documentos de la cátedra en Word (.docx) a partir de los .md.

    python3 generar-docx-catedra.py            # los cinco
    python3 generar-docx-catedra.py 2 3        # sólo algunos (0, 0.1, 1, 2, 3)

Salida: `entregables/catedra-docx/*.docx`, copiados a `~/Desktop/SPLG-Documentacion-Catedra/`.

Los .md son la fuente y no se tocan. Por documento arma un .md intermedio (portada y
Lista de Cambios al principio, como en la plantilla; cada bloque Mermaid reemplazado por su
PNG, o renderizado con mermaid-cli si no tiene) y lo convierte con pandoc usando un
reference-doc con la página y la tipografía de la plantilla (`.catedra-ref/*.doc`, que se
convierte con `textutil`). Requiere pandoc, textutil (macOS) y mermaid-cli (npx cache).
"""
import glob, hashlib, json, os, re, shutil, struct, subprocess, sys, tempfile, zipfile

D = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, D)
SALIDA = D + "entregables/catedra-docx/"
CACHE = SALIDA + ".cache/"
DESTINO = os.path.expanduser("~/Desktop/SPLG-Documentacion-Catedra/")
AUTOR_ARCHIVO = "Wagner Nahuel"

UNIVERSIDAD = "Universidad Nacional de Misiones"
FACULTAD = "Facultad de Ciencias Exactas, Químicas y Naturales"
CARRERA = "Licenciatura en Sistemas de Información – Analista en Sistemas de Computación"
MATERIA = "Proyecto Software (LSI) | Trabajo Final (ASC)"
AUTOR = "Nahuel Wagner"
FECHA_ISO, FECHA = "2026-10-19", "19/10/2026"
CAMBIO = "Actualización al estado de la Construcción, C-19"

# (clave, md, plantilla, nombre de salida)
DOCS = [
    ("0", "0-Plan_Del_Proyecto.md", "0-Plan_Del_Proyecto.doc", "Plan Del Proyecto"),
    ("0.1", "0.1-Planificacion_Iteraciones.md", "0.1Planificación_Iteración.doc", "Planificacion de Iteraciones"),
    ("1", "1-Requisitos.md", "1-Requisitos.doc", "Requerimientos"),
    ("2", "2-Analisis.md", "2.-Análisis.doc", "Analisis"),
    ("3", "3-Diseño.md", "3.-Diseño.doc", "Diseño"),
]

MAX_ANCHO_CM, MAX_ALTO_CM, DPI, DPI_MAX = 15.2, 21.0, 150, 200
MAX_PX = 1600
# un archivo por documento; SPLG_DOCX_LIMITE_MB fuerza a partirlo si hace falta un tope de peso
LIMITE = float(os.environ.get("SPLG_DOCX_LIMITE_MB", "inf")) * 1e6


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


# ---------- imágenes ----------
def tam_png(ruta):
    with open(ruta, "rb") as f:
        h = f.read(24)
    return struct.unpack(">II", h[16:24])


FONT_PX = 24                   # cuerpo del texto de los diagramas (12 px de mermaid a escala 2)
MIN_PT = 7                     # texto más chico que esto no se lee
PORT_W, PORT_H = 15.2, 21.0    # cm útiles de una página vertical
LAND_W, LAND_H = 25.2, 16.0    # cm útiles de una página horizontal (con lugar para el pie de figura)
DPI_HOR = 200


def pt_texto(w_px, d_cm):
    return FONT_PX * d_cm / w_px / 2.54 * 72


def optimizar(ruta, px, clave):
    """PNG remuestreado a `px` de ancho y cuantizado (paleta); devuelve la ruta de la copia."""
    os.makedirs(CACHE + "redu/", exist_ok=True)
    w = tam_png(ruta)[0]
    destino = CACHE + "redu/" + hashlib.sha1((ruta + clave).encode()).hexdigest()[:14] + "-%d.png" % px
    if not os.path.exists(destino):
        tmp = destino[:-4] + "-t.png"
        if w > px:
            sh(["sips", "--resampleWidth", str(px), ruta, "--out", tmp], stdout=subprocess.DEVNULL)
        else:
            shutil.copy(ruta, tmp)
        # paleta de colores: los diagramas son planos y se achican mucho sin perder nitidez
        subprocess.run(["pngquant", "--quality=30-90", "--speed", "1", "--force", "--output", destino, tmp])
        if not os.path.exists(destino) or os.path.getsize(destino) > os.path.getsize(tmp):
            shutil.copy(tmp, destino)
        os.unlink(tmp)
    return destino


def cortar_png(ruta, alto_px, n):
    """Parte un PNG en `n` franjas horizontales de `alto_px` (la última, lo que sobre)."""
    w, h = tam_png(ruta)
    franjas = []
    for i in range(n):
        y = i * alto_px
        hh = min(alto_px, h - y)
        if y + hh >= h:
            hh -= 1      # sips devuelve la imagen entera si el recorte llega justo al borde inferior
        out = ruta[:-4] + "-h%d-f%d.png" % (alto_px, i)
        if not os.path.exists(out):
            sh(["sips", "--cropToHeightWidth", str(hh), str(w), "--cropOffset", str(y), "0", ruta, "--out", out],
               stdout=subprocess.DEVNULL)
        franjas.append(out)
    return franjas


SECT_V = ('<w:sectPr><w:type w:val="nextPage"/><w:pgSz w:w="12240" w:h="15840"/>'
          '<w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>')
SECT_H = ('<w:sectPr><w:type w:val="nextPage"/><w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/>'
          '<w:pgMar w:top="1000" w:right="720" w:bottom="1000" w:left="720" w:header="500" w:footer="500" w:gutter="0"/></w:sectPr>')


def raw(xml):
    return "\n\n```{=openxml}\n" + xml + "\n```\n\n"


CONTINUA = raw('<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Verdana" w:hAnsi="Verdana"/>'
               '<w:i/><w:sz w:val="18"/></w:rPr><w:t>(continúa)</w:t></w:r></w:p>')
MARCA_INI = raw(f"<w:p><w:pPr>{SECT_V}</w:pPr></w:p>")
MARCA_FIN = raw(f"<w:p><w:pPr>{SECT_H}</w:pPr></w:p>")


def compactar(ruta):
    """Los diagramas con degradés no entran bien en paleta: si el PNG pesa mucho, prueba JPEG calidad 85."""
    if os.path.getsize(ruta) < 250_000:
        return ruta
    jpg = ruta[:-4] + ".jpg"
    if not os.path.exists(jpg):
        sh(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85", ruta, "--out", jpg], stdout=subprocess.DEVNULL)
    return jpg if os.path.getsize(jpg) < 0.7 * os.path.getsize(ruta) else ruta


def img(ruta, ancho, alto):
    ruta = compactar(ruta)
    # el tamaño viaja en el texto alternativo: pandoc lo recorta al ancho de la sección vertical y se corrige después
    return "![SPLGSZ:%.3fx%.3f](%s){width=%.2fcm height=%.2fcm}" % (ancho, alto, ruta, ancho, alto)


def imagen_md(ruta):
    """Markdown de un diagrama. Si en página vertical el texto quedaría menor que MIN_PT, va solo en una
    sección horizontal; si es muy alto, se parte en franjas con «(continúa)»."""
    if ruta.endswith(".svg"):
        os.makedirs(CACHE + "redu/", exist_ok=True)
        png = CACHE + "redu/" + os.path.basename(ruta)[:-4] + ".png"
        sh(["rsvg-convert", "-z", "3", "-b", "white", "-o", png, ruta])
        ruta = png
    w, h = tam_png(ruta)
    # vertical: a ancho de página, o a su tamaño natural si es más chico
    d = min(PORT_W, PORT_H * w / h, w / DPI * 2.54)
    if pt_texto(w, min(PORT_W, w / DPI * 2.54)) >= MIN_PT:
        # el texto se lee a ancho de página: sólo se achica por alto, y si queda chico se parte
        if pt_texto(w, d) >= MIN_PT or h / w * PORT_W <= PORT_H:
            px = min(int(d / 2.54 * DPI_MAX), w)
            return img(optimizar(ruta, px, "v"), d, d * h / w)
        ancho = min(PORT_W, w / DPI * 2.54)
        px = min(int(ancho / 2.54 * DPI_MAX), w)
        base = optimizar(ruta, px, "v")
        wb, hb = tam_png(base)
        franja = int(PORT_H / ancho * wb)
        n = -(-hb // franja)
        return CONTINUA.join(img(f, ancho, ancho * tam_png(f)[1] / wb) for f in cortar_png(base, franja, n))
    # horizontal
    dl = min(LAND_W, LAND_H * w / h)
    if (pt_texto(w, dl) < MIN_PT <= pt_texto(w, LAND_W) or dl < 0.6 * LAND_W) and w > 1100:
        dl = LAND_W
        px = min(int(dl / 2.54 * DPI_HOR), w)
        base = optimizar(ruta, px, "h")
        wb, hb = tam_png(base)
        franja = int(LAND_H / dl * wb)
        n = -(-hb // franja)
        cuerpo = CONTINUA.join(img(f, dl, dl * tam_png(f)[1] / wb) for f in cortar_png(base, franja, n))
    else:
        px = min(int(dl / 2.54 * DPI_HOR), w)
        cuerpo = img(optimizar(ruta, px, "h"), dl, dl * h / w)
    return "\n\n@@INI@@\n\n" + cuerpo + "\n\n@@FIN@@\n\n"


def norm(s):
    return re.sub(r"\s+", "", s)


def mapa_mmd():
    m = {}
    for f in sorted(glob.glob(D + "diagramas/*.mmd")):
        png = D + "diagramas/png/" + os.path.basename(f)[:-4] + ".png"
        if os.path.exists(png):
            m.setdefault(norm(open(f, encoding="utf-8").read()), png)
    return m


def buscar_mmdc():
    if shutil.which("mmdc"):
        return shutil.which("mmdc")
    c = sorted(glob.glob(os.path.expanduser("~/.npm/_npx/*/node_modules/.bin/mmdc")))
    if not c:
        sys.exit("No encuentro mmdc (mermaid-cli)")
    return c[-1]


def buscar_chromium():
    c = sorted(glob.glob(os.path.expanduser(
        "~/Library/Caches/ms-playwright/chromium-*/chrome-mac-arm64/"
        "Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")))
    if not c:
        sys.exit("No encuentro Chromium de Playwright")
    return c[-1]


def renderizar(codigo):
    """Bloque Mermaid sin PNG en el repo: lo dibuja con el estilo del repo (cacheado)."""
    from estilo_vp import MERMAID
    os.makedirs(CACHE, exist_ok=True)
    h = hashlib.sha1(codigo.encode()).hexdigest()[:16]
    png = CACHE + h + ".png"
    if os.path.exists(png):
        return png
    mmd, tema, cfg = CACHE + h + ".mmd", CACHE + "tema.json", CACHE + "puppeteer.json"
    open(mmd, "w", encoding="utf-8").write(codigo)
    json.dump(MERMAID, open(tema, "w"))
    json.dump({"executablePath": buscar_chromium(), "args": ["--no-sandbox"]}, open(cfg, "w"))
    base = [buscar_mmdc(), "-p", cfg, "-c", tema, "-i", mmd, "-b", "white", "-q"]
    svg = CACHE + h + ".svg"
    sh(base + ["-o", svg])
    vb = re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"', open(svg, encoding="utf-8").read())
    lado = int(max(float(vb.group(1)), float(vb.group(2)))) + 1
    sh(base + ["-o", png, "-s", "2", "--size", str(lado)])
    return png


# ---------- portada ----------
def p_xml(texto, tam=22, negrita=False, centrado=True, antes=0, despues=120, color=None):
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    rpr = '<w:rFonts w:ascii="Verdana" w:hAnsi="Verdana"/>' + ("<w:b/>" if negrita else "")
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    rpr += f'<w:sz w:val="{tam}"/>'
    jc = '<w:jc w:val="center"/>' if centrado else ""
    return (f'<w:p><w:pPr><w:spacing w:before="{antes}" w:after="{despues}"/>{jc}</w:pPr>'
            f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{texto}</w:t></w:r></w:p>')


def salto_pagina():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def portada(titulo_doc, campos):
    x = [p_xml(UNIVERSIDAD, 28, True, antes=600),
         p_xml(FACULTAD, 22),
         p_xml("Carreras: " + CARRERA, 22),
         p_xml("Materia: " + MATERIA, 22, despues=1400),
         p_xml("Proyecto", 28, antes=600),
         p_xml("SPLG – Sistema de Pedidos y Logística de Garrafas de Gas", 40, True, despues=500),
         p_xml(titulo_doc, 32, True, despues=1000)]
    for k, v in campos:
        if k.lower() == "proyecto":
            continue
        x.append(p_xml(f"{k}: {v}", 22, despues=80))
    x.append(salto_pagina())
    return "```{=openxml}\n" + "".join(x) + "\n```\n"


def partir(md):
    """Devuelve (titulo, [(clave, valor)], resto) con el encabezado en negritas antes del primer ---."""
    lineas = md.split("\n")
    titulo = re.sub(r"^#\s+", "", lineas[0]).strip()
    campos, i = [], 1
    while i < len(lineas) and lineas[i].strip() != "---":
        m = re.match(r"\*\*(.+?):\*\*\s*(.*?)\s*$", lineas[i])
        if m:
            campos.append((m.group(1), m.group(2)))
        i += 1
    return titulo, campos, "\n".join(lineas[i + 1:])


def subir_version(v):
    a, b = v.split(".")
    return f"{a}.{int(b) + 1}"


# ---------- estructura de la plantilla ----------
class Nodo:
    def __init__(self, nivel, titulo, cuerpo=None):
        self.nivel, self.titulo, self.cuerpo, self.hijos, self.padre = nivel, titulo, cuerpo or [], [], None


def parsear(texto):
    raiz = Nodo(1, "")
    pila, fence = [raiz], False
    for l in texto.split("\n"):
        if l.startswith("```"):
            fence = not fence
        m = re.match(r"(#{1,6}) (.*)$", l)
        if m and not fence:
            n = Nodo(len(m.group(1)), m.group(2).strip())
            while pila[-1].nivel >= n.nivel:
                pila.pop()
            n.padre = pila[-1]
            pila[-1].hijos.append(n)
            pila.append(n)
        else:
            pila[-1].cuerpo.append(l)
    return raiz


def sin_numero(t):
    return re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", t).strip()


def buscar(raiz, titulo, empieza=False):
    for n in raiz.hijos:
        t = sin_numero(n.titulo)
        if t == titulo or (empieza and t.startswith(titulo)):
            return n
        r = buscar(n, titulo, empieza)
        if r:
            return r
    return None


def sacar(raiz, titulo, empieza=False):
    n = buscar(raiz, titulo, empieza)
    if not n:
        sys.exit(f"no encuentro la sección «{titulo}»")
    n.padre.hijos.remove(n)
    n.padre = None
    return n


def nuevo(titulo, hijos=(), cuerpo=None):
    n = Nodo(1, titulo, cuerpo)
    for h in hijos:
        n.hijos.append(h)
    return n


def renombrar(n, titulo):
    n.titulo = titulo
    return n


def absorber(padre, desde, hasta):
    """Los hermanos de `desde` hasta `hasta` (sin incluirlo) pasan a ser hijos de `desde`."""
    lista = padre.hijos
    i = next(k for k, h in enumerate(lista) if sin_numero(h.titulo).startswith(desde))
    j = next(k for k, h in enumerate(lista) if sin_numero(h.titulo).startswith(hasta))
    mover = lista[i + 1:j]
    lista[i + 1:j] = []
    lista[i].hijos.extend(mover)


DSS = re.compile(r"^(?:(?:Crítico|Importante|Secundario|Menor)(?: · automático)? )?DSS — (CU-\d+): (.*)$")


def titulo_final(t):
    t = sin_numero(t)
    m = DSS.match(t)
    if m:
        return f"Diagrama de Sistema Para el caso de Uso {m.group(1)} {m.group(2)}:"
    return t


# Títulos de nivel 2 de cada plantilla; cualquier otra subsección propia baja a nivel 3.
H2_PLANTILLA = {
    "0": {"Plan de las Fases", "Calendario del Proyecto", "Actores", "Diagrama de Caso de Uso",
          "Casos de Usos de Alto Nivel"},
    "1": {"Participantes del Proyecto", "Objetivos del sistema", "Diagrama de Caso de Uso del Sistema", "Casos de Usos",
          "Subsistemas del Proyecto", "Requisitos de Información", "Requisitos de Funcionales", "Requisitos No funcionales"},
    "2": {"Lista de Concepto Candidatos", "Lista de conceptos idóneos", "Descripción del Concepto",
          "Relaciones entre los conceptos", "Descripción de los Atributos", "Diagrama Conceptual",
          "Diagrama de Secuencias a Nivel de Sistema", "Contratos"},
    "3": {"Operaciones"},
}


def emitir(n, nivel, out, permitidos=None):
    if permitidos is not None and nivel == 2 and sin_numero(n.titulo) not in permitidos:
        nivel = 3
    out.append("#" * min(nivel, 6) + " " + titulo_final(n.titulo))
    out.extend(n.cuerpo)
    for h in n.hijos:
        emitir(h, nivel + 1, out, permitidos)


INTRO_PLAN = "En esta sección se presenta la organización en fases e iteraciones y el calendario del proyecto."


def armar(clave, raiz):
    """Ordena el documento como la plantilla de la cátedra. Devuelve (secciones de nivel 1, anexos)."""
    anexos = []

    def anexo(titulo, empieza=False):
        anexos.append(sacar(raiz, titulo, empieza))

    if clave == "0":
        anexo("Índice de Figuras"); anexo("Componentes del Sistema")
        anexo("Plan de construcción de los casos de uso planificados")
        fases = renombrar(sacar(raiz, "Plan de las Fases"), "Plan de las Fases")
        fases.hijos.append(sacar(raiz, "Hitos por Fase"))
        cal = renombrar(sacar(raiz, "Calendario del Proyecto — Diagrama de Gantt"), "Calendario del Proyecto")
        plan = nuevo("Plan del Proyecto", [fases, cal], [INTRO_PLAN, ""])
        actores = renombrar(sacar(raiz, "Actores del Sistema"), "Actores")
        dcu = renombrar(sacar(raiz, "Diagrama de Casos de Uso del Sistema"), "Diagrama de Caso de Uso")
        cua = renombrar(sacar(raiz, "Casos de Uso de Alto Nivel"), "Casos de Usos de Alto Nivel")
        grupo = nuevo("Casos de Usos y Actores", [actores, dcu, cua])
        cal2 = renombrar(sacar(raiz, "Calificación de los Casos de Uso"), "Calificación de los Casos de usos")
        return [plan, grupo, cal2], anexos
    if clave == "0.1":
        anexo("Índice de Figuras") if buscar(raiz, "Índice de Figuras") else None
        anexo("Índice de Iteraciones")
        return list(raiz.hijos), anexos
    if clave == "1":
        anexo("Leyenda de Prioridad"); anexo("Relaciones entre Casos de Uso", True)
        figuras = sacar(raiz, "Índice de Figuras")
        pres = renombrar(sacar(raiz, "Presentación General"), "Presentación General")
        obj = renombrar(sacar(raiz, "Objetivos del Sistema"), "Objetivos del sistema")
        dcu = renombrar(sacar(raiz, "Diagrama de Casos de Uso del Sistema"), "Diagrama de Caso de Uso del Sistema")
        lista = renombrar(sacar(raiz, "Casos de Uso: lista e importancia"), "Casos de Usos")
        subs = renombrar(sacar(raiz, "Subsistemas del Proyecto"), "Subsistemas del Proyecto")
        dsub = renombrar(sacar(subs, "Diagramas de Casos de Uso por Subsistema"), "Diagrama de Casos de Usos")
        pres.hijos += [obj, dcu, lista, subs]
        itera = renombrar(sacar(raiz, "Objetivos de la Iteración"), "Objetivos de la Iteración")
        info = renombrar(sacar(raiz, "Requisitos de Información"), "Requisitos de Información")
        func = renombrar(sacar(raiz, "Requisitos Funcionales — Casos de Uso"), "Requisitos de Funcionales")
        actores = renombrar(sacar(func, "Definición de Actores"), "Definición de Actores")
        cue = nuevo("Caso de Usos del Sistema", list(func.hijos))
        func.hijos = [dsub, actores, cue]
        nf = renombrar(sacar(raiz, "Requisitos No Funcionales"), "Requisitos No funcionales")
        req = nuevo("Requisitos del Sistema", [info, func, nf])
        matriz = renombrar(sacar(raiz, "Matriz de Rastreabilidad Objetivos / Requisitos"), "Matriz de Rastreabilidad Objetivo/Requisitos")
        glos = renombrar(sacar(raiz, "Glosario de Términos"), "Glosario de Términos")
        return [figuras, pres, itera, req, matriz, glos], anexos
    if clave == "2":
        anexo("Índice de Figuras"); anexo("Leyenda"); anexo("Módulos Inteligentes del Sistema")
        mc = renombrar(sacar(raiz, "Modelo Conceptual (Modelo de Dominio)"), "Modelo Conceptual")
        for viejo, nuevo_t in (("Lista de Conceptos Candidatos", "Lista de Concepto Candidatos"),
                               ("Relaciones entre los Conceptos", "Relaciones entre los conceptos")):
            renombrar(buscar(mc, viejo), nuevo_t)
        ido = renombrar(buscar(mc, "Lista de Conceptos Idóneos"), "Lista de conceptos idóneos")
        # la tabla de conceptos idóneos es la «Descripción del Concepto» (Símbolo / Intención / Extensión)
        i = next(k for k, l in enumerate(ido.cuerpo) if l.startswith("| # | Descripción del Concepto"))
        desc = Nodo(2, "Descripción del Concepto", ido.cuerpo[i:])
        ido.cuerpo = ido.cuerpo[:i]
        mc.hijos.insert(mc.hijos.index(ido) + 1, desc)
        comp = renombrar(sacar(raiz, "Comportamiento del Sistema"), "Comportamiento del Sistema")
        absorber(comp, "Diagramas de Secuencia a Nivel de Sistema", "Contratos de Operaciones del Sistema")
        renombrar(buscar(comp, "Diagramas de Secuencia a Nivel de Sistema"), "Diagrama de Secuencias a Nivel de Sistema")
        renombrar(buscar(comp, "Contratos de Operaciones del Sistema"), "Contratos")
        glos = renombrar(sacar(raiz, "Glosario"), "Glosario")
        return [mc, comp, glos], anexos
    if clave == "3":
        anexo("Índice de Figuras"); anexo("Leyenda de Prioridad"); anexo("Introducción")
        anexo("Arquitectura del Sistema")
        anexo("Observaciones transversales de diseño"); anexo("Operaciones del sistema")
        anexo("Tabla de implementación por caso de uso")
        for t in ("Módulos Inteligentes — Especificación Detallada", "Pantallas UI — Wireframes y Diagramas",
                  "Decisiones de Diseño Relevantes", "Trazabilidad Diseño → Análisis → Requisitos",
                  "Trabajo futuro", "Diagramas de Estados y de Actividad"):
            anexo(t)
        reales = renombrar(sacar(raiz, "Casos de Uso Reales (CU Real)"), "Casos de Usos Reales")
        inter = renombrar(sacar(raiz, "Diagramas de Interacción (Nivel de Diseño)"), "Diagrama de Interacción")
        grupos = list(inter.hijos)
        inter.hijos = [nuevo("Operaciones", grupos)]
        clases = renombrar(sacar(raiz, "Diagrama de Clases de Diseño"), "Diagrama de Clase")
        return [reales, inter, clases], anexos
    return None, anexos


def peso_linea(l):
    return sum(os.path.getsize(m) for m in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", l) if os.path.exists(m))


def puntos_de_corte(lineas):
    """Dónde se puede partir: {línea: dentro de una sección horizontal}. Antes de un título de nivel 1 a 3,
    justo después de un pie de figura (y de su cierre de sección) o entre franjas «(continúa)»."""
    pts, fence, land, i = {}, False, False, 0
    while i < len(lineas):
        l = lineas[i]
        if l.startswith("```{=openxml}") and i + 1 < len(lineas):
            cuerpo = lineas[i + 1]
            if "(continúa)" in cuerpo:
                pts[i + 3] = land
            elif "<w:sectPr>" in cuerpo:
                land = 'w:orient="landscape"' not in cuerpo
            i += 3
            continue
        if l.startswith("```"):
            fence = not fence
        elif not fence:
            if re.match(r"#{1,3} ", l):
                pts[i] = False
            elif l.startswith("**Figura "):
                j = i + 1
                while j < len(lineas) and not lineas[j].strip():
                    j += 1
                if j < len(lineas) and lineas[j].startswith("```{=openxml}") and "orient" in lineas[j + 1]:
                    j += 3
                pts[j] = False
        i += 1
    return pts


def cortar(resto, parte, total):
    """Parte `parte` de `total` del cuerpo, repartiendo el peso de las imágenes."""
    if total == 1:
        return resto
    lineas = resto.split("\n")
    pesos = [peso_linea(l) for l in lineas]
    puntos = puntos_de_corte(lineas)
    objetivo = sum(pesos) / total
    cortes, acum = [0], 0
    for i, l in enumerate(lineas):
        if len(cortes) < total and acum >= objetivo * len(cortes) and i in puntos and i > cortes[-1]:
            cortes.append(i)
        acum += pesos[i]
    if len(cortes) < total:
        raise ValueError("no hay dónde partir en %d" % total)
    cortes.append(len(lineas))
    texto = "\n".join(lineas[cortes[parte - 1]:cortes[parte]])
    if parte > 1 and puntos.get(cortes[parte - 1]):
        texto = MARCA_INI.strip() + "\n\n" + texto      # la parte anterior cerró la sección horizontal: abro otra
    if parte < total and puntos.get(cortes[parte]):
        texto = texto + "\n\n" + MARCA_FIN.strip()
    return texto


TITULOS_PORTADA = {"0.1": "Planificación de la Iteración", "2": "Fase II Análisis", "3": "Fase III de Diseño"}
CON_LISTA_COMO_TITULO = ("1", "0.1")   # las plantillas 1 y 0.1 traen «Lista de Cambios» como sección


def preparar_md(clave, nombre_md, parte=1, total=1):
    md = open(D + nombre_md, encoding="utf-8").read()
    titulo, campos, resto = partir(md)
    titulo = TITULOS_PORTADA.get(clave, titulo)
    # la plantilla lleva la Lista de Cambios antes del índice
    m = re.search(r"^## Lista de Cambios\n(.*?)(?=^## )", resto, re.S | re.M)
    cambios = ""
    if m:
        tabla = m.group(1)
        resto = resto[:m.start()] + resto[m.end():]
        filas = re.findall(r"^\| (\d+) \|", tabla, re.M)
        tabla = tabla.rstrip("\n") + f"\n| {int(filas[-1]) + 1} | {FECHA_ISO} | {CAMBIO} | {AUTOR} |\n\n"
        if clave in CON_LISTA_COMO_TITULO:
            cambios = "# Lista de Cambios\n" + tabla
        else:
            cambios = ("```{=openxml}\n" + p_xml("Lista de Cambios", 32, True, centrado=False, despues=200)
                       + "\n```\n" + tabla)
    campos = [(k, subir_version(v) if k == "Versión" else FECHA if k == "Fecha" else v) for k, v in campos]
    mmds = mapa_mmd()
    contador = {"png": 0, "render": 0}

    def bloque(mo):
        cod = mo.group(1)
        png = mmds.get(norm(cod))
        if png:
            contador["png"] += 1
        else:
            png = renderizar(cod)
            contador["render"] += 1
        return imagen_md(png)

    # el pie de figura va siempre debajo de la imagen
    resto = re.sub(r"(\*\*Figura \d+ — [^\n]*\*\*)\n\n(!\[[^\]]*\]\([^)\s]+\)|```mermaid\n.*?^```)",
                   lambda m: m.group(2) + "\n\n" + m.group(1), resto, flags=re.S | re.M)
    resto = re.sub(r"^```mermaid\n(.*?)^```[ \t]*$", bloque, resto, flags=re.S | re.M)

    def imagen(mo):
        ruta = mo.group(2)
        if ruta.startswith("http") or not os.path.exists(D + ruta):
            return mo.group(0)
        return imagen_md(D + ruta)

    resto = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)(?!\{)", imagen, resto)
    resto = re.sub(r"@@FIN@@\s*(\*\*Figura \d+ — [^\n]*\*\*)", r"\1\n\n@@FIN@@", resto)
    resto = resto.replace("@@INI@@", MARCA_INI.strip()).replace("@@FIN@@", MARCA_FIN.strip())
    raiz = parsear(resto)
    secciones, anexos = armar(clave, raiz)
    # lo que quedó sin ubicar (texto suelto antes del primer título o secciones no previstas) falla fuerte
    sobrantes = [n.titulo for n in raiz.hijos if n not in secciones]
    if sobrantes or "".join(raiz.cuerpo).strip(" -\n"):
        sys.exit(f"{nombre_md}: contenido sin ubicar en la estructura de la plantilla: {sobrantes} {raiz.cuerpo[:3]}")
    salida = []
    for sec in secciones:
        emitir(sec, 1, salida, H2_PLANTILLA.get(clave))
    for i, an in enumerate(anexos):
        an.titulo = f"Anexo {chr(65 + i)} – {sin_numero(an.titulo)}"
        emitir(an, 1, salida)
    resto = "\n".join(salida)
    resto = cortar(resto, parte, total)
    if total > 1:
        titulo += f" (Parte {parte} de {total})"
    cuerpo = (portada(titulo, campos) + "\n" + cambios + "\n"
              + "```{=openxml}\n" + salto_pagina() + p_xml("Índice", 32, True, centrado=False, despues=200) + "<w:p><w:r><w:t>@@TOC@@</w:t></w:r></w:p>\n```\n\n"
              + resto)
    return cuerpo, contador, dict(campos).get("Versión", "")


# ---------- reference-doc ----------
def reference(plantilla_doc, destino):
    """pandoc reference.docx con página y tipografía de la plantilla de la cátedra."""
    tmp = tempfile.mkdtemp()
    sh(["textutil", "-convert", "docx", "-output", tmp + "/p.docx", D + ".catedra-ref/" + plantilla_doc])
    doc = zipfile.ZipFile(tmp + "/p.docx").read("word/document.xml").decode("utf8")
    pg_sz = re.search(r"<w:pgSz[^>]*/>", doc).group(0)
    pg_mar = re.search(r"<w:pgMar[^>]*/>", doc).group(0)
    base = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                          capture_output=True).stdout
    open(tmp + "/base.docx", "wb").write(base)
    zin = zipfile.ZipFile(tmp + "/base.docx")
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == "word/document.xml":
                s = data.decode("utf8")
                s = re.sub(r"<w:pgSz[^>]*/>", pg_sz, s)
                s = re.sub(r"<w:pgMar[^>]*/>", pg_mar, s)
                data = s.encode("utf8")
            elif it.filename == "word/styles.xml":
                s = data.decode("utf8")
                s = re.sub(r'(<w:rFonts)[^>]*/>', r'\1 w:ascii="Verdana" w:hAnsi="Verdana" w:cs="Verdana" w:eastAsia="Verdana"/>', s)
                s = re.sub(r'(<w:style w:type="paragraph" w:styleId="(?:BodyText|FirstParagraph|Compact)">.*?<w:name[^>]*/>)',
                           r'\1', s, flags=re.S)
                # tablas con bordes
                bordes = ('<w:tblBorders>' + "".join(
                    f'<w:{l} w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
                    for l in ("top", "left", "bottom", "right", "insideH", "insideV")) + '</w:tblBorders>')
                s = re.sub(r'(<w:style w:type="table"[^>]*w:styleId="Table">.*?<w:tblPr>)', r"\1" + bordes, s, count=1, flags=re.S)
                # texto de 10 pt; tablas de 9 pt; títulos en Verdana con jerarquía visible y sin quedar solos al pie
                s = re.sub(r"(<w:docDefaults>.*?)<w:sz w:val=\"24\" />\s*<w:szCs w:val=\"24\" />", r'\1<w:sz w:val="20"/><w:szCs w:val="20"/>', s, count=1, flags=re.S)
                s = s.replace('<w:spacing w:before="180" w:after="180" />', '<w:spacing w:before="100" w:after="100" />')
                s = re.sub(r'(w:styleId="Compact">.*?<w:pPr>.*?</w:pPr>)', r'\1<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>', s, count=1, flags=re.S)
                for k, (nombre, sz, antes, desp, color) in enumerate((
                        ("heading 1", 36, 480, 160, "1F3864"), ("heading 2", 28, 320, 120, "2F5496"),
                        ("heading 3", 24, 240, 100, "2F5496"), ("heading 4", 22, 200, 80, "404040"),
                        ("heading 5", 20, 160, 60, "404040"), ("heading 6", 20, 120, 60, "404040")), start=1):
                    nuevo_estilo = (f'<w:style w:type="paragraph" w:styleId="Heading{k}"><w:name w:val="{nombre}"/>'
                                    '<w:basedOn w:val="Normal"/><w:next w:val="BodyText"/><w:uiPriority w:val="9"/><w:qFormat/>'
                                    f'<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="{antes}" w:after="{desp}"/>'
                                    f'<w:outlineLvl w:val="{k - 1}"/></w:pPr><w:rPr><w:rFonts w:ascii="Verdana" w:hAnsi="Verdana" '
                                    f'w:cs="Verdana" w:eastAsia="Verdana"/><w:b/><w:bCs/><w:color w:val="{color}"/>'
                                    f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr></w:style>')
                    s = re.sub(rf'<w:style w:type="paragraph" w:styleId="Heading{k}">.*?</w:style>', lambda m: nuevo_estilo, s,
                               count=1, flags=re.S)
                s = s.replace("</w:styles>",
                              '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Imagen"><w:name w:val="Imagen"/>'
                              '<w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="60"/>'
                              '<w:jc w:val="center"/></w:pPr></w:style></w:styles>')
                data = s.encode("utf8")
            elif it.filename == "word/theme/theme1.xml":
                s = data.decode("utf8")
                s = re.sub(r'(<a:(?:major|minor)Font>\s*<a:latin typeface=")[^"]*', r"\1Verdana", s)
                data = s.encode("utf8")
            zout.writestr(it, data)
    shutil.rmtree(tmp)


FILTRO = """
function Para(el)
  if #el.content == 1 and el.content[1].t == 'Image' then
    return pandoc.Div(el, pandoc.Attr('', {}, {['custom-style'] = 'Imagen'}))
  end
end
"""


ANCHO_UTIL = 9000  # twips de texto entre márgenes


def columnas_al_ancho(m):
    """Reparte el ancho útil entre las columnas según cuánto texto lleva cada una
    (el visor de Drive respeta las columnas de la grilla, no el ancho de la tabla)."""
    tabla = m.group(0)
    cols = re.findall(r"<w:gridCol [^>]*/>", tabla)
    if not cols:
        return tabla
    largo = [1.0] * len(cols)
    for fila in re.findall(r"<w:tr>.*?</w:tr>", tabla, re.S):
        celdas = re.findall(r"<w:tc>.*?</w:tc>", fila, re.S)
        if len(celdas) != len(cols):
            continue
        for i, c in enumerate(celdas):
            texto = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", c))
            largo[i] = max(largo[i], min(len(texto), 120))
    # una columna corta (fechas, códigos) no se parte: hasta 14 caracteres entra entera
    minimo = [max(560, int(min(l, 14) * 115)) for l in largo]
    if sum(minimo) > ANCHO_UTIL:
        minimo = [int(ANCHO_UTIL / len(cols))] * len(cols)
    peso = [max(l, 6) ** 0.7 for l in largo]
    total = sum(peso)
    resto = ANCHO_UTIL - sum(minimo)
    anchos = [minimo[i] + int(resto * p / total) for i, p in enumerate(peso)]
    grilla = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{a}"/>' for a in anchos) + "</w:tblGrid>"
    return re.sub(r"<w:tblGrid>.*?</w:tblGrid>", grilla, tabla, count=1, flags=re.S)


NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')


def _run(t, tam=16):
    return (f'<w:r><w:rPr><w:rFonts w:ascii="Verdana" w:hAnsi="Verdana"/><w:sz w:val="{tam}"/></w:rPr>'
            f'<w:t xml:space="preserve">{t}</w:t></w:r>')


def encabezado_xml():
    """Como el pie de la plantilla: proyecto, iteración y equipo."""
    tab = '<w:r><w:tab/></w:r>'
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}><w:p><w:pPr>'
            '<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="808080"/></w:pBdr>'
            '<w:tabs><w:tab w:val="center" w:pos="4500"/><w:tab w:val="right" w:pos="9000"/></w:tabs></w:pPr>'
            + _run("SPLG – Sistema de Pedidos y Logística de Garrafas de Gas") + tab + _run("Iteración C-19") + tab
            + _run("Equipo: " + AUTOR) + '</w:p></w:hdr>')


def pie_xml(version):
    campo = ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
             '<w:r><w:fldChar w:fldCharType="separate"/></w:r>' + _run("1") + '<w:r><w:fldChar w:fldCharType="end"/></w:r>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}><w:p><w:pPr>'
            '<w:tabs><w:tab w:val="right" w:pos="9000"/></w:tabs></w:pPr>'
            + _run("Versión: " + version) + '<w:r><w:tab/></w:r>' + _run("Página ") + campo + '</w:p></w:ftr>')


def con_encabezado(zin, doc2, version):
    """Devuelve {nombre: bytes} con encabezado y pie agregados a la sección final del documento."""
    ct = zin.read("[Content_Types].xml").decode("utf8")
    ct = ct.replace("</Types>",
                    '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
                    '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
    rels = zin.read("word/_rels/document.xml.rels").decode("utf8")
    rels = rels.replace("</Relationships>",
                        '<Relationship Id="rIdSplgH" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
                        '<Relationship Id="rIdSplgF" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>')
    refs = '<w:headerReference w:type="default" r:id="rIdSplgH"/><w:footerReference w:type="default" r:id="rIdSplgF"/>'
    doc2 = re.sub(r"(<w:sectPr[^>]*>)", r"\1" + refs, doc2)
    if 'xmlns:r=' not in doc2[:2000]:
        doc2 = doc2.replace("<w:document ", '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
    return {"[Content_Types].xml": ct.encode("utf8"), "word/_rels/document.xml.rels": rels.encode("utf8"),
            "word/document.xml": doc2.encode("utf8"), "word/header1.xml": encabezado_xml().encode("utf8"),
            "word/footer1.xml": pie_xml(version).encode("utf8")}


def tamanos_de_imagen(doc):
    """Restituye el tamaño pedido a cada imagen (pandoc las limita al ancho de la página vertical)."""
    def una(m):
        d = m.group(0)
        t = re.search(r'descr="SPLGSZ:([\d.]+)x([\d.]+)"', d)
        if not t:
            return d
        cx, cy = int(float(t.group(1)) * 360000), int(float(t.group(2)) * 360000)
        d = re.sub(r"<wp:extent [^>]*/>", f'<wp:extent cx="{cx}" cy="{cy}"/>', d, count=1)
        d = re.sub(r"<a:ext cx=\"\d+\" cy=\"\d+\"\s*/>", f'<a:ext cx="{cx}" cy="{cy}"/>', d, count=1)
        return d.replace(t.group(0), 'descr="Diagrama"')
    return re.sub(r"<wp:inline.*?</wp:inline>", una, doc, flags=re.S)


def indice_estatico(doc):
    """Índice en texto con vínculo interno a cada título de nivel 1 a 3 (sirve en Word y en el visor de Drive)."""
    entradas, n = [], [0]

    def marcar(m):
        p = m.group(0)
        est = re.search(r'<w:pStyle w:val="Heading([123])"\s*/>', p)
        if not est:
            return p
        n[0] += 1
        nombre = f"splg_h{n[0]}"
        texto = re.sub(r"<[^>]+>", "", p).strip()
        entradas.append((int(est.group(1)), texto, nombre))
        p = re.sub(r"(</w:pPr>)", rf'\1<w:bookmarkStart w:id="{9000 + n[0]}" w:name="{nombre}"/>', p, count=1)
        return p.replace("</w:p>", f'<w:bookmarkEnd w:id="{9000 + n[0]}"/></w:p>')

    doc = re.sub(r"<w:p>(?:(?!</w:p>).)*?</w:p>", marcar, doc, flags=re.S)
    filas = []
    for nivel, texto, nombre in entradas:
        t = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        sang = {1: 0, 2: 400, 3: 800}[nivel]
        filas.append(
            f'<w:p><w:pPr><w:spacing w:before="{80 if nivel == 1 else 0}" w:after="20"/><w:ind w:left="{sang}"/></w:pPr>'
            f'<w:hyperlink w:anchor="{nombre}"><w:r><w:rPr><w:rFonts w:ascii="Verdana" w:hAnsi="Verdana"/>'
            f'{"<w:b/>" if nivel == 1 else ""}<w:color w:val="1F3864"/><w:sz w:val="{20 if nivel == 1 else 18 if nivel == 2 else 16}"/></w:rPr>'
            f'<w:t xml:space="preserve">{t}</w:t></w:r></w:hyperlink></w:p>')
    marca = re.search(r"<w:p>(?:(?!</w:p>).)*?@@TOC@@.*?</w:p>", doc, re.S)
    if not marca:
        sys.exit("no encuentro la marca del índice")
    return doc[:marca.start()] + "".join(filas) + salto_pagina() + doc[marca.end():]


def encabezados_de_tabla(doc):
    """Encabezado de cada tabla en negrita y con fondo gris claro."""
    def fila(m):
        f = m.group(0)
        if "<w:tblHeader" not in f:
            return f
        f = re.sub(r"<w:tcPr\s*/>", '<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="E7E6E6"/></w:tcPr>', f)
        f = re.sub(r"<w:r>(?!<w:rPr>)", "<w:r><w:rPr><w:b/></w:rPr>", f)
        return re.sub(r"<w:r><w:rPr>(?!<w:b/>)", "<w:r><w:rPr><w:b/>", f)
    return re.sub(r"<w:tr>.*?</w:tr>", fila, doc, flags=re.S)


def generar(clave, nombre_md, plantilla, titulo, parte=1, total=1):
    os.makedirs(CACHE, exist_ok=True)
    cuerpo, cont, version = preparar_md(clave, nombre_md, parte, total)
    mdi = CACHE + f"doc-{clave}.md"
    open(mdi, "w", encoding="utf-8").write(cuerpo)
    ref = CACHE + f"ref-{clave}.docx"
    reference(plantilla, ref)
    filtro = CACHE + "imagenes.lua"
    open(filtro, "w").write(FILTRO)
    if total > 1:
        titulo += f" (Parte {parte})"
    salida = SALIDA + f"TF - 2026 - {titulo} - {AUTOR_ARCHIVO} - {FECHA_ISO}.docx"
    crudo = CACHE + f"crudo-{clave}.docx"
    sh(["pandoc", mdi, "-f", "gfm+attributes+raw_attribute", "-t", "docx", "-o", crudo,
        "--reference-doc", ref,
        "--lua-filter", filtro, "--resource-path", D, "--columns=100"], cwd=D)
    zin = zipfile.ZipFile(crudo)
    doc2 = zin.read("word/document.xml").decode("utf8")
    doc2 = tamanos_de_imagen(doc2)
    doc2 = indice_estatico(doc2)
    doc2 = encabezados_de_tabla(doc2)
    # las tablas ocupan el ancho de la página (pandoc las deja al ancho del contenido)
    doc2 = re.sub(r"<w:tblW [^>]*/>", '<w:tblW w:type="pct" w:w="5000"/>', doc2)
    doc2 = re.sub(r"<w:tbl>.*?</w:tbl>", columnas_al_ancho, doc2, flags=re.S)
    nuevos = con_encabezado(zin, doc2, version)
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as zout:
        for nombre_p, data in nuevos.items():
            if nombre_p.startswith("word/header") or nombre_p.startswith("word/footer"):
                zout.writestr(nombre_p, data)
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename in nuevos:
                data = nuevos[it.filename]
            zout.writestr(it, data)
    print(f"{os.path.basename(salida)}: {os.path.getsize(salida) / 1e6:.1f} MB · "
          f"{cont['png']} diagramas con PNG del repo, {cont['render']} renderizados")
    return salida


def main_doc(d):
    """Un .docx por documento. Con SPLG_DOCX_LIMITE_MB, si pasa el tope se parte en 2, 3…
    (mismo encabezado, numeración continua); la resolución no se toca."""
    global DPI_MAX
    DPI_MAX = 150
    for total in (1, 2, 3, 4, 5, 6, 8, 10, 12):
        try:
            salidas = [generar(*d, parte=i, total=total) for i in range(1, total + 1)]
        except ValueError as e:
            print("  ", e)
            break
        if all(os.path.getsize(x) < LIMITE for x in salidas):
            return salidas
        print(f"  {total} parte(s): {[round(os.path.getsize(x) / 1e6, 1) for x in salidas]} MB, parto más")
        for x in salidas:
            os.unlink(x)
    sys.exit("no entra en el límite")


def main():
    pedidos = set(sys.argv[1:])
    os.makedirs(SALIDA, exist_ok=True)
    os.makedirs(DESTINO, exist_ok=True)
    for d in DOCS:
        if pedidos and d[0] not in pedidos:
            continue
        nombre = f"TF - 2026 - {d[3]}"
        for viejo in glob.glob(SALIDA + nombre + "*.docx") + glob.glob(DESTINO + nombre + "*.docx"):
            os.unlink(viejo)
        for s in main_doc(d):
            shutil.copy(s, DESTINO)
    print("Copiados a", DESTINO)


if __name__ == "__main__":
    main()
