# Auditoría S3 — imágenes y adjuntos (11/10/2026)

Sólo lectura: no se subió ni borró nada, no se tocó código ni datos. Back :3010 (bucket real `splg-tesis`, sa-east-1; no hay MinIO levantado), panel :3001, base `splg_db` (contenedor `splg-bd`), superadmin con `X-Distributor: demo`.

## 1. Tabla de inventario

| Entidad | Columna / tabla | Filas con key en `splg_db` | Subida (back) | Lectura (back) | Panel MUESTRA | Panel SUBE / CAMBIA / QUITA | Viejas / rotas |
|---|---|---|---|---|---|---|---|
| Usuario (foto de perfil) | `user.photo_key` | 0 de 46 | `PUT /users/me/photo`, `PUT /users/:id/photo` | `GET .../photo` (302) o `?modo=url`; `photoUrl` firmada en listas | Sí: Usuarios (tabla y ficha), Admins, Cuenta, avatar del topbar | Sí: ficha de usuario y Mi cuenta (`EntityPhoto`) | `user.selfie` (texto, 0 con valor). |
| Cliente | = su usuario (`user.photo_key`) | 0 (0 de 28 clientes) | igual que usuario | `customer.user.photoUrl` | Sí: Clientes (tabla y ficha) | Sí, en la ficha (sube a `/users/:id/photo`) | no |
| Chofer / delivery | = su usuario | 0 (0 de 5) | igual que usuario | `delivery.user.photoUrl` | Sí: Choferes (tabla, ficha, perfil), vehículo (chofer actual) | Sí, en ficha del chofer | no |
| Legajo de empleado | `employee.photo_key` | 0 de 6 | `PUT /employees/:id/photo` (409 si tiene cuenta) | `GET /employees/:id/photo`, `photoUrl` en el listado | NO: el panel no tiene pantalla de legajos ni llama a `/employees` | NO | no |
| Adjuntos del legajo (genérico) | tabla `attachment` + `storage_key` | 0 | `POST /attachments/:ownerType/:ownerId` | `GET /attachments/:t/:id`, `GET /attachments/:id/download` | NO | NO | Sólo `employee` está registrado como dueño; los otros 7 `ownerType` del enum (`fuel_load`, `traffic_fine`, `vehicle_accident`, `purchase_receipt`, `stock_adjustment`, `driver_settlement`, `cash_movement`) no tienen resolver: no se puede adjuntar a nada de eso |
| Vehículo (`car`) | `car.photo_key` | 7 de 7 | `PUT /car/:id/photo` | `GET /car/:id/photo`, `photoUrl` | Sí: Vehículos (tabla), ficha y resumen | Sí (reemplazar / quitar) | no |
| Documentación de flota (VTV, seguro, licencia, comprobante) | `maintenance_task_attachment.storage_key` | 0 filas | `POST /fleet/tasks/:id/attachments` | `GET /fleet/tasks/:id/attachments`, `.../:attId/download` | Sí: Tarea de flota > Adjuntos (lista y grilla). Hoy vacío | Sí: botón "Adjuntar archivo" + arrastrar | La VTV/seguro no son columnas del vehículo: son tareas con adjuntos (hay 1 tarea, sin adjuntos) |
| Producto (`gas_cylinder`) | `gas_cylinder.photo_key` | demo 4 de 4; "prueba-stock" 0 de 2 | `PUT /gascylinder/:id/photo` | `photoUrl` en catálogo; GET público | Sí: Garrafas (tabla y ficha) | Sí | no |
| Distribuidora (logo) | `distributor.logo_key` + `logo_url` (texto) | 1 de 2 (demo sí, prueba-stock no) | `PUT /distributor/:id/logo` | `photoUrl ?? logo_url` | Sí: tarjeta de tenant del menú, Distribuidoras (tabla y ficha), Configuración | Sí (ficha de distribuidora y Configuración) | `logo_url` vacío en las 2 |
| Incidencia | `incident.photo_key` (+ `photo_url` legado) | 26 de 26 | `PUT /incidents/:id/photo` (409 si no está abierta) | `photoUrl`, `GET .../photo` | Sí: drawer de detalle | Sí en el drawer (Reemplazar/Quitar). El alta "Nueva incidencia" pide una URL de texto, no un archivo | `photo_url` externo: 0 |
| Reclamo | `claims.photo_key` (+ `"photoUrl"` legado) | 21 de 24 (los 3 sin foto son pruebas) | `POST /claims/:id/photo` (sin DELETE) | `GET /claims/:id/photo`, `?modo=url` | Sí: drawer de detalle | Sí en el drawer (subir/reemplazar). El alta "Nuevo reclamo" pide URL de texto | `"photoUrl"` externo: 0 |
| Cámara / foto en pedido (entrega, firma) | No existe columna | - | - | - | - | - | No hay prueba de entrega con foto |

