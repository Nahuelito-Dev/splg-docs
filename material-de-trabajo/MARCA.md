# Marca SPLG — paleta y uso (26/09/2026)

Una sola paleta para la landing, el panel y las dos apps. Registro sobrio de
herramienta de gestión: neutros pizarra fríos para casi toda la interfaz, un
naranja quemado como único color de marca y el ámbar reservado para acentos
(etiquetas, gráficos). Reemplaza a la primera versión con fondo crema y naranja
brillante, que se veía poco profesional.

## Escalas

| Token | 50 | 100 | 200 | 300 | 400 | 500 | 600 | **700** | 800 | 900 |
|---|---|---|---|---|---|---|---|---|---|---|
| `llama` (marca) | #FFF7ED | #FFEDD5 | #FED7AA | #FDBA74 | #FB923C | #F97316 | #EA580C | **#C2410C** | #9A3412 | #7C2D12 |
| `gas` (acento) | #FFFBEB | #FEF3C7 | #FDE68A | #FCD34D | **#FBBF24** | #F59E0B | #D97706 | #B45309 | #92400E | #78350F |
| `tinta` (neutro) | #F8FAFC | #F1F5F9 | #E2E8F0 | #CBD5E1 | #94A3B8 | #64748B | #475569 | #334155 | #1E293B | **#0F172A** |

`tinta-950` #020617 para sombras profundas. Fondo de página: `canvas` #F8FAFC.

## Roles semánticos

Los componentes usan roles, no escalas: si la marca cambia, se cambia acá.

| Rol | Valor | Uso |
|---|---|---|
| `primary` | llama-700 #C2410C | botón principal, marca, enlaces |
| `primary-hover` | llama-800 #9A3412 | hover y presionado |
| `on-primary` | #FFFFFF | texto sobre `primary` |
| `primary-soft` | llama-50 | fondos de íconos y selección suave |
| `accent` | gas-400 #FBBF24 | etiquetas, gráficos, "Próximamente" |
| `on-accent` | tinta-900 | texto sobre `accent` |
| `ink` | tinta-900 #0F172A | texto principal, barra lateral, secciones oscuras |
| `muted` | tinta-500 #64748B | texto secundario |
| `outline` | tinta-200 #E2E8F0 | bordes |
| `bg` | canvas #F8FAFC | fondo de página |
| `surface` | #FFFFFF | tarjetas, tablas, modales, barra superior |
| `success` / `danger` / `warn` / `info` | #15803D / #DC2626 / #B45309 / #0369A1 | estados |

Sobre fondo oscuro (barra lateral del panel, sección "Despacho automático" de la
landing) la marca se usa un tono más claro: llama-400 para el ítem activo y la
línea que lo marca, llama-500 para la llama del logo.

## Contraste (WCAG 2.1, medido)

| Combinación | Contraste | Nivel |
|---|---|---|
| blanco sobre llama-700 (botón principal) | 5,18 | AA |
| blanco sobre llama-800 (hover) | 7,31 | AAA |
| llama-700 sobre fondo (enlaces) | 4,95 | AA |
| tinta-900 sobre gas-400 (etiquetas de acento) | 10,69 | AAA |
| blanco sobre tinta-900 (barra lateral) | 17,85 | AAA |
| llama-400 sobre tinta-900 (ítem activo) | 7,89 | AAA |
| tinta-400 sobre tinta-900 (menú inactivo) | 6,96 | AA |
| tinta-500 sobre blanco (texto secundario) | 4,76 | AA |
| tinta-500 sobre fondo | 4,55 | AA |
| blanco sobre llama-500 | 2,80 | **no apto para texto** |

Por eso el botón principal es llama-700 y no el naranja más brillante.

## Tipografía

- Títulos: **Sora** (600/700).
- Texto e interfaz: **Inter** (400/500/600).
- Cifras en tablas: `font-variant-numeric: tabular-nums`.

## Dónde vive

- Panel: `splg-app-admin/src/theme/brand.json`, que leen `tailwind.config.js`,
  el tema de MUI y los gráficos. `npm run colors` falla si aparece un color
  fuera de la paleta.
- Landing: `splg-landing/src/styles/tokens.css` (`@theme` de Tailwind v4).
- Apps: `splg-lib` (tema de Flutter), cuando se adapten.
