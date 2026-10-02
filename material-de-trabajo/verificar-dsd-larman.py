#!/usr/bin/env python3
"""Verifica los diagramas de interacción de diseño (DSD) en estilo Larman.

    python3 material-de-trabajo/verificar-dsd-larman.py              informa lo que falta, sin fallar por eso
    python3 material-de-trabajo/verificar-dsd-larman.py --estricto   además falla por cada operación sin DSD
    python3 material-de-trabajo/verificar-dsd-larman.py DSD_CU-025_resolverReclamo.mmd   sólo ese

Las reglas están en `GUIA-DSD-LARMAN.md` §9 y en `dsd_larman.py`. Un DSD ya rehecho que
rompe una regla falla siempre; lo que todavía no se rehízo sólo se informa hasta que se pasa
`--estricto` (o `DSD_ESTRICTO=1`), que es lo que se activa cuando se cierra la reescritura.
Sale 0 si no hay errores, 1 si los hay.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dsd_larman

args = sys.argv[1:]
estricto = "--estricto" in args or os.environ.get("DSD_ESTRICTO") == "1"
solo = {a for a in args if not a.startswith("--")} or None
errores, pendientes, hechos = dsd_larman.verificar(estricto=estricto, solo=solo)
print(f"DSD en estilo Larman: {len(hechos)} · operaciones del catálogo sin DSD: {len(pendientes)}")
for a in dsd_larman.AVISOS:
    print("  aviso:", a)
for e in errores:
    print("  ✗", e)
if pendientes and not estricto:
    print(f"  pendientes (no fallan hasta --estricto): {', '.join(f'{c} {n}' for c, n in pendientes[:4])}"
          + (" …" if len(pendientes) > 4 else ""))
sys.exit(1 if errores else 0)
