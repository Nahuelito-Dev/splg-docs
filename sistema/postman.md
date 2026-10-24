# Colección Postman de SPLG

Generada desde el OpenAPI del back (280 operaciones) y los controllers. No se edita a mano: se regenera con el script. Corre contra el back y la base de la demo (`http://localhost:3010/api`, distribuidora `demo`) sin crear distribuidoras ni cuentas, y deja lo que crea dado de baja o cancelado.

## Archivos

| Archivo | Qué es |
|---|---|
| `postman/SPLG.postman_collection.json` | La colección, con las respuestas reales guardadas como ejemplos. |
| `postman/SPLG-local.postman_environment.json` | El environment (`baseUrl`, usuarios de la demo y las variables que se llenan solas). |
| `scripts/postman/generar-coleccion.js` | Generador. Los roles de cada endpoint salen de los controllers (`roles-desde-controllers.js`); los cuerpos y flujos, de `casos.js`; la limpieza, de la tabla `LIMPIEZA` del generador. |
| `scripts/postman/guardar-ejemplos.js` | Pone en la colección las respuestas reales de una corrida de newman. |
| `scripts/postman/probar.js` | Corre newman sin la carpeta `Manual`. |

## Cómo importarla

1. Postman, Import, `postman/SPLG.postman_collection.json` y `postman/SPLG-local.postman_environment.json`.
2. Arriba a la derecha, elegir el environment **SPLG local**.
3. Revisar `baseUrl` (por defecto `http://localhost:3010/api`) y `choferLibreEmail` (un chofer de la demo sin pedidos en curso: `cristian.maidana@gmail.com`).
4. Correr la colección completa (Runner), dejando afuera la carpeta `Manual`.

Los usuarios son los de la demo: `admin@splg.com`, `superadmin@splg.com`, `cliente@splg.com` y `chofer@splg.com`, todos con `Test1234` (están en el environment). Los tokens se obtienen solos: el pre-request de la colección inicia sesión por rol cuando falta el token o venció.

## Orden de las carpetas

1. `00 · Acceso`: un login por rol.
2. `00 · Preparación`: lee los ids de la demo que hacen falta (cliente, chofer, catálogo, vehículo y ubicación del chofer libre, etc.) y deja el control de carga de camión en su valor por defecto.
3. `00 · Datos de prueba`: arma lo que comparten las pruebas, ver "Qué crea y cómo lo deja".
4. `00 · Errores documentados`: ejemplos 500 y 504 (el back no los produce a pedido) y 503 real.
5. `Manual`: ver abajo.
6. Una carpeta por recurso (tag del OpenAPI) y, adentro, una subcarpeta por endpoint.
7. `99 · Restauración`: cierra la corrida.

Cada subcarpeta trae, en orden: los pasos `Preparar ·` (crean los recursos propios de esa prueba: pedido, depósito, proveedor, etc.), el caso feliz, los casos de error y los pasos `Limpiar ·`. Por eso se puede correr un endpoint suelto (después de `00 ·`) y la corrida completa se puede repetir.

## Casos por endpoint

| Caso | Qué prueba |
|---|---|
| `200/201 · correcto` | Cuerpo válido con un rol permitido. Verifica status, que sea JSON, el tiempo y lo propio del endpoint (por ejemplo el total de la cotización o `cancelledBy`). |
| `400 · datos inválidos` | Cuerpo, parámetro de ruta o query inválido; verifica el `statusCode` y el `message` del filtro de excepciones. |
| `400 · sin Idempotency-Key` | Los 9 endpoints de stock, compras y cargas que la exigen (se detectan en el OpenAPI). Todas las escrituras mandan la clave. |
| `400 · super administrador sin X-Distributor` | Escrituras de pedidos y cobros, cotización e historial: el super admin tiene que mandar la distribuidora. |
| `401 · sin token` | Sólo en endpoints protegidos. |
| `401 · credenciales inválidas` / `401 · token inválido` | El 401 propio del login y el del token mal formado. |
| `403 · rol sin permiso` | Rol que el decorador `@Auth` del controller no admite. |
| `403 · recurso de otro usuario` | Un cliente pidiendo datos de otro cliente. |
| `404 · no existe` / `404 · <referencia> inexistente` | Id con formato válido que no existe, en la ruta o en el cuerpo. |
| `409`, `410` | La transferencia ya confirmada; el chofer que pide un pedido que ya no es suyo (`GET /orders/{id}` y `/status-history`). |
| `503 · dependencia caída` | `/health` y `/health/ready`. |

Cuando un caso no existe no se genera, no se relaja la expectativa: endpoints públicos (sin 401), endpoints abiertos a cualquier rol (sin 403), listados sin parámetros (sin 400), listados que con un id desconocido devuelven `200` vacío (sin 404) y texto libre sin validación (sin 400). El motivo de cada excepción está en `casos.js` (`no400`, `no404`, `sinExito`).

`POST /stock/reconciliation/adjustments` no tiene caso 201: sólo es posible con el vendible desalineado del físico y ninguna operación de la API lo produce. Se prueba el 400 "sin diferencia que corregir" con datos válidos.

