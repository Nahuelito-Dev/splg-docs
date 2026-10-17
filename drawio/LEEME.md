# Diagramas en draw.io

Los modelos de SPLG como archivos de draw.io, con cada relación dibujada como una arista conectada a sus dos
elementos (si se mueve una tabla o una clase, la línea la sigue). Los genera `generar-drawio.py`; no se editan a mano.

| Archivo | Qué es | Origen |
|---|---|---|
| `SPLG-MC.drawio` | Modelo conceptual: conceptos con atributos, asociaciones con nombre y multiplicidades en los dos extremos, composición, generalización y la clase de asociación | `modelo_conceptual.py` |
| `SPLG-DER.drawio` | DER conceptual: una entidad por concepto con tabla, con el vocabulario del modelo conceptual y las relaciones en pata de gallo | `diagramas/base-de-datos/SPLG-modelo.json` |
| `SPLG-DBD.drawio` | Diagrama de base de datos físico: las 63 tablas de la base con columnas, tipos, claves, únicos e índices, y cada una de las 150 claves foráneas como una arista de la columna FK a la clave primaria destino | `diagramas/base-de-datos/SPLG-modelo.json` (leído de la base) |
| `SPLG-DC.drawio` | Diagrama de clases de diseño: 299 clases con atributos y operaciones, asociaciones con navegabilidad y multiplicidades, composición, agregación, generalización y dependencias | `material-de-trabajo/dc_larman.py` (derivado de los DSD) |

Cada archivo tiene **una sola página** con el diagrama completo, sin módulos ni recuadros de agrupación: los
elementos van sueltos y graphviz los acomoda a partir de sus relaciones, de modo que los relacionados quedan cerca.

## Cómo se abren

- **draw.io de escritorio** (`/Applications/draw.io.app`): Archivo → Abrir, o `open -a draw.io drawio/SPLG-DBD.drawio`.
- **Web**: https://app.diagrams.net → Abrir desde → Dispositivo.

Al seleccionar una arista se ven sus dos extremos conectados.

## Exportar a imagen

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png --scale 2 -o salida.png drawio/SPLG-DBD.drawio
```

## Regenerar y verificar

```bash
python3 generar-drawio.py      # reescribe los cuatro .drawio
python3 verificar-drawio.py    # 0 relaciones faltantes y 0 aristas sueltas, contra la base, el MC, el DER y el DC
```

Los `.drawio` se regeneran solo a mano con `generar-drawio.py` (el diagrama de clases tarda unos minutos); `generar-sitio.py` no los regenera y avisa si están desactualizados. Hace falta graphviz (`dot`, `fdp`): sin él, `generar-drawio.py` termina con error.
