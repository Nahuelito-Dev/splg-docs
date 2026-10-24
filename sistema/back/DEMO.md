# Demo limpia: purga completa y datos nuevos

Cómo dejar `splg_db` (y la carpeta de la demo en S3) en un estado limpio, coherente y
realista, sin un solo dato de prueba visible. Repetible: se puede correr cuantas veces
haga falta y deja siempre el mismo resultado.

Piezas (todo en `scripts/`):

| Comando                | Qué hace                                                                                             |
| ---------------------- | ---------------------------------------------------------------------------------------------------- |
| `npm run cuentas:demo` | Cuentas: borra de Firebase las de prueba y pone nombre real a las de login. **Dry-run por defecto.** |
| `npm run seed`         | Roles, distribuidoras y cuentas con login (idempotente; no cambia nada si ya existen).               |
| `npm run seed:demo`    | **Purga** todo lo de la distribuidora y siembra la demo de Posadas.                                  |
| `npm run fotos:demo`   | Fotos de ejemplo en S3 para personas y legajos (el resto las sube `seed:demo`).                      |

## Orden exacto de comandos sobre `splg_db`

Desde la raíz de `splg-app-backend`. Todo en la misma terminal, con el `.env` que apunta a
`splg_db` y al bucket real:

```bash
set -euo pipefail
set -a; source .env; set +a      # DB_*, AWS_*, FIREBASE_* en la shell
```

**0. Antes de empezar.** Parar el back y el panel si están corriendo (no es obligatorio: la
purga va en una transacción, pero un usuario conectado vería la base cambiar).

**1. Backup (obligatorio): base + archivos de S3.**

```bash
scripts/demo-backup.sh
```

Hace `pg_dump -Fc` por `docker exec` (contenedor `DB_CONTAINER`, por defecto `splg-bd`; usuario
`DB_USERNAME`, por defecto `postgres`), **corta si el dump queda vacío**, y **copia** con
`aws s3 sync` los objetos de las carpetas de la demo (`gascylinders cars claims incidents
distributors users employees attachments fleet`) más un inventario del bucket. Si `AWS_S3_BUCKET` está
vacío, corta sin hacer nada; si la copia de S3 trae 0 objetos también corta (salvo `PERMITIR_S3_VACIO=1`). Deja todo en `~/backups-splg/<fecha>/` (`splg_db.dump`, `s3/`,
`s3-inventario.txt`, `MANIFEST.txt`) y te imprime la ruta. **Anotá esa ruta.**

**2. Cuentas: dry-run, leer, aplicar.**

```bash
npm run cuentas:demo
```

Imprime tres listas: lo que se **borraría de Firebase**, lo que se daría de baja **sólo en la
base** y las cuentas con login que se conservan (con su nombre nuevo). Reglas:

- En Firebase se borran **sólo** cuentas cuyo **correo** termina en `@splg-test.com`, sin
  excepciones ni listas. Nunca por nombre y nunca por patrones sin dominio (`qa.*`, `cobro.*`, `ajeno*` valen para cualquier dominio,
  incluidas personas reales: esas sólo salen de la **base**).
- Las demás cuentas "de prueba" (por nombre o patrón) se dan de baja sólo en la base.
- Primero se aplica la base, en una transacción; recién después se toca Firebase.

Si la lista de Firebase es la que querés:

```bash
CONFIRMAR_PROYECTO="$FIREBASE_PROJECT_ID" npm run cuentas:demo -- --apply
```

**3. Base de referencia (idempotente).**

```bash
npm run seed
```

**4. Purga y datos nuevos.** Mirá primero qué otras distribuidoras hay:

```bash
docker exec splg-bd psql -U "${DB_USERNAME:-postgres}" splg_db -c "SELECT slug, name FROM distributor"
```

```bash
SEED_S3=1 SEED_PURGE_S3=1 CONFIRMAR_DISTRIBUIDORAS=<slugs separados por coma> npm run seed:demo
```

- Con `SEED_SINGLE_TENANT=true` (por defecto) el seed **borra las otras distribuidoras**. Antes
  las lista con sus conteos (pedidos, productos, choferes, admins) y **se niega a seguir** si
  `CONFIRMAR_DISTRIBUIDORAS` no coincide exactamente con esos slugs. Sin otras distribuidoras no
  hace falta la variable.