`GET /routes/driving` acepta `200`, `502` y `503`: depende del proveedor de rutas (Google u OSRM). Sin proveedor configurado el back responde `503`, y eso es lo que pasa hoy en la demo.

## Qué crea y cómo lo deja

Todo lo que la colección crea lleva `Prueba API` en el nombre o en las notas y se da de baja al final de la carpeta que lo creó (la tabla `LIMPIEZA` del generador, en orden inverso al de alta): depósitos (después de dejarlos sin stock con un ajuste), proveedores, puestos, legajos, vehículos, garrafas, zonas, franjas, roles, direcciones y planes se dan de baja; pedidos, órdenes de compra, recepciones, cargas, tareas, reclamos, incidencias y envases se cancelan, anulan, cierran o retiran; las calificaciones se ocultan.

- **Stock de la demo:** las pruebas usan una garrafa propia (`Prueba API garrafa …`, carpeta `00 · Datos de prueba`). Las entregas de prueba descuentan del camión del chofer de esa garrafa propia, y al final se deja en cero y se da de baja. Los productos de la demo no se tocan.
- **Cuentas:** no se crea ni se modifica ninguna cuenta (Firebase es el real y está compartido). Registro, alta/edición/bloqueo/baja de usuarios y administradores, empleados con cuenta, mails, altas y bajas de distribuidoras y los tokens de notificación del cliente (`POST /notifications/token`, `/notifications/order-confirmation`) están en `Manual`.
- **Chofer libre:** `cristian.maidana@gmail.com` cambia de vehículo y se le arma una carga, y al terminar la prueba recupera el vehículo que tenía (el historial de asignaciones queda con las filas del cambio).
- **Lo que no se puede deshacer por API** y queda como historial: los pedidos entregados (alrededor de 9 por corrida; un pedido entregado no se cancela), los cancelados (alrededor de 20), los movimientos y ajustes de stock, las filas de auditoría y los productos, depósitos y cargas dados de baja (se ven en el historial de cada pantalla con su nombre `Prueba API`). Los pedidos entregados los hace el chofer `chofer@splg.com`, así que cuentan en la carga abierta de ese chofer.
- **Antes de una presentación:** la corrida deja historial de prueba en la distribuidora demo. Para volver a la demo limpia se vuelve a sembrar con el procedimiento de `back/DEMO.md` (backup, `npm run seed`, `seed:demo`, `fotos:demo`).

## Cómo provocar el 503

El back responde `503` en `/api/health` y `/api/health/ready` cuando Postgres o Redis no responden. En un entorno descartable: bajar el contenedor (`docker stop <postgres>` o `docker stop <redis>`), ejecutar `503 · dependencia caída` y volver a levantarlo. Con todo sano responde `200` y el caso lo acepta. El `500` y el `504` no se disparan a pedido: están como ejemplos guardados con el formato real de error del back.

## Carpeta Manual

Queda fuera de la corrida automática porque toca cuentas reales de Firebase, distribuidoras, dispositivos, mails, archivos o necesita un usuario nuevo:

- registro (`/auth/registro`, `/users/customer-registration`), alta de usuarios (`POST /users`), alta de administrador, cuenta de un empleado, egreso y reingreso de empleados;
- edición de usuarios (puede cambiar la contraseña), bloqueo, bajas de usuario, administrador, cliente y chofer;
- alta, edición y baja de distribuidoras (la baja da de baja a la sembrada si se usa su id);
- `POST /notifications/token` y `/notifications/order-confirmation` (pisan o usan el token de push del cliente real);
- `POST /stock/reconciliation/reapply-deliveries` (reaplica descuentos de stock sobre la demo);
- mails (`/email/*`);
- fotos, logos y adjuntos (multipart).

Correrlas a mano y con datos descartables, nunca con las cuentas ni la distribuidora de la demo.

## Newman

```bash
npm run postman:probar -- --base-url=http://localhost:3010/api --reporte=.orq/newman-reporte.json
```

Corre todo menos `Manual` (usa `npx newman@6.2.1`, no agrega dependencias).

## Regenerar

```bash
# lee el OpenAPI de la API levantada (la documentación pide Basic Auth)
SWAGGER_USER=... SWAGGER_PASSWORD=... npm run postman:generar          # colección + environment
npm run postman:probar -- --reporte=.orq/newman-reporte.json            # corrida contra la API levantada
npm run postman:guardar-ejemplos -- --report=.orq/newman-reporte.json   # pone las respuestas reales
```

Para leer el OpenAPI de un archivo: `node scripts/postman/generar-coleccion.js --input=ruta/openapi.yaml`.

`guardar-ejemplos` oculta tokens y firmas de URLs, recorta las listas a 3 elementos y conserva los ejemplos documentales 500, 503 y 504.

## Límites de la API que conviene saber

- Login: 8 intentos por minuto por cuenta. Correr la colección dos veces seguidas en menos de un minuto puede dar `429` en los logins.
- Las pruebas de camión y de vehículo usan al chofer `choferLibreEmail`; si ese chofer tiene un pedido en curso, el cambio de vehículo da `409`.
- Si algo externo cambia `requireOpenTruckLoad` a `true` durante la corrida, la asignación de pedidos falla con "El chofer no tiene la carga del día abierta"; `00 · Preparación` lo deja en `false` al empezar.
