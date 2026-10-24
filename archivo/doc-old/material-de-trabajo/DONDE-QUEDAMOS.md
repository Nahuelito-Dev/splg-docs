# Dónde quedamos — 25/09/2026

Es lo primero que hay que leer. Estado general del sistema medido sobre el
código, lo que se hizo el 25/09 y el plan desde el lunes 28/09. El cierre del
24/09 quedó en `historico/DONDE-QUEDAMOS-2026-09-24.md`.

**Ramas:** backend en `fix/alineacion-nest` (pusheado, **falta mergear a
`develop`**), panel y app de clientes en `feature/alta-unificada` (sin mergear),
docs en `develop`.

---

## 1. En una línea

**Las bases del backend están cerradas:** Nest y TypeScript estricto en todo el
código, aislamiento entre distribuidoras probado, modelo de datos completo y
normalizado, bajas lógicas y auditoría. **Desde el lunes se desarrolla por API
sobre tablas que ya existen**, sin volver a tocar el esquema. El panel y las
apps van después y se adaptan a la API.

## 2. Cumplimiento de Nest y TypeScript (medido el 25/09)

| Criterio (CONVENCIONES.md §12) | Estado |
|---|---|
| `tsc` estricto | 0 errores |
| ESLint estricto (sin `any`, sin promesas sueltas) | 0 errores en todo `src` |
| `any` en el código | 0 |
| `forwardRef` | 0 |
| `process.env` fuera de la configuración | 0 (todo por `ConfigService`, validado con Joi) |
| DTO de entrada y de salida con mapper | todos los módulos con endpoints |
| Pruebas | 326 en verde, en 45 archivos |
| Cada módulo dueño de sus tablas | todos salvo dos lecturas de `order` (ver 4.2) |
| Swagger | tipado en los módulos alineados; falta la pasada completa (6.4) |
| Entidades = base de datos | 0 diferencias (`migration:generate` no encuentra nada) |

## 3. Estado de los módulos del backend

### 3.1 Terminados y andando

Cumplen los 12 puntos de "módulo terminado" y se probaron contra la API.

| Módulo | Qué hace | Notas |
|---|---|---|
| `auth`, `registro`, `users`, `role`, `admin` | acceso, alta única de usuarios, perfiles | aislamiento H-66, H-77, H-84; baja lógica de usuario |
| `distributor` | distribuidoras (multi-tenant) | guarda también la configuración de procesos (`module_config`) |
| `customer`, `user-address` | clientes y direcciones | pertenencia por pedidos; direcciones con punto PostGIS |
| `delivery`, `car` | choferes y vehículos | aislamiento H-80; baja lógica |
| `gascylinder` | catálogo, stock y promociones | promociones en tabla; stock con lock pesimista |
| `cylinder` | envases físicos y su trazabilidad | salvo 4.2 |
| `order` | pedidos, despacho secuencial, reservas, pagos | 221 errores de lint → 0; H-78, H-79, H-85 |
| `time-slot`, `coverage-zone` | franjas y zonas PostGIS | salvo 4.2 (`time-slot`) |
| `payments` | MercadoPago y efectivo | |
| `claims`, `incident`, `rating` | posventa | H-82, H-89 |
| `notifications`, `email` | push FCM y correos | rutas de administración sólo del Administrador General (H-83) |
| `reports` | informes de ventas | modelo de lectura (CQRS) documentado |
| `audit` **(nuevo)** | registro de toda escritura (CU-153) y consulta (CU-152) | inmutable en la base |
| `health`, `redis`, `firebase`, `gateways`, `common`, `adapters` | infraestructura | |

### 3.2 Con tablas listas, sin servicios todavía (se desarrollan desde el lunes)

