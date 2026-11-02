# Marca SPLG — sistema visual «Brasa» (26/09/2026)

Un solo sistema para el panel, la landing y las dos apps. Registro de herramienta
de gestión profesional: neutros fríos para casi toda la interfaz y un único color
de marca, el naranja de la llama, usado con intención (botón principal, sección
activa, gráficos y recargos por zona). Los estados de los pedidos tienen su propio
código de color, separado de la marca, para leerse de un vistazo.


## Escalas

| Token | 50 | 100 | 200 | 300 | 400 | **500** | 600 | 700 | 800 | 900 |
|---|---|---|---|---|---|---|---|---|---|---|
| `llama` (marca) | #FFF5ED | #FFE6D3 | #FFCCA8 | #FFB27A | #FF8A3D | **#F26B1D** | #D9530E | #B8430B | #93360C | #772E0E |
| `gas` (acento) | #FFFAEB | #FEF0C7 | #FEDF89 | #FEC84B | **#FFB020** | #F79009 | #DC6803 | #B54708 | #93370D | #7A2E0E |
| `tinta` (neutro) | #F5F6F8 | #F0F2F5 | #E7EAEE | #D0D5DD | #98A2B3 | #667085 | #475467 | #344054 | #1D2939 | **#0B1220** |

`tinta-25` #FAFBFC (encabezados de tabla, hover de filas) y `tinta-950` #0B0F16
(menú lateral).

## Roles semánticos

| Rol | Valor | Uso |
|---|---|---|
| botón principal | degradé #D24E0D → #B23F0A, borde #A13A09, texto blanco | acción principal de cada pantalla |
| `primary-strong` | llama-700 #B8430B | enlaces y montos de recargo |
| `primary-soft` | llama-50 | fondos suaves de selección |
| `accent` | gas-400 #FFB020 | etiquetas como "Próximamente" |
| `ink` / `ink-2` | #0B1220 / #344054 | texto principal / secundario fuerte |
| `muted` / `faint` | #667085 / #98A2B3 | texto secundario / placeholders |
| `outline` / `outline-soft` | #E7EAEE / #F0F2F5 | bordes y divisores |
| `bg` / `surface` | #F5F6F8 / #FFFFFF | fondo de página / tarjetas |
| menú lateral | #0B0F16, elevado #121824, texto #98A2B3 | con un brillo cálido llama-500 arriba |
| estados | éxito #067647 · peligro #B42318 · aviso #B54708 · info #175CD3 | con fondo suave y punto del mismo color |

## Contraste (WCAG 2.1, medido)

| Combinación | Contraste | Nivel |
|---|---|---|
| blanco sobre el degradé del botón (inicio / centro / fin) | 4,34 / 5,03 / 5,82 | AA en el centro, donde va el texto |
| llama-700 sobre blanco (enlaces) | 5,46 | AA |
| muted sobre blanco / sobre el fondo | 4,97 / 4,60 | AA |
| texto del menú sobre #0B0F16 | 7,45 | AAA |
| llama-400 sobre el menú (ítem activo) | 8,18 | AAA |
| estados sobre su fondo suave (éxito, peligro, aviso, info) | 5,40 · 6,05 · 5,20 · 5,57 | AA |

## Tipografía e íconos

- **Geist** para todo (títulos con tracking -0,03 em) y **Geist Mono** para montos,
  ids, patentes y cifras de tablas.
- Íconos **Lucide**, trazo 1,7–1,8.

## Dónde vive

- Panel: `splg-app-admin/src/theme/brand.json`, que leen `tailwind.config.js`, el
  tema de MUI y los gráficos. `npm run colors` falla si aparece un color fuera
  del sistema.
- Landing: `splg-landing/src/styles/tokens.css` (`@theme` de Tailwind v4) y la
  clase `.btn-primary`.
- Apps: `splg-lib` (tema de Flutter), cuando se adapten.