Otras columnas tipo `*_url` / `file`: `payment.payment_url` (link de pago, no imagen), `audit_log.path` (ruta HTTP). No hay más. `storage_orphan`: sin filas (ni pendientes ni `failed`).

Base de datos, resultado de los conteos: 0 URLs externas viejas (`incident.photo_url`, `claims."photoUrl"`, `distributor.logo_url` y `user.selfie` en cero o vacíos), 0 keys apuntando a algo que no existe (ver sección 2: todas las keys firmadas responden 200).

## 2. Prueba contra la API (curl/fetch, evidencia)

Login `POST /api/auth/login/dashboard` con superadmin: 200. Se pidió la URL firmada (lista y `?modo=url`) y se hizo GET a S3:

| Entidad | Resultado |
|---|---|
| car | 7/7: 200 `image/png`; `?modo=url` devuelve `https://splg-tesis.s3.sa-east-1.amazonaws.com/cars/...?X-Amz-...` y también 200 `image/png` |
| gascylinder | 4/4: 200 `image/png` (lista y `?modo=url`) |
| distributor | demo: 200 `image/png`; prueba-stock: `{"url":null}` |
| incident | 26/26: 200 `image/png` |
| claim | 21/21: 200 `image/png`; 3 sin foto -> `{"url":null,"expiresAt":null,"requiresAuth":false}` |
| user / customer / delivery / employee / `users/me` | Sin foto: `GET .../photo?modo=url` -> 200 `url:null`. **No se pudo comprobar una URL firmada de usuario/chofer/legajo porque no hay ninguna cargada** |
| fleet attachments | 0 adjuntos: no se pudo probar la descarga (`/fleet/tasks/:id/attachments` lista vacía, 200) |
| attachments genéricos | 0 filas: sin prueba de descarga |

Pdf: no hay ninguno para probar.

## 3. Prueba en el panel (Chromium headless, superadmin, tenant demo)

Capturas: carpeta `capturas-apps/panel/s3/` (01..22 y 14b, 15b). Medición con `naturalWidth > 0`; además se escuchó la red: 0 respuestas >=400 de `amazonaws.com`.

- Vehículos (7 miniaturas), ficha del vehículo, Garrafas (4 + ficha), Distribuidoras (logo), ficha, logo del tenant en el menú: cargan, todas `naturalWidth` 320, sin 403.
- Drawer de incidencia (`14b-incident-drawer.png`) y de reclamo con foto (`15b-claim-drawer-con-foto.png`): imagen S3 cargada (438x160).
- Usuarios, Choferes, Clientes, Mi cuenta: muestran las iniciales (no hay fotos), con botón "Subir foto" en cada ficha.
- Tarea de flota (`18-fleet-task-detail.png`): sección Adjuntos con "Adjuntar archivo" (vacía).
- En modo "Todas las empresas" el detalle de tarea de flota dice "No se pudo cargar / Elegí una distribuidora" (esperado, hay que usar "Ver como"). Un reclamo de prueba sin foto muestra "Sin foto" + "Subir foto".
- Falso positivo del contador: en todas las pantallas con el menú hay una segunda `<img>` del logo con caja 0x0 (`complete=false`) dentro de la tarjeta del tenant; la visible (26x26) carga bien. No hay placeholder roto a la vista.
- No existe pantalla de legajos (`/employees`): "legajos" no se pudo recorrer.

