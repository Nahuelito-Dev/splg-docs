#!/usr/bin/env python3
"""Genera los cinco documentos de la cátedra en Word (.docx) a partir de los .md.

    python3 herramientas/generar-docx-catedra.py            # los cinco
    python3 herramientas/generar-docx-catedra.py 2 3        # sólo algunos (0, 0.1, 1, 2, 3)

Salida: `catedra/entregables/catedra-docx/*.docx`, copiados a `~/Desktop/SPLG-Documentacion-Catedra/`.

Los .md son la fuente y no se tocan. Por documento arma un .md intermedio (portada y
Lista de Cambios al principio, como en la plantilla; cada bloque Mermaid reemplazado por su
PNG, o renderizado con mermaid-cli si no tiene) y lo convierte con pandoc usando un
reference-doc con la página y la tipografía de la plantilla (`catedra/.catedra-ref/*.doc`, que se
convierte con `textutil`). Requiere pandoc, textutil (macOS) y mermaid-cli (npx cache).
"""
import datetime, glob, hashlib, json, os, re, shutil, struct, subprocess, sys, tempfile, zipfile
from imagenes_cu import desplegar

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DOC = D + "documentos/"
sys.path.insert(0, D + "herramientas")
SALIDA = D + "catedra/entregables/catedra-docx/"
CACHE = SALIDA + ".cache/"
DESTINO = os.path.expanduser("~/Desktop/SPLG-Documentacion-Catedra/")
AUTOR_ARCHIVO = "Wagner Nahuel"

UNIVERSIDAD = "Universidad Nacional de Misiones"
FACULTAD = "Facultad de Ciencias Exactas, Químicas y Naturales"
CARRERA = "Licenciatura en Sistemas de Información – Analista en Sistemas de Computación"
MATERIA = "Proyecto Software (LSI) | Trabajo Final (ASC)"
AUTOR = "Nahuel Wagner"
# fecha de la entrega (portada, nombre del archivo y fila nueva de la Lista de Cambios): hoy, o SPLG_DOCX_FECHA=AAAA-MM-DD
FECHA_ISO = os.environ.get("SPLG_DOCX_FECHA") or datetime.date.today().isoformat()
FECHA = "/".join(reversed(FECHA_ISO.split("-")))
CAMBIO = os.environ.get("SPLG_DOCX_CAMBIO", "Actualización al estado de la Construcción, C-19")

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


