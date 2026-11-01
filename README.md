# SPLG — Documentación

Sistema de Pedidos y Logística de Garrafas de Gas · Proceso Unificado · FCEQyN – UNaM

---

## ¿Qué necesitás?

| Si querés… | Abrí |
|---|---|
| **Ver un caso de uso** (cualquiera, del CU-001 al CU-348) con todo lo que tiene | **`documentos/Casos-de-Uso.md`** |
| **Entregar a la cátedra** | Los cinco documentos numerados de `documentos/` |
| **Subir los documentos a Drive** | `catedra/drive/` — ya están en HTML |
| **Abrir los modelos en draw.io** (conceptual, DER, base de datos y clases) | `modelos/drawio/` — ver `modelos/drawio/LEEME.md` |
| **Ver la base de datos** (SQL, diccionario, DER por módulo) | `modelos/base-de-datos/` — ver su `LEEME.md` |
| **Poner una imagen en un documento** | `documentos/INDICE-IMAGENES.md` te dice cuál va dónde |
| **Saber qué le falta al sistema** | `documentos/3-Diseño.md` §10 (pendientes de implementación) |
| **Seguimiento interno de las features nuevas (F1…FN, estado y % de avance; no va al sitio de la cátedra)** | **`FEATURES-NEW.md`** |
| **Entender cómo está hecho el código** (backend, Postman, setup) | `sistema/` — ver `sistema/README.md` |
| **Ver las pantallas reales** del panel y de las apps | `capturas/` |
| **Ver el sitio** | `sitio/` (se publica en https://splg-atlas.netlify.app con `./publicar.sh`; la v1 congelada queda en `/v1/` y el selector de la cabecera cambia de versión — config en `sitio/versiones.json`) |

Todo lo demás está en `catedra/material-de-trabajo/` y no hace falta para entregar.

## Cómo está organizado

```
splg-docs/
├─ README.md · VERSION · AGENTS.md · CLAUDE.md · publicar.sh
├─ documentos/    los cinco documentos de la cátedra, Casos-de-Uso, INDICE-IMAGENES y las guías
├─ modelos/
│  ├─ drawio/         MC, DER, DBD y DC en draw.io
│  └─ base-de-datos/  SQL, SPLG-modelo.json, diccionario y DER por módulo
├─ diagramas/     DSS, DSD, CU y pantallas (.mmd, PNG, SVG, PlantUML)
├─ sistema/       documentación técnica del código (back, Postman, setup)
├─ capturas/      capturas reales del panel y de las apps
├─ catedra/       drive/, entregables/, .catedra-ref/ y material-de-trabajo/
├─ sitio/         generador y archivos del sitio publicado
└─ herramientas/  los scripts de generación y verificación
```

Los links de `documentos/*.md` a las imágenes son relativos a esa carpeta (`../diagramas/png/…`).

---

## Los cinco documentos de la cátedra

| | Documento | Qué lleva |
|---|---|---|
| **0** | `0-Plan_Del_Proyecto.md` | Fases, hitos, cronograma, actores y los 338 casos de uso de alto nivel |
| **0.1** | `0.1-Planificacion_Iteraciones.md` | Qué se hace en cada iteración |
| **1** | `1-Requisitos.md` | Objetivos, subsistemas y los 338 casos de uso expandidos |
| **2** | `2-Analisis.md` | Modelo conceptual de los 21 casos esenciales, diagramas de secuencia de los diez casos con interacción del actor, contratos de sus operaciones y glosario |
| **3** | `3-Diseño.md` | Arquitectura, casos de uso reales, los diagramas de interacción y los módulos inteligentes |

## El documento de consulta

**`Casos-de-Uso.md`** tiene los **338 casos, del CU-001 al CU-348, sin los diez retirados**, cada uno con sus
cuatro artefactos: alto nivel (CUA), expandido (CUE), diagrama de secuencia del sistema
(DSS) y diagrama de interacción de diseño (DSD).

Los casos también están dentro de los documentos 0, 1, 2 y 3 porque **cada plantilla de
la cátedra exige su artefacto ahí**. Este archivo los reúne para no saltar entre cuatro.

## Los comandos

```bash
python3 herramientas/verificar-conformidad.py   # ¿cumple las plantillas? (33 chequeos)
python3 herramientas/verificar-links.py         # ¿algún link roto en los .md y los .html?
python3 herramientas/incrustar-imagenes-cu.py --aplicar  # cada DSS/DSD de los .md como imagen (PNG) con su Mermaid plegado debajo
python3 herramientas/generar-tabla-implementacion.py  # copia la tabla de implementación (Casos §8) al Documento 3 §4.25
python3 herramientas/generar-html-drive.py      # regenera catedra/drive/*.html
python3 herramientas/generar-docx-catedra.py    # Documentos de la cátedra en Word (.docx) -> catedra/entregables/catedra-docx/ y ~/Desktop/SPLG-Documentacion-Catedra/
python3 sitio/generar-sitio.py                  # regenera sitio/splg-documentacion.html
python3 herramientas/generar-drawio.py          # regenera modelos/drawio/*.drawio (MC, DER, base de datos y clases)
```

## Con qué está hecha

| | |
|---|---|
| **Proceso Unificado** | La metodología que exige la cátedra |
| **Markdown** | Los seis documentos de `documentos/`, versionados como texto plano |
| **Mermaid** | Los 711 diagramas de secuencia, interacción, flujo y estados |
| **PlantUML** | Los diagramas de estados, actividad, componentes, despliegue y cronograma (`diagramas/uml/UML_*.puml`). Los de casos de uso los dibuja `generar-uml.py` directamente en SVG |
| **Python** | Verificación de conformidad y generación de los entregables |
| **Git** | Historia completa de cada cambio |
| **Netlify** | Publicación del atlas |

Los diagramas se escriben como código junto al texto que documentan, así que se versionan
igual que el resto y no hay que redibujarlos a mano cuando algo cambia.

El mapa de archivos está en `documentos/GUIA-DEL-REPOSITORIO.md`.
