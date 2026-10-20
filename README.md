# SPLG — Documentación

Sistema de Pedidos y Logística de Garrafas de Gas · Proceso Unificado · FCEQyN – UNaM

---

## ¿Qué necesitás?

| Si querés… | Abrí |
|---|---|
| **Ver un caso de uso** (cualquiera, del CU-001 al CU-348) con todo lo que tiene | **`Casos-de-Uso.md`** |
| **Entregar a la cátedra** | Los cinco documentos numerados de esta carpeta |
| **Subir los documentos a Drive** | `drive/` — ya están en HTML |
| **Abrir los modelos en draw.io** (conceptual, DER, base de datos y clases) | `drawio/` — ver `drawio/LEEME.md` |
| **Poner una imagen en un documento** | `INDICE-IMAGENES.md` te dice cuál va dónde |
| **Saber qué le falta al sistema** | `3-Diseño.md` §10 (pendientes de implementación) |

Todo lo demás está en `material-de-trabajo/` y no hace falta para entregar.

---

## Los cinco documentos de la cátedra

| | Documento | Qué lleva |
|---|---|---|
| **0** | `0-Plan_Del_Proyecto.md` | Fases, hitos, cronograma, actores y los 338 casos de uso de alto nivel |
| **0.1** | `0.1-Planificacion_Iteraciones.md` | Qué se hace en cada iteración |
| **1** | `1-Requisitos.md` | Objetivos, subsistemas y los 338 casos de uso expandidos |
| **2** | `2-Analisis.md` | Modelo conceptual, los 338 diagramas de secuencia, el catálogo de operaciones y sus contratos |
| **3** | `3-Diseño.md` | Arquitectura, casos de uso reales, los diagramas de interacción y los módulos inteligentes |

## El documento de consulta

**`Casos-de-Uso.md`** tiene los **338 casos, del CU-001 al CU-348, sin los diez retirados**, cada uno con sus
cuatro artefactos: alto nivel (CUA), expandido (CUE), diagrama de secuencia del sistema
(DSS) y diagrama de interacción de diseño (DSD).

Los casos también están dentro de los documentos 0, 1, 2 y 3 porque **cada plantilla de
la cátedra exige su artefacto ahí**. Este archivo los reúne para no saltar entre cuatro.

## Los comandos

```bash
python3 verificar-conformidad.py   # ¿cumple las plantillas? (31 chequeos)
python3 generar-tabla-implementacion.py  # copia la tabla de implementación (Casos §8) al Documento 3 §4.25
python3 generar-html-drive.py      # regenera drive/*.html
python3 generar-docx-catedra.py    # Documentos de la cátedra en Word (.docx) -> entregables/catedra-docx/ y ~/Desktop/SPLG-Documentacion-Catedra/
python3 generar-sitio.py           # regenera splg-documentacion.html
python3 generar-drawio.py          # regenera drawio/*.drawio (MC, DER, base de datos y clases)
```

## Con qué está hecha

| | |
|---|---|
| **Proceso Unificado** | La metodología que exige la cátedra |
| **Markdown** | Los seis documentos, versionados como texto plano |
| **Mermaid** | Los 711 diagramas de secuencia, interacción, flujo y estados |
| **PlantUML** | Los diagramas de estados, actividad, componentes, despliegue y cronograma (`diagramas/uml/UML_*.puml`). Los de casos de uso los dibuja `generar-uml.py` directamente en SVG |
| **Python** | Verificación de conformidad y generación de los entregables |
| **Git** | Historia completa de cada cambio |
| **Netlify** | Publicación del atlas |

Los diagramas se escriben como código junto al texto que documentan, así que se versionan
igual que el resto y no hay que redibujarlos a mano cuando algo cambia.

El mapa de archivos está en `GUIA-DEL-REPOSITORIO.md`.
