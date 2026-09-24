# Dónde quedamos — 24/09/2026

Se lee junto con `splg-app-backend/CONVENCIONES.md` (las reglas) y
`MODELO-DE-DOMINIO.md` (el modelo nuevo).

**Compromiso:** presentar avances la semana que viene.

---

## Lo que se hizo hoy

### Fase 0 — las bases, terminada

| Qué | Estado |
|---|---|
| Prettier sobre todo el código | Hecho, en un commit aparte |
| TypeScript `strict: true` | 339 errores → 0 |
| ESLint estricto (`any` y promesas sueltas prohibidos) | Activo; `common/`, `main.ts`, `app.module`, `adapters`, `redis` en 0. Lo de cada módulo se resuelve en su tanda |
| Migración inicial | `InitialSchema`: una base nueva se crea con `migration:run`. Verificado: esquema idéntico al de desarrollo |
| `CONVENCIONES.md` | Las reglas de Nest y TypeScript y la lista de **12 puntos de módulo terminado** |
| Bug real | El socket confirmaba la conexión antes de entrar a su sala |

### Modelos para la cátedra, rehechos

- Modelo de dominio en **8 contextos**, con los 153 CU. La **propuesta con
  vigencia** es el concepto común del despacho y los 4 módulos inteligentes.
- Modelo de datos completo: **37 tablas, 84 relaciones**; se declaran las 13
  relaciones sin FK.
- Actualizados el Doc 2 §1 (modelo conceptual) y el Doc 3 (tabla de
  faltantes). `verificar-conformidad.py` pasa en todo.

### Tanda 1 — módulos alineados

| Módulo | Qué cambió visible hacia afuera |
|---|---|
| `role` | Nada |
| `auth` | Nada en éxito. 401 de token inválido suma `statusCode` y conserva `code`. Se cortó el ciclo `auth ↔ users` (un guard corría dos veces en `/users`) |
| `gateways` | Nada. Identidad del socket tipada en `socket.data` |
| `customer` | Dejan de salir `notification_token` y `user.firebase_uid` (ningún cliente los lee) |
| `admin` | Dejan de salir `firebase_uid` y `uid` |
| `health`, `redis`, `firebase` | Ya cumplían; Firebase lee credenciales por `ConfigService` |

Cada uno: prueba unitaria, batería de Postman, comparación de forma de las
respuestas y sus DSD actualizados en las **tres copias**.

---

## Lo primero para mañana

1. **Terminar la tanda 1:** `incident`, `claims`, `rating`, `reports`.
2. **Revisar el comparador de formas:** no marcó `firebase_uid` en `GET /admin`
   ni en `POST /admin/register` aunque se sacó (verificado a mano). Entender
   por qué antes de seguir confiando en él.
3. **Tanda 2:** `distributor`, `payments` (mover el webhook de MP fuera de
   `order`), `car`, `cylinder`, `coverage-zone`, `time-slot`, `notifications`,
   `email`.
4. **Tanda 3:** `users`, `delivery`, `user-address`, `gascylinder`, `order` al
   final. Acá va el corte del ciclo `users ↔ customer ↔ email`: los registros de
   cliente y de chofer se mueven juntos a sus módulos (cambia CU-002 y CU-003).
5. **Pasada final:** propiedades a camelCase con `@Column({ name })` y renombres
   de archivos. Va al final porque recién ahí todo tiene DTO de salida.
6. Publicar el sitio.

## Cómo se trabaja un módulo

```bash
mkdir -p /tmp/splg-alineacion
cp splg-app-backend/scripts/alineacion/newman-base1.json /tmp/splg-alineacion/
splg-app-backend/scripts/alineacion/modulo.sh <modulo> src/<modulo>
```

Detalle en `splg-app-backend/scripts/alineacion/LEEME.md`. El back de prueba
corre en **:3100** porque el 3000 lo ocupa el MCP de Excalidraw.

## Hallazgos nuevos (en `HALLAZGOS.md`, sin corregir)

- **H-52 · ALTO:** un cliente se puede validar a sí mismo con
  `PATCH /customers/:id` `{"validated":"true"}`. Verificado contra la API.
- **H-53:** `/health` da 503 bajo la batería completa (umbral de 300 MB).
- **H-54:** el evento "en camino" se llama distinto en cliente y panel.
- **H-55:** la asignación manual no avisa al chofer por socket (revisar CU-012).

## Reglas acordadas hoy

- A rajatabla lo que pide Nest y TypeScript.
- No se cambia comportamiento; lo visible que cambie se escribe en el commit.
- Se conservan los nombres de clase que usan los DSD; los DSD que cambian se
  actualizan en las tres copias y se corre el verificador de la cátedra.
- La autorización según quién pide puede quedar en el controlador (así CU-086 y
  CU-087 no cambian); las invariantes del negocio van al servicio.