- Las personas sin login que se quitan tienen un **alcance explícito**: las ligadas a la demo (o
  a las distribuidoras confirmadas) por pedidos o por perfil (chofer, administrador, legajo,
  vehículo) con su `distributor_id`, y las cuentas recién dadas de baja. Los usuarios sin login
  **huérfanos** (sin perfil ni pedidos en ninguna distribuidora) se **listan y no se tocan**; para
  quitarlos hay que repetir con `CONFIRMAR_HUERFANOS=<cantidad listada>`.
- Con `SEED_SINGLE_TENANT=false` no toca **nada** fuera de la distribuidora demo (ni su
  auditoría, ni sus personas, ni archiva usuarios).
- Con una sola distribuidora, las únicas cuentas con login que quedan son las 6 de la lista
  blanca (`scripts/lib/cuentas-demo.ts`); cualquier otra con `firebase_uid` sale de la demo
  (baja lógica y borrado en la base). Los cobros y la auditoría los firma `admin@splg.com`.
- Sin `SEED_S3=1` no sube ni borra ningún archivo; sin `SEED_PURGE_S3=1` no borra objetos.
- Se niega a correr si algo parece producción (`SEED_ALLOW_PRODUCTION=true` lo fuerza; no lo uses).
- Al final verifica la conciliación y **falla (código 1) si no cierra**; los objetos viejos de S3 se
  borran recién **después** de esa verificación.

**Si la siembra falla después de la purga:** la base queda vacía de datos de la demo (la purga
ya se confirmó) pero sin inconsistencias. Corré de nuevo el mismo comando: es seguro (la purga y
la siembra son repetibles) y los objetos viejos de S3 siguen ahí hasta que una corrida termine
bien. Si preferís volver atrás, restaurá el backup.

**5. Fotos de personas y legajos.**

```bash
SEED_S3=1 npm run fotos:demo
```

**6. Verificación** (sección siguiente) y levantar el back y el panel.

## Volver atrás (restauración)

```bash
set -a; source .env; set +a
CONFIRMAR_RESTAURAR=splg_db scripts/demo-restore.sh ~/backups-splg/<fecha>
```

- Antes de tocar nada compara el `MANIFEST.txt` con tu entorno y **corta** (mostrando los dos valores) si la base o el bucket no coinciden con `DB_NAME` / `AWS_S3_BUCKET`.
- Base: `pg_restore --clean --if-exists` por `docker exec -i` (pisa `splg_db`).
- S3: vuelve a subir los objetos copiados (`aws s3 sync` carpeta por carpeta). **No borra** lo que
  se haya subido después del backup; esos objetos quedan sin dueño (y el cron de huérfanos o una
  purga posterior los limpia).
- Las cuentas borradas de Firebase **no** vuelven.
- Para MinIO/otro endpoint: `AWS_S3_ENDPOINT` en el `.env` (los scripts lo usan).

## Qué hace la purga

`scripts/lib/purga-demo.ts`, **una sola transacción** (si algo falla, no queda nada a medias):

- Vacía, de la hoja a la raíz, todo lo que cuelga de la distribuidora: pedidos y sus renglones,
  historial de estados, pagos, ofertas, reclamos, incidencias, calificaciones, envases y su
  trazabilidad, recuperos, carritos, rutas, stock (libro, saldos, ubicaciones, depósitos,
  mínimos, ajustes), compras (proveedores, órdenes, recepciones), cargas del camión, personal
  y puestos, flota (vehículos, asignaciones, uso diario, mantenimiento), adjuntos, secuencias
  de numeración y auditoría.
- Con `SEED_SINGLE_TENANT=true` (por defecto) también quita las otras distribuidoras (Gas
  Andino), con confirmación explícita (ver arriba). Las cuentas de su staff conservan su usuario.
- Borra a las personas sembradas sin cuenta en Firebase (en modo multi-distribuidora, sólo las
  que trabajaron o pidieron únicamente en la demo). Si algo ajeno al seed referencia a una, no la
  borra: la archiva y lo informa.
- **El libro de stock y la auditoría son de sólo escritura para la aplicación** (un trigger
  rechaza `UPDATE` y `DELETE`). La purga del seed sí los vacía, porque reconstruye la demo; para
  eso desactiva esos triggers **dentro de su transacción** y los reactiva antes de confirmar
  (si algo falla, el rollback los deja como estaban). Eso no existe en la aplicación.
- `module_config` (qué módulos tiene activos la distribuidora) **no** se toca.
- Los usuarios con login (`firebase_uid`) no se borran: conservan su id y su cuenta.

