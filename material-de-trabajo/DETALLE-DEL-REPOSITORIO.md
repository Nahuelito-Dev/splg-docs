# SPLG — Documentación

**Sistema de Pedidos y Logística de Garrafas de Gas**
Proceso Unificado · FCEQyN – UNaM · Nahuel Wagner

Este repositorio contiene la documentación del proyecto, separada del código del sistema.

---

## Cómo está organizado

En la raíz hay **seis documentos y nada más**: los cinco que exige la cátedra y el que
reúne todos los casos de uso. Todo lo demás está en carpetas.

```
splg-docs/
├── 0-Plan_Del_Proyecto.md          ← entrega
├── 0.1-Planificacion_Iteraciones.md ← entrega
├── 1-Requisitos.md                 ← entrega
├── 2-Analisis.md                   ← entrega
├── 3-Diseño.md                     ← entrega
├── Casos-de-Uso.md                 ← LOS 108 CASOS, COMPLETOS
│
├── diagramas/                      imágenes y fuentes de los diagramas
├── design/                         wireframes y capturas de pantalla
├── drive/                          los seis documentos en HTML, para subir
├── .catedra-ref/                   las plantillas originales de la cátedra
├── material-de-trabajo/            auditorías, guías, trazabilidad, notas
└── old/                            versiones anteriores a la revisión (no se entrega)
```

## El documento único: `Casos-de-Uso.md`

Es el que se abre cuando hay que mostrar un caso puntual. Tiene **los 108 casos, del
CU-001 al CU-108**, cada uno con sus cuatro artefactos:

| Sección | Contenido | Cobertura |
|---------|-----------|-----------|
| §1 | Actores del sistema | — |
| §2 | Diagrama de casos de uso del sistema | — |
| §3 | Catálogo y calificación | 108 |
| §4 | **CUA** — Casos de uso de alto nivel | 108 |
| §5 | **CUE** — Casos de uso expandidos | 108 |
| §6 | **DSS** — Diagramas de secuencia del sistema | 108 |
| §7 | **DSD** — Diagramas de interacción de diseño | 108 |

711 KB, 213 diagramas.

### Por qué los casos también aparecen en los otros documentos

No es duplicación por descuido: **las plantillas de la cátedra lo exigen**. Cada artefacto
tiene que figurar en el documento que le toca —los de alto nivel en el Plan del Proyecto,
los expandidos en Requisitos, los de secuencia en Análisis y los de interacción en Diseño—
porque cada documento se entrega y se corrige por separado. `Casos-de-Uso.md` los reúne
para poder consultarlos sin saltar entre cuatro archivos.

---

## Los documentos de la cátedra

| # | Documento | Contiene |
|---|-----------|----------|
| 0 | `0-Plan_Del_Proyecto.md` | Fases e iteraciones, hitos, cronograma, actores, los 108 casos de uso de alto nivel y su calificación. |
| 0.1 | `0.1-Planificacion_Iteraciones.md` | Metas, artefactos y problemas a resolver de cada iteración. |
| 1 | `1-Requisitos.md` | Objetivos, subsistemas, requisitos de información, los 108 casos de uso expandidos, requisitos no funcionales, matriz de rastreabilidad y glosario. |
| 2 | `2-Analisis.md` | Modelo conceptual, los 108 diagramas de secuencia del sistema, los 26 contratos de operación y los módulos inteligentes. |
| 3 | `3-Diseño.md` | Arquitectura, casos de uso reales, diagramas de interacción, diagrama de clases, especificación de los módulos inteligentes, wireframes y diagrama entidad-relación. |

`Casos-de-Uso.md` reúne los cuatro artefactos de los 108 casos en un solo archivo. Es el
documento de consulta; su contenido se corresponde con el de los documentos 0, 1 y 2, que
lo conservan porque las plantillas exigen que cada artefacto figure donde le toca.

Las plantillas originales de la cátedra están en `.catedra-ref/`.

## Los cuatro artefactos de cada caso de uso

| Sigla | Artefacto | Documento |
|-------|-----------|-----------|
| CUA | Caso de uso de alto nivel | 0 — Plan del Proyecto §7 |
| CUE | Caso de uso expandido | 1 — Requisitos §7 |
| DSS | Diagrama de secuencia del sistema | 2 — Análisis §2.1 |
| DSD | Diagrama de interacción de diseño | 3 — Diseño §4 |

Los 108 casos tienen los cuatro.

## Herramientas

| Script | Qué hace |
|--------|----------|
| `verificar-conformidad.py` | Chequea los artefactos contra las plantillas de la cátedra. Devuelve error si algo no cumple. |
| `generar-html-drive.py` | Regenera los seis documentos en HTML, listos para abrir con Documentos de Google. Salida en `drive/`. |
| `generar-atlas.py` | Genera el Atlas: una página con los cuatro artefactos de cada caso y su respaldo documental. |

```bash
python3 verificar-conformidad.py     # 11 verificaciones
python3 generar-html-drive.py        # -> drive/*.html
python3 generar-atlas.py             # -> atlas-casos-de-uso.html
```

## Diagramas

| Carpeta | Contenido |
|---------|-----------|
| `diagramas/*.mmd` | Código Mermaid de cada diagrama de secuencia e interacción |
| `diagramas/png/` · `diagramas/svg/` | Los mismos, renderizados |
| `diagramas/uml/` | Casos de uso en notación UML: contexto y uno por subsistema, con su fuente PlantUML |

Cada imagen lleva el código y el nombre del caso de uso en el nombre del archivo.
`INDICE-IMAGENES.md` dice dónde va cada una dentro de los documentos.

## Pantallas

| Ruta | Contenido |
|------|-----------|
| `design/wireframes.html` | Los nueve wireframes renderizados, listos para capturar |
| `design/diagrams-png/` | Diagramas exportados como imagen |
| `design/*.png` | Capturas de las aplicaciones en el simulador |

## Verificación contra el código

La documentación se contrastó contra el sistema construido. El resultado está en
`INFORME-HALLAZGOS.md`, la correspondencia caso por caso en `TRAZABILIDAD-CU-CODIGO.md`,
y el detalle en los informes `AUDITORIA-*`.

Lo anterior a esa revisión quedó en `old/` y no forma parte de la entrega.

## Qué no está acá

El código del sistema vive en los repositorios del backend y de las aplicaciones.
Este repositorio no contiene credenciales: `.gitignore` bloquea las claves de servicio
y los archivos de entorno.
