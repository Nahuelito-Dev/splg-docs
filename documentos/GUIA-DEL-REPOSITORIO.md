# SPLG — Guía del repositorio de documentación

**Sistema de Pedidos y Logística de Garrafas de Gas**
Proceso Unificado · FCEQyN – UNaM · Nahuel Wagner

Este repositorio contiene la documentación del proyecto, separada del código del sistema.

---

## Cómo está organizado

La raíz tiene sólo `README.md`, `VERSION`, `AGENTS.md`, `CLAUDE.md` y `publicar.sh`. Todo lo
demás está en carpetas. Los documentos, que antes estaban en la raíz, están en `documentos/`.

```
splg-docs/
├── documentos/
│   ├── 0-Plan_Del_Proyecto.md          ← entrega
│   ├── 0.1-Planificacion_Iteraciones.md ← entrega
│   ├── 1-Requisitos.md                 ← entrega
│   ├── 2-Analisis.md                   ← entrega
│   ├── 3-Diseño.md                     ← entrega
│   ├── Casos-de-Uso.md                 ← LOS 338 CASOS, COMPLETOS
│   ├── INDICE-IMAGENES.md · GUIA-actualizar-drive.md · GUIA-DEL-REPOSITORIO.md
│
├── modelos/
│   ├── drawio/                     MC, DER, DBD y DC en draw.io (+ LEEME)
│   └── base-de-datos/              SQL, SPLG-modelo.json, diccionario y DER por módulo
├── diagramas/                      DSS, DSD, CU, pantallas y wireframes (PNG, SVG, .mmd, PlantUML)
├── sistema/                        documentación técnica del código: back/, postman, setup, estado
├── capturas/                       capturas reales del panel y de las apps (customer, driver, panel, referencias-figma)
├── catedra/
│   ├── drive/                      los seis documentos en HTML, para subir
│   ├── entregables/                diagramas de casos de uso sueltos y Word de la cátedra
│   ├── .catedra-ref/               las plantillas originales de la cátedra
│   └── material-de-trabajo/        auditorías, guías, trazabilidad, notas
├── sitio/                          generador y archivos del sitio publicado
└── herramientas/                   los scripts .py y scripts/ (versionado)
```

Los links de los `.md` de `documentos/` a las imágenes son relativos a esa carpeta: `../diagramas/png/…`.

## El documento único: `Casos-de-Uso.md`

Es el que se abre cuando hay que mostrar un caso puntual. Tiene **los 338 casos, del
CU-001 al CU-291**, cada uno con sus cuatro artefactos:

| Sección | Contenido | Cobertura |
|---------|-----------|-----------|
| §1 | Actores del sistema | — |
| §2 | Diagrama de casos de uso del sistema | — |
| §3 | Catálogo y calificación | 336 |
| §4 | **CUA** — Casos de uso de alto nivel | 336 |
| §5 | **CUE** — Casos de uso expandidos | 336 |
| §6 | **DSS** — Diagramas de secuencia del sistema | 336 |
| §7 | **DSD** — Diagramas de interacción de diseño | 336 |

2101 KB, 711 diagramas.

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
| 0 | `0-Plan_Del_Proyecto.md` | Fases e iteraciones, hitos, cronograma, actores, los 338 casos de uso de alto nivel y su calificación. |
| 0.1 | `0.1-Planificacion_Iteraciones.md` | Metas, artefactos y problemas a resolver de cada iteración. |
| 1 | `1-Requisitos.md` | Objetivos, subsistemas, requisitos de información, los 338 casos de uso expandidos, requisitos no funcionales, matriz de rastreabilidad y glosario. |
| 2 | `2-Analisis.md` | Modelo conceptual de los 21 casos de uso esenciales, diez diagramas de secuencia del sistema (los casos con interacción del actor), los 8 contratos de las operaciones que cambian el estado y el glosario. |
| 3 | `3-Diseño.md` | Arquitectura, casos de uso reales, diagramas de interacción, diagrama de clases, especificación de los módulos inteligentes, wireframes y diagrama entidad-relación. |

`Casos-de-Uso.md` reúne los cuatro artefactos de los 338 casos en un solo archivo. Es el
documento de consulta; su contenido se corresponde con el de los documentos 0, 1 y 2, que
lo conservan porque las plantillas exigen que cada artefacto figure donde le toca.

Las plantillas originales de la cátedra están en `catedra/.catedra-ref/`.

## Los cuatro artefactos de cada caso de uso

| Sigla | Artefacto | Documento |
|-------|-----------|-----------|
| CUA | Caso de uso de alto nivel | 0 — Plan del Proyecto §7 |
| CUE | Caso de uso expandido | 1 — Requisitos §7 |
| DSS | Diagrama de secuencia del sistema | 2 — Análisis §2.1 |
| DSD | Diagrama de interacción de diseño | 3 — Diseño §4 |

Los 338 casos tienen los cuatro.

## Herramientas