## 4. Apps móviles (sólo lectura de código)

- Chofer: muestra su foto de perfil (`GET users/me/photo?modo=url`, perfil y calificación). NO sube ni cambia foto; la incidencia (`POST /incidents`) no adjunta foto. No hay `image_picker`.
- Cliente: no sube ni muestra foto de perfil; el reclamo (`claim_sheet`) y su detalle no tienen foto; el catálogo/detalle de garrafa usa `assets/cylinder_10.png` fijo, no `photoUrl` del back; el tracking intenta `avatar/photo/selfie/image` del chofer (nombres que el back no manda como `photoUrl`). No hay `image_picker`/`file_picker` en ninguna de las dos apps ni en `splg-lib` (`SplgAvatar` sólo lee una URL).

## 5. Qué falta, priorizado

Veredicto: lo hecho funciona (todo lo cargado en S3 se ve en el panel y firma bien), pero "absolutamente todo" aún no está.

### Back
1. (alto) Registrar resolvers para los `ownerType` del enum que no tienen dueño (`fuel_load`, `traffic_fine`, `vehicle_accident`, `purchase_receipt`, `stock_adjustment`, `driver_settlement`, `cash_movement`) o sacarlos del enum: hoy `POST /attachments/<esos>` no tiene a quién asignarse.
2. (medio) `POST /claims` y `POST /incidents` siguen aceptando `photoUrl` / `photo_url` externa de texto: se pueden seguir guardando URLs fuera de S3. Aceptar sólo la subida de archivo (o una subida junto con el alta).
3. (medio) `user.selfie` es texto libre sin migrar a S3 (hoy 0 valores); decidir si se elimina o se mapea a `photo_key`. `distributor.logo_url`, `incident.photo_url` y `claims."photoUrl"` quedan como columnas legadas.
4. (medio) El tracking de pedido para el cliente no expone la foto del chofer como `photoUrl` firmada (la app busca `avatar/photo/selfie/image`).
5. (bajo) Datos de demo: no hay fotos de usuarios, choferes ni legajos, ni adjuntos de flota ni de legajo, así que esas rutas están sin una prueba de punta a punta (extender `npm run fotos:demo`). La distribuidora "prueba-stock" y sus 2 garrafas no tienen foto. `GET /gascylinder?limit=200` devolvió 0 en mi script (probablemente 400 por límite); no investigado.

### Panel
1. (alto) No existe pantalla de legajos de empleados: no se ve ni se sube su foto ni sus adjuntos (`/employees`, `/employees/:id/photo`, `/attachments/employee/:id`).
2. (alto) Adjuntos genéricos (`/attachments`) sin UI.
3. (medio) Alta de Incidencia y de Reclamo piden una URL de texto para la foto; deberían ofrecer subir un archivo (el panel sube recién desde el drawer, ya creado).
4. (bajo) `UserDetails` pinta `user.selfie` con `<img>` directo (URL no firmada) como respaldo.
5. (bajo) Vehículo: la VTV y el seguro viven sólo como adjuntos de tareas; no hay una vista "documentos del vehículo" en la ficha del vehículo.

### Apps
1. (alto) Cliente: foto de perfil (mostrar y subir), foto en el reclamo (subir y ver) y foto real del producto en el catálogo (`photoUrl`).
2. (alto) Chofer: subir/cambiar su foto de perfil y adjuntar foto en la incidencia (hoy sólo la muestra).
3. (medio) Agregar `image_picker` y un widget común en `splg-lib` (el `SplgAvatar` sólo lee).
4. (bajo) Prueba de entrega con foto: no existe en back ni apps (no estaba pedido, anotado).

## Reproducción

Scripts de la prueba (fuera del repo): `/private/tmp/claude-501/-Users-nahuelwagner/593a9195-2979-4426-aafa-e116c394af8d/scratchpad/{api.mjs,all.mjs,ui.mjs,drawers.mjs}`. SQL de sólo lectura sobre `information_schema` y `count(...)` en las tablas de la sección 1.
