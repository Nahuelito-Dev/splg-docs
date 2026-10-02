# -*- coding: utf-8 -*-
"""Los colores del sitio y de los diagramas, en un solo lugar.

Estaban escritos dos veces, una en el generador de diagramas y otra en la hoja de
estilos, y el mismo subsistema salia de un color en la lamina y de otro en la pagina.
El orden de las listas es el de los codigos SS-01 a SS-18.
"""

# un tinte de fondo y un borde por subsistema
TINTE = ["#E7F0F6", "#E9F4EA", "#F5ECF7", "#FBF2DE", "#FAE8E3", "#E4F2F1",
         "#F0EEF9", "#EFF6E2", "#FDEFE6", "#E6EEF7", "#F7ECEF", "#EDF5F9",
         "#F3F1E4", "#E9EFE6", "#F8EDF3", "#E8F1EC", "#F5F0E8", "#ECEDF6"]
BORDE = ["#3C6E8F", "#3F7A50", "#7B4B8A", "#8A7326", "#9C5A46", "#3E7C79",
         "#5A5896", "#5E7A3A", "#A26A45", "#44608B", "#8E5566", "#4A7488",
         "#7A7340", "#4E6B4A", "#8A5674", "#4B7560", "#7C6B4C", "#5B5F87"]

# un color de linea por actor, para poder seguir cada asociacion en el diagrama grande
COLOR_ACT = {"01": "#1F6F8B", "02": "#2E7D46", "03": "#8C4A9E",
             "04": "#8A6D1F", "05": "#B4432B",
             "06": "#0E7C86", "07": "#C98A00", "08": "#5F6B7A",
             "09": "#4F6D3A"}

def indice(codigo):
    """SS-07 -> 6. Cae en cero si el codigo no tiene forma de subsistema."""
    try:
        return (int(str(codigo).split("-")[1][:2]) - 1) % len(TINTE)
    except (IndexError, ValueError):
        return 0

def tinte(codigo): return TINTE[indice(codigo)]
def borde(codigo): return BORDE[indice(codigo)]

def css_subsistemas(codigos):
    """Una regla por subsistema, para que la marca del sitio use el mismo color
    que la caja del diagrama."""
    return "\n".join(
        f'.marca-ss[data-ss="{c}"]{{background:{tinte(c)};border-color:{borde(c)};color:{borde(c)}}}'
        for c in sorted(codigos))
