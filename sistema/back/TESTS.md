# Tests del Backend SPLG

## Estructura

```
test/
├── integration/                     # Tests de integración E2E
│   ├── setup/
│   │   └── test-env.ts              # Bootstrap: Postgres+Redis en Docker
│   ├── health.e2e-spec.ts           # GET /health, /health/live, /health/ready
│   ├── orders-stock-concurrency.e2e-spec.ts  # CU-005 race condition
│   └── redlock.e2e-spec.ts          # Distributed locks
├── performance/
│   └── orders-load.ts               # Load test del POST /orders con autocannon
└── jest-e2e.json                    # Config de Jest para tests e2e
```

## Pre-requisitos

**Docker corriendo.** `testcontainers` levanta Postgres + Redis efímeros automáticamente. Si no tenés Docker, los tests de integración no van a correr.

```bash
docker info  # debe responder OK
```

## Cómo correr cada tipo de test

### Tests unitarios (mocks, rápidos)

```bash
npm test                # corre todos los .spec.ts
npm run test:watch      # modo watch
npm run test:cov        # con cobertura
```

### Tests de integración (Docker requerido)

```bash
# Todos los de integración (corre en serie, lento la primera vez por imagen)
npm run test:integration

# Individuales
npm run test:integration:health
npm run test:integration:concurrency   # ⭐ el crítico: oversell prevention
npm run test:integration:redlock
```

**Primera ejecución:** ~2-3 min (descarga imágenes `postgres:16-alpine` + `redis:7-alpine`).
**Siguientes:** ~30-60s.

### Tests de performance

```bash
# 1. En una terminal: levantar el backend
npm run start:dev

# 2. Hacer seed manual de Customer + Address + GasCylinder vía Postman
#    o usando el módulo Seed del proyecto. Anotar los UUIDs.

# 3. Exportar los UUIDs y correr el test
export PERF_CUSTOMER_ID="<uuid>"
export PERF_ADDRESS_ID="<uuid>"
export PERF_CYLINDER_ID="<uuid>"
npm run test:perf:orders
```

**Salida esperada:**

```
🎯 Apuntando a http://localhost:3000/orders
⏱️  Duración: 30s, Conexiones: 50

📊 RESULTADOS
───────────────────────────────────────────
Total requests:    1452
Throughput:        48.4 req/s
Errores:           0
Timeouts:          0
Non-2xx:           48

Latencia (ms):
  p50  → 412
  p90  → 980
  p97  → 1340
  p99  → 1580
  avg  → 487.32
  max  → 2104
───────────────────────────────────────────
✅ Todos los targets NFR-02 cumplidos
```

## Qué valida cada test

| Test                                   | Qué valida                                         | Falla si...                                          |
| -------------------------------------- | -------------------------------------------------- | ---------------------------------------------------- |
| `health.e2e-spec.ts`                   | `/health` responde 200 con DB+Redis OK             | health check no detecta caídas de Redis              |
| `orders-stock-concurrency.e2e-spec.ts` | El pessimistic lock previene oversell              | hay race condition de stock (≥ 2 ventas con stock=1) |
| `redlock.e2e-spec.ts`                  | Acquire concurrente devuelve null si otro lo tiene | el lock distribuido no funciona                      |
| `orders-load.ts` (perf)                | p95 < 5s, throughput > 20 req/s, errores < 1%      | el endpoint no cumple NFR-02                         |

## Cobertura por concepto auditado

| Concepto                            | Test que lo valida                                      |
| ----------------------------------- | ------------------------------------------------------- |
| Pessimistic locks (Día 1)           | `orders-stock-concurrency.e2e-spec.ts`                  |
| Health checks (Día 2)               | `health.e2e-spec.ts`                                    |
| Distributed locks / Redlock (Día 3) | `redlock.e2e-spec.ts`                                   |
| Idempotencia (Día 4-5)              | _pendiente_ — agregar `orders-idempotency.e2e-spec.ts`  |
| Workers + Queues (Día 6-8)          | _pendiente_ — agregar `notifications-queue.e2e-spec.ts` |
| Performance                         | `orders-load.ts`                                        |

## Troubleshooting

**"Cannot connect to Docker daemon"**
→ Arrancá Docker Desktop o el daemon antes de correr `test:integration`.

**Test hangs por > 3 min**
→ Probablemente Docker está descargando una imagen por primera vez. Esperá.
Para acelerar futuras corridas, las imágenes quedan cacheadas.

**Pessimistic concurrency test falla con stock != 0**
→ El lock no está funcionando. Revisar `OrderService.create()` en `order.service.ts:96-105`.

**Redlock test devuelve 2 locks adquiridos**
→ El Redlock está mal configurado. Revisar `RedisService.onModuleInit()` y `acquireLock()`.
