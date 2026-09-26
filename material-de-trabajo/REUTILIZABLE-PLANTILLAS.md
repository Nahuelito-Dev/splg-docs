# Qué reutilizar de Tutu admin y de Minimal para el panel — 26/09/2026

Relevamiento de sólo lectura para la puesta a punto del panel (React 18, MUI 5,
DataGrid 6, React Query 5, rhf + zod, Tailwind). Materio no está en el disco.

## Dónde están

| Proyecto | Ruta | Sirve |
|---|---|---|
| Tutu admin (web) | `gearthlogic/others/tutu_admin` | Poco: CRA, JS sin tipos, fork viejo de Minimal, paginación en el cliente. Sólo la idea de validar chofer y vehículo por separado. |
| Minimal v7.3 vite-ts | `~/Desktop/templates/Minimal_TypeScript_v7.3.0/vite-ts` | Sí, adaptando: usa React 19, MUI 7, DataGrid 8 y `minimal-shared`. |

## Qué tomar de Minimal (rutas relativas a `vite-ts/src`)

| Prioridad | Qué | Origen | Para qué en SPLG | Cómo |
|---|---|---|---|---|
| 1 | Formularios `Form` + `Field.*` | `components/hook-form/*`, `schema-helper.ts` | patrón de campos con zod (fechas, archivos, nullable) | adaptar a MUI 5, sin `minimal-shared` |
| 2 | Subida y miniaturas | `components/upload/*`, `components/file-thumbnail/*` | documentación de flota y de choferes (plan semana 1) | adaptar (react-dropzone) |
| 3 | Visor | `components/lightbox/*` | reemplazar abrir documentos en otra pestaña; PDF con iframe o react-pdf | adaptar |
| 4 | Listado con pestañas por estado y filtros en chips | `sections/user/view/user-list-view.tsx`, `components/filters-result/*` | cola de aprobación de choferes, vencimientos (vigente/por vencer/vencido) | adaptar a query params de React Query |
| 5 | Menú por secciones, colapsable, drawer en móvil | `layouts/nav-config-dashboard.tsx`, `components/nav-section/*` | shell del panel | idea; rehacer con Tailwind |
| 6 | Tarjeta de KPI con variación | `sections/overview/app/app-widget-summary.tsx` | tablero | sólo diseño (usan ApexCharts; SPLG, Recharts) |
| 7 | Cajón de notificaciones | `layouts/components/notifications-drawer/*` | campana del panel | adaptar |
| 8 | Estados vacíos y skeletons | `components/empty-content`, `components/table/table-skeleton.tsx` | kit | copiar |

## Qué no tomar

- De Tutu: paginación y filtros con `slice` en el cliente, Redux para datos del
  servidor, token sin `Bearer`, layout con márgenes fijos, JS sin tipos.
- De Minimal: `minimal-shared` y el motor de tema de MUI 7, la toolbar de
  DataGrid 8, SWR, ApexCharts y Mapbox (duplicarían Recharts y Leaflet), la
  paleta verde. Revisar que la licencia comprada cubra el uso en SPLG.