def franjas(alto, franja):
    """Cantidad de franjas de `franja` px para cubrir `alto`; si la última sería una tira de menos del 6 %,
    se reparte entre las demás (cada una crece a lo sumo un 6 %, todavía entra en la página)."""
    n = -(-alto // franja)
    if n > 1 and alto - (n - 1) * franja < 0.06 * franja:
        n -= 1
        franja = -(-alto // n)
    return franja, n


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
        franja, n = franjas(hb, int(PORT_H / ancho * wb))
        return CONTINUA.join(img(f, ancho, ancho * tam_png(f)[1] / wb) for f in cortar_png(base, franja, n))
    # horizontal
    dl = min(LAND_W, LAND_H * w / h)
    if (pt_texto(w, dl) < MIN_PT <= pt_texto(w, LAND_W) or dl < 0.6 * LAND_W) and w > 1100:
        dl = LAND_W
        px = min(int(dl / 2.54 * DPI_HOR), w)
        base = optimizar(ruta, px, "h")
        wb, hb = tam_png(base)
        franja, n = franjas(hb, int(LAND_H / dl * wb))
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
        self.ancla = None


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


# ---------- anclas y enlaces internos ----------
# Destinos: cada título que nombra un caso de uso, un IRQ o un NFR, y cada título numerado (para «sección 8.3» o
# «§8.3»); y la fila de la tabla que define cada objetivo (OBJ-nn). Las referencias en el texto a uno de esos
# destinos pasan a ser hipervínculos internos; las que apuntan a algo que no está en este documento (un caso sin
# ficha, otro documento) quedan como texto.
COD_DESTINO = re.compile(r"\b(CU-\d{3}|IRQ-\d{2}|NFR-\d{2})\b")
REF = re.compile(r"(?<![\w#\[/-])(CU-\d{3}|IRQ-\d{2}|NFR-\d{2}|OBJ-\d{2})(?![\w-])"
                 r"|(?<![\w])(secci[oó]n(?:es)? |§ ?)(\d+(?:\.\d+)*)(?![\d.]\d)")
LINK_MD = re.compile(r"\[([^\]\n]*)\]\(([^)\s]+)\)(\{[^}\n]*\})?")


def ancla_de(cod):
    return cod.lower().replace("-", "_")


def asignar_anclas(raiz):
    """Pone un ancla en los títulos que son destino. Devuelve {alias de sección: ancla}."""
    usadas, alias = set(), {}

    def recorrer(n):
        for h in n.hijos:
            cod = COD_DESTINO.search(h.titulo)
            num = re.match(r"^(\d+(?:\.\d+)*)\.?\s", h.titulo)
            a = ancla_de(cod.group(1)) if cod else ("sec_" + num.group(1).replace(".", "_") if num else None)
            if a and a not in usadas:
                usadas.add(a)
                h.ancla = a
                if num:
                    alias["sec_" + num.group(1).replace(".", "_")] = a
            recorrer(h)
    recorrer(raiz)
    return alias


def enlazar(texto, alias):
    """Convierte las referencias a destinos de este texto en hipervínculos internos `[ref](#ancla)`."""
    lineas = texto.split("\n")
    # la fila que define cada objetivo lleva su ancla
    definidas = set()
    for i, l in enumerate(lineas):
        m = re.match(r"^\| (\*\*)?(OBJ-\d{2})(\*\*)? \|", l)
        if m and m.group(2) not in definidas:
            definidas.add(m.group(2))
            lineas[i] = l.replace(m.group(0), f"| {m.group(1) or ''}[{m.group(2)}]{{#{ancla_de(m.group(2))}}}{m.group(3) or ''} |", 1)
    presentes = set(re.findall(r"\{#([\w-]+)\}", "\n".join(lineas)))
    alias = {k: v for k, v in alias.items() if v in presentes}

    def destino(m):
        if m.group(1):
            a = ancla_de(m.group(1))
            return a if a in presentes else None
        return alias.get("sec_" + m.group(3).replace(".", "_"))

    def tramo(s):
        def uno(m):
            a = destino(m)
            if not a:
                return m.group(0)
            # «Documento 2, sección 3» es de otro documento: queda como texto
            if m.group(2) and re.search(r"Documento\s+[\d.]+\W{0,3}$", s[max(0, m.start() - 16):m.start()]):
                return m.group(0)
            return f"[{m.group(0)}](#{a})"
        return REF.sub(uno, s)

    fence = False
    for i, l in enumerate(lineas):
        if l.startswith("```"):
            fence = not fence
            continue
        if fence or re.match(r"^(#{1,6} |!\[|\*\*Figura \d|- Figura \d|<)", l):
            continue
        partes, ult = [], 0
        for m in LINK_MD.finditer(l):
            partes.append(tramo(l[ult:m.start()]))
            if m.group(3) or not m.group(2).startswith("#") or m.group(2)[1:] in presentes:
                partes.append(m.group(0))
            else:
                partes.append(m.group(1))       # enlace a un ancla que no está en el documento: texto
            ult = m.end()
        partes.append(tramo(l[ult:]))
        lineas[i] = "".join(partes)
    return "\n".join(lineas)


def emitir(n, nivel, out, permitidos=None):
    if permitidos is not None and nivel == 2 and sin_numero(n.titulo) not in permitidos:
        nivel = 3
    out.append("#" * min(nivel, 6) + " " + titulo_final(n.titulo) + (f" {{#{n.ancla}}}" if n.ancla else ""))
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
        anexo("Leyenda de Prioridad")
        figuras = sacar(raiz, "Índice de Figuras")
        pres = renombrar(sacar(raiz, "Presentación General"), "Presentación General")
        obj = renombrar(sacar(raiz, "Objetivos del Sistema"), "Objetivos del sistema")
        dcu = renombrar(sacar(raiz, "Diagrama de Casos de Uso del Sistema"), "Diagrama de Caso de Uso del Sistema")
        lista = renombrar(sacar(raiz, "Casos de Uso: lista e importancia"), "Casos de Usos")
        subs = renombrar(sacar(raiz, "Subsistemas del Proyecto"), "Subsistemas del Proyecto")
        pres.hijos += [obj, dcu, lista, subs]
        itera = renombrar(sacar(raiz, "Objetivos de la Iteración"), "Objetivos de la Iteración")
        info = renombrar(sacar(raiz, "Requisitos de Información"), "Requisitos de Información")
        func = renombrar(sacar(raiz, "Requisitos Funcionales — Casos de Uso"), "Requisitos de Funcionales")
        dsub = renombrar(sacar(func, "Diagramas de Casos de Uso por Subsistema"), "Diagrama de Casos de Usos")
        actores = renombrar(sacar(func, "Definición de Actores"), "Definición de Actores")
        cue = renombrar(sacar(func, "Casos de Uso del Sistema"), "Caso de Usos del Sistema")
        func.hijos = [dsub, actores, cue] + list(func.hijos)
        nf = renombrar(sacar(raiz, "Requisitos No Funcionales"), "Requisitos No funcionales")
        req = nuevo("Requisitos del Sistema", [info, func, nf])
        matriz = renombrar(sacar(raiz, "Matriz de Rastreabilidad Objetivos / Requisitos"), "Matriz de Rastreabilidad Objetivo/Requisitos")
        glos = renombrar(sacar(raiz, "Glosario de Términos"), "Glosario de Términos")
        return [figuras, pres, itera, req, matriz, glos], anexos
    if clave == "2":
        anexo("Índice de Figuras")
        mc = renombrar(sacar(raiz, "Modelo Conceptual"), "Modelo Conceptual")
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
        anexo("Índice de Figuras")
        reales = renombrar(sacar(raiz, "Casos de Uso Reales"), "Casos de Usos Reales")
        inter = renombrar(sacar(raiz, "Diagrama de Interacción"), "Diagrama de Interacción")
        sin_dsd = sacar(inter, "Casos sin diagrama de interacción")
        ops = buscar(inter, "Operaciones")
        ops.hijos = list(ops.hijos)
        inter.hijos = [ops, sin_dsd]
        clases = renombrar(sacar(raiz, "Diagrama de Clase"), "Diagrama de Clase")
        return [reales, inter, clases], anexos
    return None, anexos


def peso_linea(l):
    return sum(os.path.getsize(DOC + m) for m in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", l) if os.path.exists(DOC + m))


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
    md = desplegar(open(DOC + nombre_md, encoding="utf-8").read())   # el Word pone la imagen una sola vez
    titulo, campos, resto = partir(md)
    titulo = TITULOS_PORTADA.get(clave, titulo)
    # la plantilla lleva la Lista de Cambios antes del índice
    m = re.search(r"^## Lista de Cambios\n(.*?)(?=^## )", resto, re.S | re.M)
    cambios = ""
    if m:
        tabla = m.group(1)
        resto = resto[:m.start()] + resto[m.end():]
        filas = re.findall(r"^\| (\d+) \| ([^|]+?) \|", tabla, re.M)
        # si el .md ya trae la fila de la fecha de la entrega, no se agrega otra ni se sube la versión
        ya_tiene = filas[-1][1].strip() in (FECHA, FECHA_ISO)
        # la fila nueva va pegada a la última fila de la tabla (después suele venir un «---»)
        ult = [k for k in re.finditer(r"^\|.*\|[ \t]*$", tabla, re.M)][-1]
        nueva = "" if ya_tiene else f"\n| {int(filas[-1][0]) + 1} | {FECHA_ISO} | {CAMBIO} | {AUTOR} |"
        tabla = (tabla[:ult.end()] + nueva
                 + re.sub(r"^\s*-{3,}\s*$", "", tabla[ult.end():], flags=re.M).rstrip() + "\n\n")
        if clave in CON_LISTA_COMO_TITULO:
            cambios = "# Lista de Cambios\n" + tabla
        else:
            cambios = ("```{=openxml}\n" + p_xml("Lista de Cambios", 32, True, centrado=False, despues=200)
                       + "\n```\n" + tabla)
    ya_tiene = m is not None and ya_tiene
    campos = [(k, (v if ya_tiene else subir_version(v)) if k == "Versión" else FECHA if k == "Fecha" else v) for k, v in campos]
    # la plantilla del Documento 1 repite la portada antes de la parte de la iteración: el bloque citado del .md
    # («Documento de Requisitos del Sistema — Requisitos de la Iteración») pasa a ser una portada de página completa
    resto = re.sub(r"^> \*\*Documento de Requisitos del Sistema — Requisitos de la Iteración\*\*[ \t]*\n(?:>[^\n]*\n)*",
                   lambda _m: "```{=openxml}\n" + salto_pagina() + "\n```\n" + portada(titulo, campos) + "\n",
                   resto, flags=re.M)
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
        if ruta.startswith("http") or not os.path.exists(DOC + ruta):
            return mo.group(0)
        return imagen_md(DOC + ruta)

    resto = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)(?!\{)", imagen, resto)
    # <br> dentro de una celda: pandoc descarta el HTML y pega los renglones; va como salto de línea de Word
    resto = re.sub(r"^\|.*$", lambda m: re.sub(r"<br\s*/?>", "`<w:r><w:br/></w:r>`{=openxml}", m.group(0)),
                   resto, flags=re.M)
    resto = re.sub(r"@@FIN@@\s*(\*\*Figura \d+ — [^\n]*\*\*)", r"\1\n\n@@FIN@@", resto)
    # el título de la figura (y su línea de actor/operaciones) pasa a la página horizontal con ella: si no, queda
    # solo en una página vertical casi vacía
    resto = re.sub(r"(^#{1,6} [^\n]*\n(?:[ \t]*\n|(?![#|!`@<])[^\n]*\n){0,8}?)[ \t\n]*@@INI@@",
                   lambda m: "@@INI@@\n\n" + m.group(1), resto, flags=re.M)
    # dos figuras horizontales seguidas comparten la sección: si no, queda una página vertical en blanco entre ellas
    resto = re.sub(r"@@FIN@@(?:\s|<!--(?:(?!-->).)*-->)*@@INI@@", "\n\n", resto, flags=re.S)
    resto = resto.replace("@@INI@@", MARCA_INI.strip()).replace("@@FIN@@", MARCA_FIN.strip())
    raiz = parsear(resto)
    alias = asignar_anclas(raiz)
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
    resto = enlazar(resto, alias)
    final_horizontal = False
    sin_cola = re.sub(r"(?:\s|^-{3,}[ \t]*$|<!--(?:(?!-->).)*-->)*\Z", "", resto, flags=re.S | re.M)
    if sin_cola.endswith(MARCA_FIN.strip()):
        resto, final_horizontal = sin_cola[:-len(MARCA_FIN.strip())], True
    if total > 1:
        titulo += f" (Parte {parte} de {total})"
    cuerpo = (portada(titulo, campos) + "\n" + cambios + "\n"
              + "```{=openxml}\n" + salto_pagina() + p_xml("Índice", 32, True, centrado=False, despues=200) + "<w:p><w:r><w:t>@@TOC@@</w:t></w:r></w:p>\n```\n\n"
              + resto)
    return cuerpo, contador, dict(campos).get("Versión", ""), final_horizontal


# ---------- reference-doc ----------
def reference(plantilla_doc, destino):
    """pandoc reference.docx con página y tipografía de la plantilla de la cátedra."""
    tmp = tempfile.mkdtemp()
    sh(["textutil", "-convert", "docx", "-output", tmp + "/p.docx", D + "catedra/.catedra-ref/" + plantilla_doc])
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
                # castellano: si no, Word marca todo el texto como error de ortografía en inglés
                s = re.sub(r'(<w:lang w:val=")[^"]*', r"\1es-AR", s)
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
    """Como el pie de la plantilla: proyecto y equipo (sin iteración, por decisión de nahue del 01/11/2026)."""
    tab = '<w:r><w:tab/></w:r>'
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}><w:p><w:pPr>'
            '<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="808080"/></w:pBdr>'
            '<w:tabs><w:tab w:val="center" w:pos="4500"/><w:tab w:val="right" w:pos="9000"/></w:tabs></w:pPr>'
            + _run("SPLG – Sistema de Pedidos y Logística de Garrafas de Gas") + tab + tab
            + _run("Equipo: " + AUTOR) + '</w:p></w:hdr>')


def pie_xml(version):
    campo = ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
             '<w:r><w:fldChar w:fldCharType="separate"/></w:r>' + _run("1") + '<w:r><w:fldChar w:fldCharType="end"/></w:r>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}><w:p><w:pPr>'
            '<w:tabs><w:tab w:val="right" w:pos="9000"/></w:tabs></w:pPr>'
            + _run("Versión: " + version) + '<w:r><w:tab/></w:r>' + _run("Página ") + campo + '</w:p></w:ftr>')


