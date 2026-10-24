# SPLG — Landing

Landing comercial de SPLG (Sistema de Pedidos y Logística de Garrafas): app del
cliente, app del chofer y panel de la distribuidora. Sitio estático hecho con
Astro + Tailwind CSS, con un par de islas de React sólo donde hace falta
interacción (el toggle mensual/anual de precios).

## Cómo correr el proyecto

Requiere Node 22+.

```bash
npm install
npm run dev        # http://localhost:4321
npm run build       # genera dist/
npm run preview     # sirve dist/ en http://localhost:4321
npx astro check      # chequeo de tipos de los .astro
```

## Dónde cambiar los precios

Todo vive en un único archivo: `src/data/planes.ts`. Ahí se define cada plan
(nombre, precio mensual, beneficios) y la cantidad de meses que se cobran en
el ciclo anual (`MESES_ANUAL`, hoy 10 → "2 meses gratis"). El toggle
Mensual/Anual y el cálculo del precio anual (`precioAnual()`) están en
`src/components/PlanesToggle.tsx`, no hace falta tocarlo para cambiar montos.

Otros contenidos también están separados en `src/data/`:

- `funciones.ts` — los tres bloques de funciones (app cliente, app chofer, panel).
- `pasos.ts` — los 3 pasos de "Cómo funciona".
- `proximamente.ts` — los módulos marcados como "Próximamente".
- `faq.ts` — preguntas frecuentes.
- `navegacion.ts` — enlaces del header.

## Contacto

**No hay formulario de contacto.** Los botones de "Hablemos" apuntan a
WhatsApp y a mail, y los datos salen de `src/config/contacto.ts`:

```ts
export const contacto = {
  whatsapp: '',   // número internacional sin signos, ej: "5493764000000"
  email: '',
  mensajeWhatsapp: '...',
  asuntoEmail: '...',
};
```

Mientras `whatsapp` o `email` estén vacíos, los botones de contacto se
muestran deshabilitados con el texto "Contacto disponible pronto", y el build
imprime un warning en consola para no olvidarse de completarlos antes de
publicar.

## Paleta e identidad

Tokens semánticos definidos en `src/styles/tokens.css` (Tailwind v4, `@theme`).
Fuente de la paleta: `../splg-docs/material-de-trabajo/MARCA.md`.

| Rol | Valor | Uso |
|---|---|---|
| `primary` | `#F26B1D` | botón principal, marca |
| `primary-hover` | `#DB5A10` | hover del botón principal |
| `on-primary` | `#1B1F27` | texto sobre `primary` (nunca blanco, no pasa AA) |
| `primary-strong` | `#B8460B` | enlaces y texto de acento |
| `accent` | `#FFB21E` | resaltados, etiquetas |
| `on-accent` | `#1B1F27` | texto sobre `accent` |
| `ink` | `#1B1F27` | texto principal, secciones oscuras |
| `muted` | `#5A6072` | texto secundario |
| `outline` | `#D5D9E0` | bordes |
| `bg` | `#FFF8F1` | fondo de página |
| `surface` | `#FFFFFF` | tarjetas y superficies |
| `success` / `danger` / `warn` / `info` | `#16A34A` / `#DC2626` / `#D97706` / `#0284C7` | estados |

También están disponibles las escalas completas `llama-*`, `gas-*` y
`tinta-*` para matices puntuales.

Tipografía: **Sora** (títulos) e **Inter** (texto), cargadas desde Google
Fonts con `display=swap`.

## Estructura

```
src/
  components/   Componentes Astro (estáticos) y dos islas React (.tsx)
  data/         Contenido de cada sección (planes, funciones, FAQ, etc.)
  config/       Datos de contacto
  layouts/      Layout base con head, meta OG/Twitter, header y footer
  pages/        index.astro
  styles/       tokens.css (paleta y estilos base)
public/         favicon, imagen OG (svg y png), robots.txt
```

## Despliegue en Netlify

El repo incluye `netlify.toml` con:

```toml
[build]
  command = "npm run build"
  publish = "dist"
```

Basta con conectar el repo en Netlify; no requiere variables de entorno.

## Accesibilidad y SEO

- Un solo `<h1>` por página, HTML semántico, `lang="es-AR"`.
- Skip-link al contenido, foco visible, contraste AA en todos los textos.
- Respeta `prefers-reduced-motion`.
- Meta description, Open Graph y Twitter card con imagen propia (`public/og.png`,
  generada a partir de `public/og.svg`).
- Sitemap autogenerado (`@astrojs/sitemap`) y `robots.txt`.