| Módulo | Tablas | Casos de uso |
|---|---|---|
| `fleet` | plan y tarea de mantenimiento, propuesta de ventana de taller, uso del vehículo; en `car`: tara, carga máxima, odómetro, estado en la flota | CU-105 (M1) y CU-136 a CU-142 |
| `cart` | carrito e ítems | CU-122 a CU-126 |
| `order` (ampliación) | historial de estados, cambio de dirección, quién recibe, modalidad express, lotes de recorrido | CU-018 a 020, CU-127, 128, CU-147 a 149, CU-107 (M3) |
| `customer` (ampliación) | consumo declarado, invitación de recompra | CU-143 a 146, CU-106 (M2) |
| `cylinder` (ampliación) | revisión, vencimiento, caso y aviso de recupero | CU-132 a 135, CU-108 (M4) |
| `coverage-zone` (ampliación) | recargo porcentual, etiqueta, color, vigencia | CU-150, 151 |
| `user-address` (ampliación) | piso, departamento, lugar y precisión | falta la resolución contra el mapa (CU-116, 118) |

### 3.2 bis Los clientes ya no se validan (26/09)

Decisión de nahue: el cliente se registra y compra, no hay nada que aprobar.
Fuera `PATCH /customers/:id/validate|invalidate`, la columna `customer.validated`
(migración `ClienteSinValidacion`) y todo lo del panel. **CU-093 dado de baja**:
la documentación pasa a **152 casos de uso**, con el número CU-093 reservado
(no se renumera). El apéndice C de DSD corre un lugar (C.25 → C.24 …). Los
choferes siguen validándose (CU-032). Rama `feat/sin-validacion-de-cliente` en el
back y un commit más en `feat/adaptar-api-25-09` del panel.

### 3.3 Mejoras que quedaron fuera de las bases — RESUELTAS el 26/09

No eran pendientes de las bases (esas se cerraron completas el 25/09): eran
cuatro mejoras que se dejaron para después a propósito. Se hicieron el 26/09 en
`refactor/mejoras-bases` (sale de `fix/alineacion-nest`).

1. **`cylinder` y `time-slot` ya no leen la tabla `order`:** preguntan a
   `OrderLookupModule`, un puerto de lectura que no depende de nadie (no arma
   ciclo). Salió H-90 (aislamiento de envases), resuelto.
2. **camelCase en todas las entidades:** 112 propiedades en 21 entidades. La
   base no cambia (cada columna lleva su `name`) y **la API tampoco**: las
   respuestas pasan por mappers y los DTOs siguen en snake_case, así que el
   panel y las apps no se enteran. Ver H-93 por lo que había que cuidar.
3. **Swagger completo:** cada código que la API devolvió en la corrida de
   Postman está declarado en su ruta (antes faltaban en 52 de 130), con el
   mensaje real como descripción; las respuestas de pedidos, tipadas.
4. **`order.deliveryLatitude/Longitude` → `order.deliveryPoint`** (punto
   PostGIS). Salió H-91, resuelto.

## 4. Lo que se hizo el 25/09

| Tema | Resultado | Detalle |
|---|---|---|
| Aislamiento entre distribuidoras | batería de 205 casos: 66 fallas → 0 | H-77 a H-84, `scripts/alineacion/aislamiento/` |
| Tanda 3 (`users`, `delivery`, `gascylinder`, `order`) | alineados a Nest | H-85: pedir sin stock daba 500 |
| Claves foráneas | las 13 sin declarar, declaradas | 84 en total |
| Baja lógica (H-74) | usuarios, vehículos, zonas, direcciones | Firebase se deshabilita, no se borra |
| Normalización | 1FN a 5FN documentado | `NORMALIZACION.md`; H-88 |
| Modelo propuesto | 17 tablas y 26 columnas implementadas | comparado columna por columna: 0 diferencias |
| Auditoría | CU-152 y CU-153 implementados | |
| Documentación | modelos regenerados (MC, DBM, draw.io); CU/CUE/DSS/DSD en curso | ver 5 |
| Tutu | analizado | `REUTILIZABLE-TUTU.md`, H-86 y H-87 |

Todo el código se probó contra la API corriendo antes de commitear: la colección
de Postman completa, la batería de aislamiento y casos puntuales.

## 5. Documentación — CERRADA (25/09)

