# Qué se puede traer de Tutu — 25/09/2026

Tutu está en `gearthlogic/tutu-dev/` (backend NestJS + TypeORM + Postgres/PostGIS
+ BullMQ; apps Flutter con BLoC; panel React + MUI). Mismo stack de base que
SPLG, pero con tipado débil, sin pruebas y fechas/montos en `text`/`float`: casi
siempre conviene **adaptar la idea**, no copiar el código. Las apps usan BLoC y
SPLG Stacked: de Flutter se traen servicios y widgets, no pantallas.

| # | De Tutu | Para qué en SPLG | Cómo |
|---|---|---|---|
| 1 | Documentos de vehículo y chofer con vencimientos y validación cruzada (`backend/src/car`, `car-processed-documents`, `driver-processed-documents`, parser de fechas en `common/helpers/index.ts`) | M1 y documentación del chofer | Adaptar a tablas con `date`; copiar reglas y parser |
| 2 | Colas BullMQ + bull-board (`backend/src/bull`, `workers`, `bull-board`) | Jobs de M1, M2 y M4 | Copiar la estructura |
| 3 | Avisos programados con plantillas por anticipación (`notifications.service.ts:28-62`, `:250-315`) | Vencimientos (M1), recompra (M2) | Idea, sobre BullMQ (Tutu usa `node-schedule` en memoria) |
| 4 | Subida de archivos (`cloud-file-upload`, `common/files`) | SPLG no tiene uploads: documentos, fotos, visor | Adaptar a Firebase Storage |
| 5 | Ranking de choferes por ETA con tráfico (`maps/maps.service.ts`) | Despacho y M3 | Reordenar por ETA los 3-5 más cercanos |
| 6 | Rutas con paradas intermedias (`getTollsFee`, `computeRoutes`) | M3 | Misma llamada con `optimizeWaypointOrder` |
| 7 | `tutu_app_driver/lib/services/polylines_service.dart` | Navegación del chofer (hoy vacía) | Copiar a `splg-lib` |
| 8 | Conectividad y restauración de estado (`network_bloc`, `hive_state_service`) | Offline y sesión en las apps | Adaptar |
| 9 | Panel: visor de documentos, vencimientos, aprobación de choferes (`admin/src/pages/Drivers`, `Insurance`) | Flota y visor de imágenes | Copiar componentes (mismo MUI) |
| 10 | Control de versión de la app (`backend/src/app-version`, `new_version_plus`) | Ciclo de vida de las apps | Copiar |

**No traer:** secretos versionados (clave de Firebase Admin, API keys, `.env`),
servicios de más de 2000 líneas con `forwardRef`, jobs en memoria, chat sin
persistencia con salas por email, recompensas propias del ride-hailing,
`aws-sdk` v2.

**Donde SPLG ya es mejor:** despacho secuencial con ofertas que vencen,
identidad del socket por token, servicio en primer plano del chofer,
multi-tenant y pruebas.

Hallazgos que salieron de la comparación: H-86 y H-87 (reconexión del socket).
