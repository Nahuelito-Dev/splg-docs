# -*- coding: utf-8 -*-
"""Estilo Visual Paradigm de los diagramas del repositorio, en un solo lugar.

Lo usan los generadores que dibujan SVG propio (uml_lamina.py), el de draw.io y el tema de
Mermaid; los diagramas PlantUML lo toman de `diagramas/estilo-vp.iuml` (los mismos colores).
Fondo blanco, sin sombras, Arial de 10 a 11 pt, relleno celeste y borde azul oscuro con línea fina.
"""
FUENTE = "Arial, Helvetica, sans-serif"
FONDO = "#FFFFFF"
RELLENO = "#C6DAF0"
RELLENO_CLARO = "#DCE6F2"
BORDE = "#3C5F8F"
TINTA = "#1F3A5F"          # flechas, texto y líneas
SUAVE = "#6B7683"          # referencias a otras láminas
PLAN_RELLENO = "#F6E4E1"   # caso planificado
PLAN_BORDE = "#9C4436"
GROSOR = 1.0

# Mermaid (secuencia): cabeceras de lifeline y barras de activación celestes, mensajes con flecha llena
MERMAID = {
    "theme": "base",
    "themeVariables": {
        "fontFamily": "Arial, Helvetica, sans-serif", "fontSize": "12px",
        "background": FONDO, "primaryColor": RELLENO, "primaryBorderColor": BORDE, "primaryTextColor": "#000000",
        "lineColor": TINTA, "signalColor": TINTA, "signalTextColor": "#000000",
        "actorBkg": RELLENO, "actorBorder": BORDE, "actorTextColor": "#000000", "actorLineColor": BORDE,
        "activationBkgColor": RELLENO, "activationBorderColor": BORDE,
        "labelBoxBkgColor": RELLENO_CLARO, "labelBoxBorderColor": BORDE, "labelTextColor": "#000000",
        "loopTextColor": "#000000", "noteBkgColor": "#FFFFFF", "noteBorderColor": BORDE, "noteTextColor": "#000000",
        "sequenceNumberColor": "#FFFFFF",
    },
    "sequence": {"mirrorActors": False, "showSequenceNumbers": False},
}
