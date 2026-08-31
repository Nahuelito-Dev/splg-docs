# Guía para construir el diagrama de casos de uso en draw.io

> Material de trabajo. No forma parte de los documentos de entrega de la cátedra.

### Herramienta recomendada
**app.diagrams.net** (draw.io) — gratuito, online, exporta PNG/SVG.

### Paso 1 — Configurar el canvas
- Abrir draw.io → Nuevo Diagrama → En blanco.
- Menú **Archivo → Configuración de Página**: tamaño **A3**, orientación **horizontal**.

### Paso 2 — Dibujar el límite del sistema
- Insertar un **rectángulo grande** que ocupe el centro del canvas.
- Texto dentro (arriba): `«system» SPLG – Sistema de Pedidos y Logística de Garrafas de Gas`
- Sin relleno, solo borde. Tamaño aproximado: 1400 x 900 px.

### Paso 3 — Agregar los actores (fuera del rectángulo)
Usar la forma **UML Actor** (búscala en el panel lateral → UML → Actor, o usa un stick figure manual):

| Actor | Posición |
|-------|----------|
| `Cliente (ACT-01)` | Lado izquierdo, arriba |
| `Chofer (ACT-02)` | Lado izquierdo, abajo |
| `Administrador (ACT-03)` | Lado derecho, centro |
| `Sistema (ACT-04)` | Abajo, centro |

### Paso 4 — Agregar los Casos de Uso (dentro del rectángulo)
Usar la forma **Ellipse** con texto. Agrupar visualmente por color de fondo:

| Color | Subsistema | CU a incluir |
|-------|-----------|--------------|
| Azul claro | SS-01 Auth | CU-001, CU-002, CU-003 |
| Verde claro | SS-02 Pedidos | CU-005, CU-006, CU-007, CU-008 |
| Naranja claro | SS-03 Despacho | CU-013, CU-014, CU-015 |
| Amarillo claro | SS-04 Tracking | CU-017, CU-018, CU-019, CU-020, CU-021, CU-022 |
| Rojo claro | SS-05 Reclamos | CU-023, CU-024, CU-025 |
| Violeta claro | SS-06 Reportes | CU-026, CU-027, CU-028 |
| Gris claro | SS-07 Choferes | CU-032, CU-033, CU-034 |
| Marrón claro | SS-08 Productos | CU-036, CU-037, CU-038, CU-039, CU-041 |
| Celeste claro | SS-09 Franjas | CU-042, CU-043, CU-044, CU-045 |

> Tip: no incluyas todos los CU o el diagrama queda ilegible. Incluí los **Críticos** e **Importantes**. Los Secundarios los podés omitir o agrupar.

### Paso 5 — Trazar las asociaciones (líneas)

Trazar líneas simples (sin flecha o con flecha simple) entre cada actor y sus CU:

**Cliente (ACT-01) → sus CU:**
CU-001, CU-002, CU-005, CU-006, CU-007, CU-008, CU-021, CU-023, CU-041, CU-044, CU-045

**Chofer (ACT-02) → sus CU:**
CU-001, CU-015, CU-016, CU-017, CU-018, CU-019, CU-020, CU-022

**Administrador (ACT-03) → sus CU:**
CU-001, CU-003, CU-010, CU-011, CU-012, CU-024, CU-025, CU-026, CU-027, CU-028, CU-029, CU-030, CU-031, CU-032, CU-033, CU-034, CU-035, CU-036, CU-037, CU-038, CU-039, CU-040, CU-042, CU-043

**Sistema Automático (ACT-04) → sus CU:**
Agregar un actor con estereotipo `«sistema»` y conectarlo a:
CU-013, CU-014

### Paso 6 — Exportar
- Menú **Archivo → Exportar como → PNG** (resolución 200 dpi mínimo).
- Guardar como `diagrama-cu-sistema.png` en la carpeta `docs/`.
- Insertar la imagen en este documento en la Sección 6.
