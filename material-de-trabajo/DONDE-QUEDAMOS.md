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

## Avance del 24/09 a la noche (segunda sesión)

**Módulos alineados (21):** `health`, `redis`, `firebase`, `common`, `role`,
`auth`, `gateways`, `customer`\*, `admin`, `claims`, `incident`, `rating`,
`reports`, `distributor`, `time-slot`\*, `coverage-zone`, `car`, `cylinder`\*,
`notifications`.

\* Les queda un punto que va con `order` en la tanda 3: `customer` (alta de
clientes crea el User), `time-slot` (el cupo cuenta pedidos dentro de la
transacción del alta) y `cylinder` (lee el cliente del pedido). Los tres por
el mismo motivo: `order` ya depende de ellos y la lectura inversa armaría un
ciclo.

**Hallazgos corregidos:** H-52 (un cliente se validaba solo) y H-56 (el
informe por producto salía vacío). Anotados sin corregir: H-53, H-54, H-55,
H-57.

**Diagramas:** los DSD de flota (CU-136 a 142) y el diagrama de clases pasaron
al modelo Plan + Tarea; CU-021 al día con la identidad del socket. Los 304
diagramas pasan el parser de Mermaid 10.9.1 y el verificador de la cátedra.

## Lo que sigue

1. **Tanda 2, lo que falta:** `email` (ciclo con `users`, 41 errores de
   ESLint) y `payments` (mover el webhook de MercadoPago fuera de `order`).
2. **Decoradores compuestos** (`applyDecorators`): `@ApiBearerAuth` + `@Roles`
   + las respuestas de error se repiten en todos los controladores.
3. **Tanda 3:** `users`, `delivery`, `user-address`, `gascylinder` y `order`
   al final, con los tres pendientes marcados con \*.
4. **Pasada final:** camelCase con `@Column({ name })` y renombres de archivos.
5. Publicar el sitio.

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