| Artefacto | Estado |
|---|---|
| Modelo conceptual (MC) y de base de datos (DBM) | regenerados con todo lo del 25/09, incluidas las claves únicas de H-88; sin elementos «propuesto». Export para draw.io en `drawio/` (draw.io y `.sql` para Importar datos · ERD) |
| Normalización | `NORMALIZACION.md` (FNBC salvo seis redundancias justificadas) |
| CU / CUA / CUE / DSS / DSD | los 153 CU con sus cinco artefactos. Aislamiento, bajas lógicas, stock, normalización y auditoría (CU-152/153) reflejados y verificados contra la API. Copias sincronizadas: 0 diferencias entre los `.mmd` y los documentos, CUE iguales en `1-Requisitos.md` y `Casos-de-Uso.md` |
| Diagramas de casos de uso, contexto e iteraciones | al día; `diagramas/INDICE.md` suma 153 |
| Verificación | 917/917 diagramas Mermaid válidos; `verificar-conformidad.py`: todos cumplen la plantilla de la cátedra |
| Sitio (splg-atlas) | regenerado en local (`splg-documentacion.html`); **no publicado**: se publica cuando nahue lo apruebe |

**Orden de lectura sugerido:**

1. Este archivo.
2. `CAMBIOS-25-09.md`: qué cambió y en qué CU.
3. `MODELO-DE-DOMINIO.md` y `NORMALIZACION.md`.
4. El MC y el DBM (`diagramas/base-de-datos/` o `drawio/`).
5. Los CU por subsistema en `Casos-de-Uso.md`. Para empezar, conviene mirar los que más cambiaron: CU-005, 008 al 019, 085, 093 al 096 y 152/153.

Después sigue la etapa 2 (revisión del código del back y merge a develop), después Postman y por último el panel.

## 6. Qué le sirve al panel (para cuando se adapte)

El panel (`splg-app-admin`) tiene que adaptarse a la API nueva. Lista concreta:

| Cambio en la API | Qué tiene que hacer el panel |
|---|---|
| `customer.validated` es booleano | tratarlo como `true`/`false` (hoy convierte desde texto) |
| Choferes: sin `isTraveling`, sin `notification_token` ni `firebase_uid` | quitar esas columnas |
| `PATCH /delivery/:id` acepta sólo `validated` e `isActive` | ya es lo que manda |
| El admin de empresa no edita, bloquea, resetea ni da de baja clientes, ni toca sus direcciones (403) | ocultar esos botones según el rol |
| `POST /admin` ya no recibe `role_id`; `/admin` suma `user.role` | ajustar el tipo `Admin` |
| Lo de otra distribuidora responde 404 | mensajes "no encontrado" coherentes |
| Nuevos: `GET /audit` (registro de auditoría), promociones validadas, direcciones con piso y departamento | pantallas nuevas: registro de auditoría, gestión de flota y documentación |
| `feature/alta-unificada` | probar con sesión (crear chofer, admin, cliente; resetear contraseña) y mergear |

Del panel de Tutu sirven: visor de documentos, tabla de vencimientos,
aprobación de choferes y el panel de colas (ver 7).

## 7. Plan desde el lunes 28/09

Orden acordado: primero la API, después panel y apps, al final los módulos
inteligentes. **La flota es de la distribuidora:** la documentación de vehículos
y la habilitación de choferes las carga y gestiona el admin de empresa desde el
panel. El chofer no usa auto propio y no carga documentos.

### Semana 1 — API

1. **Mergear** `fix/alineacion-nest` a `develop` (antes del lunes).
2. **Infraestructura de jobs con BullMQ** (idea de Tutu, `backend/src/bull`,
   `bull-board`): reemplaza los crons en memoria y sostiene M1, M2 y M4. Incluye
   el panel de colas, protegido para el Administrador General.
3. **Subida de archivos** (SPLG no tiene): servicio de almacenamiento sobre
   Firebase Storage, con filtro de tipo y tamaño (adaptado de Tutu). Lo necesitan
   la documentación de flota, las fotos de incidencias y reclamos, y el visor.