def con_encabezado(zin, doc2, version, titulo):
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
    # la portada (primera página de la primera sección) va sin encabezado ni pie
    m = re.search(r"<w:sectPr[^>]*>.*?</w:sectPr>", doc2, re.S)
    sp = m.group(0)
    sp2 = re.sub(r"(<w:docGrid|</w:sectPr>)", r"<w:titlePg/>\1", sp, count=1)
    doc2 = doc2[:m.start()] + sp2 + doc2[m.end():]
    if 'xmlns:r=' not in doc2[:2000]:
        doc2 = doc2.replace("<w:document ", '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
    ajustes = zin.read("word/settings.xml").decode("utf8")
    # sin updateFields: Word preguntaría al abrir si actualiza los campos. Los índices ya traen su resultado
    # calculado (con número de página) y se actualizan con F9 si hace falta.
    ajustes = re.sub(r"<w:updateFields[^>]*/>", "", ajustes)
    ajustes = re.sub(r'(<w:themeFontLang w:val=")[^"]*', r"\1es-AR", ajustes)
    core = zin.read("docProps/core.xml").decode("utf8")
    titulo = titulo.replace("Analisis", "Análisis").replace("Planificacion", "Planificación")   # el nombre de archivo va sin tilde
    esc = titulo.replace("&", "&amp;").replace("<", "&lt;")
    core = core.replace("<dc:title></dc:title>", f"<dc:title>SPLG – {esc}</dc:title>").replace(
        "<dc:creator></dc:creator>", f"<dc:creator>{AUTOR}</dc:creator>")
    return {"[Content_Types].xml": ct.encode("utf8"), "word/_rels/document.xml.rels": rels.encode("utf8"),
            "word/settings.xml": ajustes.encode("utf8"), "docProps/core.xml": core.encode("utf8"),
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


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _campo(instr, resultado_runs):
    """Un campo de Word completo (begin, instrucción, separate, resultado guardado, end), en runs."""
    return ('<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r><w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>' + resultado_runs
            + '<w:r><w:fldChar w:fldCharType="end"/></w:r>')


def _entrada_indice(texto, ancla, sangria, rpr):
    """Renglón de un índice como lo escribe Word: hipervínculo al marcador, tabulación con puntos y el número de
    página en un campo PAGEREF. El número se guarda como @@PG:ancla@@ y lo completa `numerar_paginas`."""
    pag = _campo(f"PAGEREF {ancla} \\h", f'<w:r><w:rPr>{rpr}</w:rPr><w:t>@@PG:{ancla}@@</w:t></w:r>')
    return (f'<w:p><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9000"/></w:tabs>'
            f'<w:spacing w:before="0" w:after="20"/><w:ind w:left="{sangria}"/></w:pPr>'
            f'<w:hyperlink w:anchor="{ancla}" w:history="1"><w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{_esc(texto)}</w:t></w:r>'
            f'<w:r><w:rPr>{rpr}</w:rPr><w:tab/></w:r>{pag}</w:hyperlink></w:p>')


def _envolver_en_campo(filas, instr):
    """Pone los renglones dentro de un campo TOC (Word lo puede actualizar con F9 y conserva el formato)."""
    if not filas:
        return filas
    inicio = ('<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
              f'<w:r><w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'
              '<w:r><w:fldChar w:fldCharType="separate"/></w:r>')
    filas[0] = filas[0].replace("</w:pPr>", "</w:pPr>" + inicio, 1)
    filas[-1] = filas[-1][:-len("</w:p>")] + '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
    return filas


def indice_estatico(doc):
    """Índice general: un campo TOC con hipervínculo y número de página por cada título de nivel 1 a 3 (Título 1 a
    3), cada uno con su marcador. El resultado del campo queda guardado, así Word lo muestra sin actualizar campos."""
    entradas, n = [], [0]

    def marcar(m):
        p = m.group(0)
        est = re.search(r'<w:pStyle w:val="Heading([123])"\s*/>', p)
        if not est:
            return p
        n[0] += 1
        nombre = f"splg_h{n[0]}"
        texto = re.sub(r"<[^>]+>", "", p).strip()
        texto = texto.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        entradas.append((int(est.group(1)), texto, nombre))
        p = re.sub(r"(</w:pPr>)", rf'\1<w:bookmarkStart w:id="{9000 + n[0]}" w:name="{nombre}"/>', p, count=1)
        return p.replace("</w:p>", f'<w:bookmarkEnd w:id="{9000 + n[0]}"/></w:p>')

    doc = re.sub(r"<w:p>(?:(?!</w:p>).)*?</w:p>", marcar, doc, flags=re.S)
    filas = []
    for nivel, texto, nombre in entradas:
        rpr = ('<w:rFonts w:ascii="Verdana" w:hAnsi="Verdana"/>' + ("<w:b/>" if nivel == 1 else "")
               + f'<w:color w:val="1F3864"/><w:sz w:val="{20 if nivel == 1 else 18 if nivel == 2 else 16}"/>')
        filas.append(_entrada_indice(texto, nombre, {1: 0, 2: 400, 3: 800}[nivel], rpr))
    filas = _envolver_en_campo(filas, 'TOC \\o "1-3" \\h \\z \\u')
    marca = re.search(r"<w:p>(?:(?!</w:p>).)*?@@TOC@@.*?</w:p>", doc, re.S)
    if not marca:
        sys.exit("no encuentro la marca del índice")
    if filas:
        filas[-1] = filas[-1][:-len("</w:p>")] + '<w:r><w:br w:type="page"/></w:r></w:p>'
        return doc[:marca.start()] + "".join(filas) + doc[marca.end():]
    return doc[:marca.start()] + salto_pagina() + doc[marca.end():]


def figuras_e_indice(doc):
    """Cada pie «Figura N — …» lleva un marcador (splg_fig_N) y su número en un campo SEQ Figura; el «Índice de
    Figuras» pasa a ser un campo TOC \\c "Figura" con hipervínculo y número de página por figura."""
    figs = []

    def pie(m):
        p = m.group(0)
        if "<w:drawing" in p or "<w:numPr" in p:      # la imagen, o un renglón del índice escrito en el .md
            return p
        texto = re.sub(r"<[^>]+>", "", p)
        mt = re.match(r"\s*Figura (\d+) — ", texto)
        ts = re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p)
        if not mt or not ts or not ts[0].startswith(f"Figura {mt.group(1)} — "):
            return p
        num = mt.group(1)
        nombre = f"splg_fig_{num}"
        figs.append((num, texto.strip().replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"), nombre))
        run = re.search(r"<w:r>(?:(?!</w:r>).)*?<w:t(?: [^>]*)?>Figura \d+ — ", p, re.S)
        rpr = re.search(r"<w:rPr>.*?</w:rPr>", run.group(0), re.S) if run else None
        rpr = rpr.group(0) if rpr else ""
        primero = re.search(r"<w:t(?: [^>]*)?>(Figura \d+ — )", p)
        # «Figura » + SEQ + « — …» (el resto del primer texto sigue en su run)
        seq = (f'<w:r>{rpr}<w:t xml:space="preserve">Figura </w:t></w:r>'
               + _campo("SEQ Figura \\* ARABIC", f'<w:r>{rpr}<w:t>{num}</w:t></w:r>'))
        ini_run = run.start()
        p = p[:ini_run] + seq + p[ini_run:primero.start(1)] + p[primero.start(1):].replace(f"Figura {num} — ", " — ", 1)
        p = re.sub(r"(<w:pPr>.*?</w:pPr>|<w:p>)", lambda x: x.group(0) + f'<w:bookmarkStart w:id="{20000 + int(num)}" w:name="{nombre}"/>', p, count=1, flags=re.S)
        return p.replace("</w:p>", f'<w:bookmarkEnd w:id="{20000 + int(num)}"/></w:p>')

    doc = re.sub(r"<w:p>(?:(?!</w:p>).)*?</w:p>", pie, doc, flags=re.S)
    # la sección «Índice de Figuras»: del título al título siguiente
    tit = None
    for m in re.finditer(r"<w:p>(?:(?!</w:p>).)*?</w:p>", doc, re.S):
        if re.search(r'<w:pStyle w:val="Heading\d"', m.group(0)) and re.sub(r"<[^>]+>", "", m.group(0)).strip().endswith("Índice de Figuras"):
            tit = m
            break
    if not tit or not figs:
        return doc
    sig = re.search(r'<w:p>(?:(?!</w:p>).)*?<w:pStyle w:val="Heading\d"', doc[tit.end():], re.S)
    fin = tit.end() + (sig.start() if sig else 0)
    rpr = '<w:rFonts w:ascii="Verdana" w:hAnsi="Verdana"/><w:sz w:val="18"/>'
    filas = _envolver_en_campo([_entrada_indice(tx, nm, 0, rpr) for _, tx, nm in figs], 'TOC \\h \\z \\c "Figura"')
    return doc[:tit.end()] + "".join(filas) + doc[fin:]


def _paginas_pdf(pdf):
    """{marcador: número de página} de los destinos con nombre que LibreOffice escribe en el PDF."""
    d = open(pdf, "rb").read()
    objs = {int(m.group(1)): m.group(2) for m in re.finditer(rb"\n(\d+) 0 obj\s*(.*?)endobj", d, re.S)}
    raiz = int(re.search(rb"/Type\s*/Catalog[^>]*?/Pages (\d+) 0 R", d, re.S).group(1))
    orden = []

    def hojas(k):
        o = objs[k]
        kids = re.search(rb"/Kids\s*\[([^\]]*)\]", o)
        if kids and b"/Type/Pages" in o.replace(b" ", b""):
            for x in re.findall(rb"(\d+) 0 R", kids.group(1)):
                hojas(int(x))
        else:
            orden.append(k)
    hojas(raiz)
    pagina = {k: i + 1 for i, k in enumerate(orden)}
    dests = re.search(rb"/Dests (\d+) 0 R", d)
    out = {}
    if dests:
        for m in re.finditer(rb"/([^\s/\[]+)\s*\[(\d+) 0 R", objs[int(dests.group(1))]):
            nombre = re.sub(r"#([0-9A-Fa-f]{2})", lambda x: chr(int(x.group(1), 16)), m.group(1).decode("latin1"))
            nombre = nombre.replace("5F", "_")
            out[nombre] = pagina.get(int(m.group(2)))
    return out


def numerar_paginas(doc, armar_docx):
    """Completa el número de página de cada renglón de los índices. Arma el .docx con un número provisorio, lo
    pagina LibreOffice y se lee la página de cada marcador del PDF."""
    marcas = sorted(set(re.findall(r"@@PG:([\w]+)@@", doc)))
    if not marcas:
        return doc
    tmp = tempfile.mkdtemp()
    prueba = os.path.join(tmp, "paginar.docx")
    armar_docx(re.sub(r"@@PG:[\w]+@@", "000", doc), prueba)
    filtro = 'pdf:writer_pdf_Export:{"ExportBookmarksToPDFDestination":{"type":"boolean","value":"true"}}'
    subprocess.run(["soffice", "--headless", "--convert-to", filtro, "--outdir", tmp, prueba],
                   check=True, capture_output=True)
    pags = _paginas_pdf(os.path.join(tmp, "paginar.pdf"))
    shutil.rmtree(tmp)
    faltan = [m for m in marcas if not pags.get(m)]
    if faltan:
        print(f"  aviso: {len(faltan)} renglones de índice sin página (p. ej. {faltan[:3]})")
    return re.sub(r"@@PG:([\w]+)@@", lambda m: str(pags.get(m.group(1)) or ""), doc)


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
    cuerpo, cont, version, final_horizontal = preparar_md(clave, nombre_md, parte, total)
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
        "--lua-filter", filtro, "--resource-path", DOC, "--columns=100"], cwd=DOC)
    if not os.environ.get("SPLG_DOCX_DEBUG"):
        # el .md intermedio lleva rutas absolutas a la caché: si queda, verificar-links.py lo cuenta como roto
        os.unlink(mdi)
    zin = zipfile.ZipFile(crudo)
    doc2 = zin.read("word/document.xml").decode("utf8")
    doc2 = tamanos_de_imagen(doc2)
    doc2 = indice_estatico(doc2)
    doc2 = figuras_e_indice(doc2)
    doc2 = encabezados_de_tabla(doc2)
    if final_horizontal:
        # la última sección (la del cuerpo) toma la página horizontal de la figura con la que termina el documento
        i = doc2.rfind("<w:sectPr")
        ult = doc2[i:]
        ult = re.sub(r"<w:pgSz[^>]*/>", re.search(r"<w:pgSz[^>]*/>", SECT_H).group(0), ult, count=1)
        ult = re.sub(r"<w:pgMar[^>]*/>", re.search(r"<w:pgMar[^>]*/>", SECT_H).group(0), ult, count=1)
        doc2 = doc2[:i] + ult
    # las tablas ocupan el ancho de la página (pandoc las deja al ancho del contenido)
    doc2 = re.sub(r"<w:tblW [^>]*/>", '<w:tblW w:type="pct" w:w="5000"/>', doc2)
    doc2 = re.sub(r"<w:tbl>.*?</w:tbl>", columnas_al_ancho, doc2, flags=re.S)
    def armar_docx(doc_xml, destino):
        # se reabre el crudo en cada armado: writestr(ZipInfo) altera los ZipInfo del archivo de origen
        zin = zipfile.ZipFile(crudo)
        nuevos = con_encabezado(zin, doc_xml, version, titulo)
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zout:
            for nombre_p, data in nuevos.items():
                if nombre_p.startswith("word/header") or nombre_p.startswith("word/footer"):
                    zout.writestr(nombre_p, data)
            for it in zin.infolist():
                data = zin.read(it.filename)
                if it.filename in nuevos:
                    data = nuevos[it.filename]
                zout.writestr(it, data)

    # los índices llevan el número de página calculado: Word los muestra completos sin actualizar campos
    doc2 = numerar_paginas(doc2, armar_docx)
    armar_docx(doc2, salida)
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
