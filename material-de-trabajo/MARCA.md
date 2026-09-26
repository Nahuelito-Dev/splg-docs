# Marca SPLG — paleta y uso (26/09/2026)

Una sola paleta para la landing, el panel y las dos apps. Reemplaza al violeta
del panel y a la idea de usar la paleta del portfolio. Tono comercial de
servicio de gas: naranja de llama como color de marca, ámbar de acento y un
carbón azulado para textos y superficies oscuras.

## Escalas

| Token | 50 | 100 | 200 | 300 | 400 | **500** | 600 | 700 | 800 | 900 |
|---|---|---|---|---|---|---|---|---|---|---|
| `llama` (marca) | #FFF4EB | #FFE6D2 | #FFC9A3 | #FFA469 | #FB8438 | **#F26B1D** | #DB5A10 | #B8460B | #92380E | #772F10 |
| `gas` (acento) | #FFF9EB | #FFEFC6 | #FFDE88 | #FFCA4A | **#FFB21E** | #F99307 | #DD6D02 | #B74B06 | #943A0C | #7A300D |
| `tinta` (neutro) | #F6F7F9 | #ECEEF2 | #D5D9E0 | #B0B6C3 | #858D9F | #5A6072 | #474C5B | #3A3E4A | #2A2E38 | **#1B1F27** |

Fondo cálido de página: `crema` #FFF8F1.

## Roles semánticos

Los componentes usan roles, no escalas: si la marca cambia, se cambia acá.

| Rol | Valor | Uso |
|---|---|---|
| `primary` | llama-500 #F26B1D | botón principal, marca, indicadores activos |
| `primary-hover` | llama-600 #DB5A10 | hover y presionado |
| `on-primary` | tinta-900 #1B1F27 | texto sobre `primary` |
| `primary-strong` | llama-700 #B8460B | enlaces y texto de acento sobre fondo claro |
| `accent` | gas-400 #FFB21E | resaltados, etiquetas, gráficos |
| `on-accent` | tinta-900 | texto sobre `accent` |
| `ink` | tinta-900 | texto principal, barra lateral, secciones oscuras |
| `muted` | tinta-500 #5A6072 | texto secundario |
| `outline` | tinta-200 #D5D9E0 | bordes |
| `bg` | crema #FFF8F1 | fondo de página |
| `surface` | #FFFFFF | tarjetas, tablas, modales |
| `success` / `danger` / `warn` / `info` | #16A34A / #DC2626 / #D97706 / #0284C7 | estados |

## Contraste (WCAG 2.1, medido)

| Combinación | Contraste | Nivel |
|---|---|---|
| tinta-900 sobre llama-500 (botón principal) | 5,42 | AA |
| tinta-900 sobre gas-400 | 9,15 | AAA |
| blanco sobre tinta-900 | 16,51 | AAA |
| llama-700 sobre crema (enlaces) | 5,09 | AA |
| tinta-500 sobre blanco (texto secundario) | 6,27 | AA |
| blanco sobre llama-500 | 3,05 | **sólo texto grande o íconos** |

Por eso el botón principal lleva texto tinta y no blanco. Si se quiere texto
blanco, el fondo es llama-700 (5,36).

## Tipografía

- Títulos: **Sora** (600/700).
- Texto e interfaz: **Inter** (400/500/600).
- Cifras en tablas: `font-variant-numeric: tabular-nums`.

## Dónde vive

- Landing: `splg-landing/src/styles/tokens.css` y `tailwind.config`.
- Panel: `splg-app-admin/tailwind.config.js` y el tema de MUI.
- Apps: `splg-lib` (tema de Flutter), cuando se adapten.