| Script | Qué hace |
|--------|----------|
| `verificar-conformidad.py` | Chequea los artefactos contra las plantillas de la cátedra. Devuelve error si algo no cumple. |
| `generar-html-drive.py` | Regenera los seis documentos en HTML, listos para abrir con Documentos de Google. Salida en `catedra/drive/`. |
| `generar-tabla-implementacion.py` | Copia la «Tabla de implementación por caso de uso» de `Casos-de-Uso.md` §8 (la fuente) al Documento 3 §4.25. Se corre después de `generar-operaciones.py`. |
| `sitio/generar-sitio.py` | Genera el Atlas: una página con los cuatro artefactos de cada caso y su respaldo documental. No regenera `modelos/drawio/`: avisa si está desactualizado. |
| `generar-drawio.py` | Genera en `modelos/drawio/` los modelos para draw.io: modelo conceptual, DER, base de datos físico y clases de diseño, cada uno en una página y con las relaciones como aristas conectadas. |
| `verificar-drawio.py` | Cuenta las aristas sueltas y compara las relaciones de cada `.drawio` contra la base, el modelo conceptual y el diagrama de clases. |
| `verificar-links.py` | Recorre los `.md` y los `.html` y comprueba que cada ruta local que enlazan exista. |

Todos los scripts están en `herramientas/` salvo `sitio/generar-sitio.py`; se corren desde la raíz del repositorio.

```bash
python3 herramientas/verificar-conformidad.py     # 32 chequeos
python3 herramientas/generar-html-drive.py        # -> catedra/drive/*.html
python3 sitio/generar-sitio.py                    # -> sitio/splg-documentacion.html
python3 herramientas/generar-drawio.py            # -> modelos/drawio/*.drawio
python3 herramientas/verificar-drawio.py          # 0 relaciones faltantes y 0 aristas sueltas
python3 herramientas/verificar-links.py           # 0 rutas rotas
```

## Diagramas

| Carpeta | Contenido |
|---------|-----------|
| `diagramas/*.mmd` | Código Mermaid de cada diagrama de secuencia e interacción |
| `diagramas/png/` · `diagramas/svg/` | Los mismos, renderizados |
| `modelos/base-de-datos/` | Esquema SQL, `SPLG-modelo.json`, diccionario de datos y los DER (físico y conceptual) por módulo |
| `diagramas/uml/` | Casos de uso en notación UML (diagrama por subsistemas, completo, láminas por actor y uno por subsistema, en SVG y PNG) y los diagramas de estados, actividad, componentes, despliegue y cronograma (fuente PlantUML) |

Cada imagen lleva el código y el nombre del caso de uso en el nombre del archivo.
`Casos-de-Uso.md`, `2-Analisis.md` y `3-Diseño.md` muestran cada DSS y DSD como esa imagen y dejan el Mermaid
plegado debajo (`incrustar-imagenes-cu.py`); `diagramas/fuentes-png.json` anota de qué `.mmd` sale cada PNG y el
gate avisa si alguno quedó viejo.
`INDICE-IMAGENES.md` dice dónde va cada una dentro de los documentos.

## Pantallas

| Ruta | Contenido |
|------|-----------|
| `diagramas/design/wireframes.html` | Los nueve wireframes renderizados, listos para capturar |
| `diagramas/design/*.png` | Capturas de las aplicaciones en el simulador |
| `capturas/` | Capturas reales del panel y de las apps, sin reducir (`customer/`, `driver/`, `panel/`, `referencias-figma/`) |
| `diagramas/pantallas/CU-xxx-<pantalla>.png` | Capturas de las pantallas de cada CU Real (§3 de `3-Diseño.md`); las de las apps son reales, tomadas con la app corriendo contra la API |

### Regenerar las capturas de las apps

Con el entorno levantado (`./splg-dev.sh --seed`, back en `:3010`) y el simulador de cada app abierto:

| App | Comando (desde el repo de la app) | Salida |
|---|---|---|
| Cliente (iPhone 16 Pro) | `scripts/capturas_cu_reales.py` | `build/capturas_cu_reales/CU-xxx-*.png` |
| Chofer (iPhone 16 Pro Max) | `scripts/capturas_cu_reales.py` | `build/capturas_cu_reales/CU-xxx-*.png` |

Cada script corre `integration_test/capturas_cu_reales_test.dart` con `--dart-define=API_BASE_URL=http://localhost:3010 --dart-define=PUSH_ENABLED=false`, saca la captura con `xcrun simctl io <udid> screenshot` cada vez que el test avisa `SHOT:<nombre>` y prepara y limpia por la API los pedidos «Prueba capturas …». Después se copian a `diagramas/pantallas/` (reducidas a 603 px de ancho con `sips -z 1311 603`). La app del chofer necesita a `chofer@splg.com` sin pedidos en curso.

## Verificación contra el código

La documentación se contrasta contra el sistema construido con los verificadores de
`herramientas/` (artefactos, relaciones, cifras de la base, cruce DSD↔clases y MC↔DER)
y el gate `verificar-conformidad.py`. Lo pendiente de implementación está en `3-Diseño.md` §10.
Los informes de auditoría anteriores están en el historial de git del repositorio (se retiraron el 24/10/2026, antes de congelar la v1).

Lo anterior a esa revisión está en el historial de git y no forma parte de la entrega.

## Qué no está acá

El código del sistema vive en los repositorios del backend y de las aplicaciones; su documentación
técnica, en `sistema/`.
Este repositorio no contiene credenciales: `.gitignore` bloquea las claves de servicio
y los archivos de entorno.
