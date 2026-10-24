# -*- coding: utf-8 -*-
"""Relaciones «include» y «extend» entre casos de uso: la única fuente.

La usan el generador de los diagramas (generar-uml.py), el verificador (verificar-conformidad.py) y los
verificadores de herramientas/. La tabla 7.7 del Documento 1 y la sección «Puntos de extensión» de cada
CUE salen de acá: cada «extend» tiene un identificador PE-n único en toda la documentación.
"""

# Relaciones entre casos de uso. Dicen que una operacion necesita de otra —tipicamente,
# escribir sobre algo exige leerlo antes—.
INCLUYE = {
  # Solo comportamiento obligatorio compartido: el caso incluido lo ejecuta siempre el caso base.
  # Que una operación parta del listado o de la ficha del registro es navegación, no un «include».
  "SS-01": [("CU-002", "CU-082")],
  "SS-02": [("CU-147", "CU-121"), ("CU-005", "CU-169"), ("CU-008", "CU-169"), ("CU-009", "CU-169"), ("CU-010", "CU-169"), ("CU-147", "CU-169")],
  "SS-05": [],
  "SS-07": [("CU-105", "CU-139"), ("CU-142", "CU-139"), ("CU-155", "CU-159"), ("CU-157", "CU-160")],
  "SS-08": [("CU-038", "CU-213"), ("CU-212", "CU-250"), ("CU-213", "CU-250"), ("CU-296", "CU-250"), ("CU-220", "CU-250"), ("CU-222", "CU-250"), ("CU-219", "CU-250"), ("CU-274", "CU-250"), ("CU-276", "CU-250"), ("CU-278", "CU-220")],
  "SS-09": [],
  "SS-10": [],
  "SS-11": [],
  "SS-12": [],
  "SS-13": [("CU-135", "CU-133"), ("CU-134", "CU-133")],
  "SS-16": [],
  "SS-03": [],
  "SS-19": [("CU-188", "CU-187")],
  "SS-21": [("CU-233", "CU-228"), ("CU-237", "CU-228"), ("CU-243", "CU-309")],
  "SS-20": [],
}

# Inclusiones entre subsistemas distintos: el caso incluido vive en otro
# subsistema y se dibuja fuera del limite del que lo incluye, con su codigo.
INCLUYE_EXTERNO = [("CU-031","CU-082"), ("CU-086","CU-082"), ("CU-087","CU-082"),
                   ("CU-174","CU-159"), ("CU-175","CU-160"),
                   ("CU-012","CU-246"), ("CU-013","CU-246"), ("CU-015","CU-246"),
                   ("CU-217","CU-250"), ("CU-280","CU-250"), ("CU-012","CU-248"), ("CU-013","CU-248"), ("CU-015","CU-248"), ("CU-080","CU-248"),
                   ("CU-236","CU-005"), ("CU-020","CU-220"), ("CU-079","CU-220"),
                   ("CU-012","CU-169"), ("CU-015","CU-169"), ("CU-018","CU-169"), ("CU-020","CU-169"), ("CU-072","CU-169"),
                   ("CU-075","CU-169"), ("CU-077","CU-169"), ("CU-079","CU-169")]

# extension -> base, con su punto de extension. La flecha de <<extend>> va
# SIEMPRE desde el caso opcional hacia el caso base, al reves que <<include>>.
EXTIENDE = {
  "SS-02": [("CU-148","CU-005","el cliente puede elegir la modalidad express"),
            ("CU-143","CU-002","el cliente declara cuánto gas consume por mes")],
  "SS-03": [],
  "SS-04": [],
  "SS-05": [("CU-174","CU-023","el cliente adjunta evidencia fotográfica")],
  "SS-14": [("CU-168","CU-008","el pedido cancelado tiene un pago aprobado por una pasarela"),
            ("CU-168","CU-010","el pedido cancelado tiene un pago aprobado por una pasarela"),
            ("CU-168","CU-149","el pedido express pasa a reparto común y ya estaba pagado en linea")],
  "SS-09": [("CU-044","CU-005","el cliente quiere agendar la entrega en una franja horaria")],
  "SS-13": [("CU-135","CU-068","el envase que se va a asignar está vencido")],
  "SS-16": [("CU-130","CU-129","la ficha se abre desde un pedido, un reclamo o una calificación y hay que ubicar al cliente por su cuenta de usuario")],
  "SS-19": [("CU-177","CU-031","el chofer que se registra todavía no tiene legajo")],
  "SS-21": [("CU-228","CU-227","el arqueo da un sobrante"), ("CU-309","CU-227","el arqueo da un faltante")],
}


def extensiones():
    """[(extension, base, condicion)] de todos los subsistemas, ordenadas por base y por extension."""
    todas = [x for v in EXTIENDE.values() for x in v]
    return sorted(todas, key=lambda x: (x[1], x[0]))


def pe_id(extension, base):
    """Identificador global del punto de extension: PE-01, PE-02..., el mismo en los diagramas y en los CUE."""
    for i, (e, b, _) in enumerate(extensiones(), 1):
        if (e, b) == (extension, base):
            return f"PE-{i:02d}"
    raise KeyError((extension, base))