4. **Flota (CU-136 a 142) sobre `fleet`:** seguro, VTV, licencia y
   mantenimientos como planes y tareas, cargados por el admin. Se adapta de
   Tutu: vencimientos, reglas de validación y parser de fechas. Un vehículo con
   algo vencido que inhabilita queda `grounded` y no recibe ofertas.
5. **Avisos programados por vencimiento** (idea de Tutu: plantillas por
   anticipación, cancelación por referencia) sobre BullMQ, sin estado en memoria.
6. **Historial de estados del pedido** (`order_status_history`): lo escribe la
   máquina de estados en cada transición. Es la fuente de verdad (NORMALIZACION 4.2).
7. **Corregir H-86 y H-87** (reconexión del socket en las apps): `order:snapshot`
   al reconectar y token fresco en cada intento.

### Semana 2 — API

8. Carrito (CU-122 a 126), cambio de dirección y quién recibe (CU-127, 128),
   modalidad express (CU-147 a 149), vigencia y recargo porcentual de zonas
   (CU-150, 151).
9. Revisión y vencimiento de envases (CU-132 a 135).
10. ~~Resolver 3.3.1 (lecturas de `order` desde `cylinder` y `time-slot`).~~ Hecho el 26/09.
11. Despacho: reordenar los primeros 3 a 5 candidatos por tiempo real de manejo
    (idea de Tutu, Distance Matrix con caché).

### Después — panel y apps

12. Adaptar el panel (lista de la sección 6) y agregar las pantallas nuevas:
    flota y documentación con visor (componentes de Tutu), vencimientos,
    aprobación de choferes, registro de auditoría y colas.
13. Apps: navegación del chofer con polilíneas (servicio Dart de Tutu),
    detección de conexión y restauración del estado, control de versión.

### Al final — módulos inteligentes

14. M1 planificación de flota, M2 recompra, M3 agrupación por recorrido (rutas
    con paradas optimizadas), M4 recupero de envases. Las tablas ya están.

### Landing page (nueva, falta)

15. **Landing para promocionar el servicio.** No existe nada todavía. Qué es,
    para quién (distribuidoras de gas: dueños y administración), qué resuelve
    (pedidos por app, despacho automático, seguimiento en vivo, flota,
    trazabilidad de envases), cómo se ve (capturas del panel y de las apps),
    planes y contacto. Página estática independiente del panel, con la marca
    SPLG. **Hay que definir:** dominio, si tiene formulario de contacto o
    agenda de demo, y si muestra precios. Puede hacerse en paralelo a la
    semana 1, porque no depende de la API.

## 8. Hallazgos abiertos

| # | Qué | Dónde |
|---|---|---|
| H-86 | Al reconectar el socket, las apps no recuperan el estado del pedido | plan, punto 7 |
| H-87 | El chofer podría no reconectarse con el token vencido (sin verificar) | plan, punto 7 |
| H-53 | `/health` da 503 bajo la batería completa | |
| H-54 | El evento "en camino" se llama distinto en cliente y panel | |
| H-55 | La asignación manual no avisa al chofer por socket | |
| H-57 | La granularidad semanal de los informes se ignora | |
| Prod | Revisar la base de producción (consultas de H-76 y H-77) y rotar secretos | |

## 9. Cómo se trabaja

- El back de prueba corre en **:3100**. `scripts/alineacion/modulo.sh <etiqueta>
  <carpetas>` hace lint, pruebas, la colección de Postman y compara las formas de
  respuesta. `aislamiento/run.sh` corre la batería entre distribuidoras
  (`SPLG_CLAVE=...`).
- Migraciones: `npm run migration:generate`, **revisar el SQL** (para cambios de
  tipo o renombres se escribe a mano, con conversión de datos),
  `migration:run`, `migration:revert` y otra vez `run`, y chequear que
  `generate` no encuentre diferencias.
- Documentación: `cue.py`, `dss.py` y `dsd.py` editan todas las copias; después
  el validador de Mermaid y `verificar-conformidad.py`.
- **Nada se commitea sin probarlo contra la API**: ni el código ni las
  afirmaciones nuevas de la documentación.