**S3:** sólo se borran objetos que (a) la demo anterior dejó referenciados en la distribuidora
y (b) están bajo un prefijo **exacto**: `<carpeta>/<id de la distribuidora>/` con carpeta en
`gascylinders cars claims incidents distributors employees attachments fleet`, o
`users/<id>/` de las personas que se quitan. Una key de otro origen se deja y se avisa. Las
fotos se suben cifradas (SSE AES256) con EXIF limpio, y el remito de dos recepciones queda
como adjunto privado (`attachments/<distribuidora>/purchase_receipt/...`).

## Qué queda en la demo

Distribuidora Demo, Posadas (Misiones). Cantidades de una corrida real del seed:

| Módulo                   | Cantidad                                                         | Ejemplos                                                                                                                                                                                                           |
| ------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Catálogo                 | 5 garrafas                                                       | 5, 10, 15, 25 y 45 kg ($8.500 a $61.500), con promociones                                                                                                                                                          |
| Zonas / franjas          | 3 / 4                                                            | Centro, Villa Cabello, Itaembé Miní · Mañana, Mediodía, Tarde, Noche                                                                                                                                               |
| Clientes                 | 30 (+ direcciones geocodificadas 41)                             | Lucía Benítez (con login), Joaquín Martínez, Delfina Paredes; correos tipo `joaquin.martinez4@gmail.com`; unos pocos bloqueados, ninguno con pedidos abiertos                                                      |
| Choferes + vehículos     | 5 (+1 vehículo dado de baja)                                     | Ramón Villalba (con login, Toyota Hilux AF218KT), Cristian Maidana (Ford Ranger AE774PM), Sergio Insaurralde (Renault Kangoo AD391RS), Diego Ferreyra (Iveco Daily AB650LN), Walter Zaracho (Fiat Fiorino AG102VC) |
| Personal                 | 15 legajos, 6 puestos                                            | 6 choferes (uno dado de baja por renuncia), 3 ayudantes, 2 administrativas, 2 de depósito, 1 vendedora, 1 gerente                                                                                                  |
| Pedidos                  | 340 en 60 días                                                   | entregados ~296, cancelados ~35, y de hoy: 2 aceptados, 1 en camino, 3 pendientes, 3 reservas                                                                                                                      |
| Medios de pago           | efectivo, Mercado Pago, transferencia                            | efectivo cobrado por el chofer, cobros impagos resueltos por el admin (cobrado después o dado de baja), MP aprobado/rechazado, transferencias confirmadas y una por confirmar                                      |
| Reclamos / incidencias   | ~24 / ~15                                                        | "Garrafa con pérdida de gas", "Faltó una garrafa del pedido"                                                                                                                                                       |
| Calificaciones           | ~275                                                             | de clientes a choferes y de choferes a clientes                                                                                                                                                                    |
| Envases con trazabilidad | 210 envases, ~500 movimientos                                    | serie SPLG-00001...                                                                                                                                                                                                |
| Depósitos                | 2                                                                | Depósito central, Galpón Norte, con mínimos de stock                                                                                                                                                               |
| Stock                    | libro completo                                                   | conteo inicial, 296 entregas, 2 transferencias, 4 ajustes (fuga, hallazgo, rotura, corrección)                                                                                                                     |
| Proveedores              | 4                                                                | Gas del Litoral S.A., Fraccionadora Misionera S.R.L., Válvulas y Reguladores Posadas S.R.L., Transportes Alto Paraná S.A.                                                                                          |
| Compras                  | 7 órdenes, 4 recepciones                                         | recibida, **cerrada con faltante**, parcial, enviada, borrador y cancelada                                                                                                                                         |
| Cargas del camión        | 4                                                                | 2 rendidas, 1 rendida **con diferencia** (2 garrafas rotas), 1 **abierta del día** (Ramón Villalba)                                                                                                                |
| Flota                    | 4 planes, 23 tareas, 80 días de uso                              | service, VTV (una vencida), frenos, carnet profesional                                                                                                                                                             |
| Auditoría                | altas y un cambio de precio con valor anterior, más dos rechazos | visibles en el panel (CU-152/153)                                                                                                                                                                                  |

**Cuentas con login** (se conservan; el nombre es el de la base y el de Firebase):

| Correo               | Nombre                                                      |
| -------------------- | ----------------------------------------------------------- |
| superadmin@splg.com  | Nahuel Wagner                                               |
| admin@splg.com       | Marcela Duarte                                              |
| cliente@splg.com     | Lucía Benítez                                               |
| chofer@splg.com      | Ramón Villalba                                              |
| admin@gasandino.com  | Gustavo Paredes (sin perfil: la 2da distribuidora se quita) |
| chofer@gasandino.com | Héctor Acosta (sin perfil)                                  |

