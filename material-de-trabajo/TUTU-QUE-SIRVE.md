# Qué sirve del backend de Tutu para SPLG

Análisis del 23/09/2026 sobre `gearthlogic/tutu-dev/backend`.

**Tutu corre el mismo stack que SPLG**: NestJS + TypeORM + PostgreSQL + PostGIS +
Redis + Socket.io, más el cliente oficial de Google Maps. Verificado: cero
`mongoose` en su `package.json`, y `app.module.ts:79` declara `type: 'postgres'`.
Se puede portar tal cual, no hay que traducir nada de la persistencia.

**Pero SPLG ya está por delante en 3 de los 4 temas.** Tiene despacho secuencial
con ofertas durables y TTL, adapter Redis para Socket.io, redlock, idempotencia y
zonas de cobertura con `ST_Contains` scopeadas por distribuidora. Tutu no tiene
nada de eso. La cosecha real es chica y puntual.

## Lo que conviene traer

| Qué | Por qué | Esfuerzo |
|---|---|---|
| Columnas `floor` / `apartment` en `UserAddress` | Hoy el piso y el depto van embutidos en `street` o en `additionalInstructions`, texto libre que nadie puede consultar. En un reparto donde el cliente espera adentro, el piso es dato operativo | Bajo |
| Recargo **porcentual** en la zona, además del fijo | `surcharge` fijo se desactualiza con la inflación y obliga a reeditar zona por zona; un porcentaje no | Bajo |
| `tag` + `color` en la zona | El panel pinta cada zona con metadata del back en vez de inventar la paleta en el front | Bajo |
| `ST_AsGeoJSON(geom)::json` en el SELECT de zonas | Devuelve Features listos para el mapa, sin conversión en el front | Bajo |
| Estado "casi libre" del chofer | Un chofer con la última garrafa del reparto entra al próximo despacho sin esperar el confirm: menos hueco muerto entre pedidos | Bajo |
| **Geocoding y reverse-geocoding** al crear/editar una dirección | **SPLG no tiene geocoding** (verificado: cero dependencias de Google Maps). Hoy el lat/lng entra sin que nadie valide que corresponde a la calle escrita. El chofer llega a la puerta equivocada y el cliente está adentro de la casa | Medio |
| Mandarle al cliente **ETA y distancia** junto con la posición | El que espera la garrafa necesita "llega en 12 minutos", no un punto moviéndose. **Calculado en el servidor y cacheado**, nunca como Tutu (tres llamadas a Google por cada tick de GPS) | Medio |
| Vigencia temporal de la zona | Recargos por zona anegada, corte de calle, feriado. Con cron, no con `node-schedule` en memoria como Tutu, que se pierde al reiniciar | Medio |

## Lo que NO conviene traer

- **Coordenadas como texto.** Tutu guarda `"lat,lng"` en una columna `text` y la parsea con `split(',')`. Tira PostGIS a la basura. **SPLG arrastra una versión suave del mismo problema**: `UserAddress.latitude`/`longitude` son `varchar(50)`. Conviene ir para el otro lado y pasarlas a `geometry(Point,4326)` con índice.
- **Persistir la posición en Postgres en cada ping.** Tutu hace un SELECT + un UPDATE de la fila entera del chofer por cada actualización de GPS. SPLG ya usa Redis GEO, que es lo correcto.
- **Llamar a la Distance Matrix de Google en cada movimiento.** Tres requests por tick, costo lineal en la frecuencia del GPS y en la cantidad de choferes.
- **El registro de clientes conectados en memoria del proceso.** No sobrevive a más de una instancia. SPLG ya lo resolvió con el adapter Redis.
- **Rooms nombradas con un dato que manda el cliente.** Es el agujero que SPLG también tiene; ver abajo.
- **El tarifario doble por "demanda".** Cuenta usuarios conectados en memoria, no es geográfico, y en garrafas con precio regulado no tiene sentido cobrar más porque mucha gente abrió la app.
- **Todo lo atado a origen-destino**: peajes, tarifa por tramos, paradas intermedias, "vuelvo a casa". Un pedido de SPLG tiene un solo domicilio y el cliente no viaja.

## Lo que el análisis destapó en SPLG (no viene de Tutu)

El defecto de las salas por dato del cliente **lo tiene SPLG igual**, y se
verificó contra la API corriendo: ver H-51.