Contraseña de todas: la de siempre (`Test1234`, la fija `npm run seed`).

## Conciliación de stock

Todo el stock físico pasa por el libro (`StockLedgerService`), igual que en la aplicación:

- el conteo inicial entra por `stock inicial + reservadas + entregadas desde entonces`
  (`vendible: sin-cambio`);
- las entregas descuentan el físico sin tocar el vendible (ya se descontó al reservar);
- compras, ajustes y mermas mueven los dos a la vez.

Por eso `vendible − déficit = llenas − reservadas` para cada garrafa, y `GET
/stock/reconciliation` da `consistent: true` sin entregas sin movimiento. El seed lo calcula
al terminar e imprime la tabla; si no cierra, aborta.

## Verificación después de correrlo

```bash
# 1. Cero datos de prueba visibles (esperado: 0 filas en todas)
psql -h localhost -U "$DB_USERNAME" splg_db -c "
  SELECT 'user' t, count(*) FROM \"user\" WHERE full_name ~* '(prueba|test|e2e|ajeno|hola|postman)' OR email ~* '(splg-test|^qa\.|^prueba\.|^ajeno|^cobro\.|^qr-prueba)'
  UNION ALL SELECT 'gas_cylinder', count(*) FROM gas_cylinder WHERE type ~* '(prueba|test|e2e|postman)'
  UNION ALL SELECT 'car', count(*) FROM car WHERE car_model ~* '(hola|prueba)' OR car_patent = 'AA123BB'
  UNION ALL SELECT 'supplier', count(*) FROM supplier WHERE business_name ~* '(e2e|postman|prueba)'
  UNION ALL SELECT 'warehouse', count(*) FROM warehouse WHERE name ~* '(postman|prueba)'"

# 2. Conciliación (back levantado, token de admin)
curl -s -H "Authorization: Bearer <token>" -H "X-Distributor: demo" http://localhost:3000/stock/reconciliation | jq '.consistent'

# 3. Logins: admin, superadmin, cliente y chofer entran (panel y apps).
# 4. Firebase: ninguna cuenta activa quedó deshabilitada (Authentication > Users).
```

## Tests

`test/integration/seed-demo-limpia.e2e-spec.ts` corre el seed **dos veces seguidas** (y una
tercera después de `fotos:demo`) como proceso aparte contra Postgres y MinIO efímeros, con
toda la cadena de migraciones, sobre una base ensuciada a propósito (una fila de prueba en
**cada** tabla con `distributor_id`, cuentas de prueba, un objeto fuera del prefijo de la
demo). Verifica purga completa, cero texto de prueba en cualquier columna legible, el
servicio real de conciliación, que los usuarios con login se conserven con nombre real,
idempotencia (mismos conteos) y que S3 no quede con huérfanos ni toque lo ajeno.

```bash
npx jest --config ./test/jest-e2e.json --testPathPatterns=seed-demo-limpia
```

También cubre: la lista blanca de cuentas (ninguna con login archivada, superadmin con su fila en `admin`), la confirmación de `CONFIRMAR_DISTRIBUIDORAS`, el modo `SEED_SINGLE_TENANT=false` (no toca nada ajeno), la coherencia de la demo (fechas de envases, reservas, cancelados, bloqueos, auditoría, correos) y que `cuentas:demo` no borre de Firebase a `real2@gmail.com` ni `cobro.posadas@empresa.com`. No necesita Firebase (el borrado real de cuentas es `cuentas:demo`, aparte). Control de
mutación: sacar el `DELETE FROM "employee"` de `purga-demo.ts` hace fallar "ningún texto
visible…" y "segunda corrida"; cambiar el filtro de prefijo de S3 por `true` hace fallar
"segunda corrida".

## Variables del seed

| Variable                    | Por defecto | Para qué                                     |
| --------------------------- | ----------- | -------------------------------------------- |
| `SEED_DISTRIBUTOR`          | `demo`      | slug de la distribuidora                     |
| `SEED_CUSTOMERS`            | 30          | clientes (contando el que tiene login)       |
| `SEED_DRIVERS`              | 5           | choferes con vehículo y legajo (máximo 5)    |
| `SEED_ORDERS`               | 340         | pedidos repartidos en 60 días                |
| `SEED_SINGLE_TENANT`        | `true`      | quita las otras distribuidoras               |
| `SEED_S3` / `SEED_PURGE_S3` | —           | subir fotos / borrar las de la demo anterior |
