# Revisión de la especificación de módulos

> Contraste de la sección "Especificación de módulos" del documento de entrega
> contra los 23 módulos registrados en `src/app.module.ts`.
>
> Fecha: 2026-08-27.

---

## 1. La clasificación "Funcionales / No Funcionales" está mal aplicada

En ingeniería de requisitos, **no funcional** no significa "de soporte": designa
un **atributo de calidad** del sistema (rendimiento, seguridad, disponibilidad,
usabilidad, escalabilidad, mantenibilidad). No son módulos, son propiedades.

Los cinco módulos listados hoy como "no funcionales" —Usuarios y Autenticación,
Notificaciones, Reportes y Dashboard, Gestión de Choferes y Vehículos, Auditoría
y Logs— **son funcionales**: tienen actores, casos de uso y resultados
observables. "El administrador valida un chofer" es un requisito funcional.

Ejemplos de requisitos no funcionales asociados, para contrastar:

- *El sistema debe autenticar en menos de 2 segundos.*
- *Las contraseñas deben almacenarse con hash bcrypt.*
- *El despacho debe soportar N instancias concurrentes.*

### Corrección propuesta

| Título actual | Título correcto | Módulos |
|---|---|---|
| Funcionales | **Módulos de negocio (core)** | Pedidos, Catálogo y Stock, Despacho y Asignación, Seguimiento en Tiempo Real, Reclamos, Pagos, Franjas Horarias, **Envases**, **Zonas de Cobertura**, **Incidencias**, **Calificaciones** |
| No Funcionales | **Módulos de soporte (transversales)** | Usuarios y Autenticación, Notificaciones, Reportes y Dashboard, Gestión de Choferes y Vehículos, Auditoría y Logs, **Distribuidoras (multi-tenant)** |

Cambiando los dos títulos y reubicando, el problema se resuelve sin reescribir
las descripciones.

---

## 2. Módulos que existen y no están listados

Comparación contra `app.module.ts`:

| Módulo | Módulo NestJS | Por qué debe figurar |
|---|---|---|
| **Envases (ciclo del envase)** | `CylinderModule` | **Construido completo**: máquina de estados, historial de movimientos auditable, pantalla en el panel y tarjeta en la app chofer. Es el diferencial del rubro y el soporte del módulo inteligente 5 |
| **Zonas de Cobertura** | `CoverageZoneModule` | Activo. Soporte de los módulos inteligentes 2 y 4 |
| **Incidencias** | `IncidentModule` | Activo, y distinto de Reclamos |
| **Calificaciones** | `RatingModule` | Activo. Calificación bidireccional cliente ↔ chofer |
| **Distribuidoras** | `DistributorModule` | Base del multi-tenant: sostiene que el producto sea un SaaS para varias distribuidoras y no una app de un solo negocio |

> El módulo de **Envases** es el más urgente de incorporar: el módulo inteligente
> de recuperación de envases se apoya en él, y sin el módulo funcional listado
> queda sin sustento.

Los módulos restantes de `app.module.ts` (`RedisModule`, `FirebaseModule`,
`EmailModule`, `HealthModule`, `RoleModule`) son infraestructura y no
corresponden a una especificación funcional.

---

## 3. Descripciones que no coinciden con el código

| Módulo | El documento dice | El código hace |
|---|---|---|
| Despacho y Asignación | "reintenta la asignación cada minuto ampliando el radio hasta 15 km" | Cada **15 segundos**; radios `[5, 10, 15, 20]` km |
| Pagos | "recargo del 10% para pagos por transferencia" | `applyPaymentSurcharge()` lo aplica a **MercadoPago y transferencia**. Fue el hallazgo P0-5 de la revisión de arquitectura y se resolvió unificando la regla |
| Catálogo y Stock | "se restituye si el pedido es cancelado" | **No siempre.** `applyCancellationPolicy()` decide según el actor: si cancela el chofer, el stock no se restituye y el pedido vuelve a PENDING para redespacho |
| Pedidos | "PENDIENTE → ACEPTADO → EN CAMINO → ENTREGADO / CANCELADO" | Falta **RESERVED**: pre-reserva con seña y fecha agendada; el cron la activa el día pactado (RESERVED → PENDING) |

---

## 4. Correspondencia con los módulos inteligentes

Cada módulo inteligente necesita que su módulo funcional de soporte esté
declarado:

| Módulo inteligente | Se apoya en | Estado |
|---|---|---|
| 1 · Negociación secuencial de asignación | Despacho y Asignación | Listado |
| 2 · Planificación predictiva de flota | Gestión de Choferes y Vehículos (**a extender con mantenimiento y habilitaciones**) + Zonas de Cobertura | Parcial |
| 3 · Anticipación de recompra | Pedidos, Clientes | Listado |
| 4 · Agrupación de pedidos por recorrido | Zonas de Cobertura + Franjas Horarias | Parcial |
| 5 · Recuperación de envases | **Envases** | **No listado** |

---

## 5. Acciones

1. Renombrar los dos títulos de la clasificación (§1).
2. Incorporar los cinco módulos faltantes (§2), priorizando Envases.
3. Corregir las cuatro descripciones (§3).
4. Extender la descripción de Gestión de Choferes y Vehículos para incluir
   mantenimiento y habilitaciones, si va el módulo inteligente 2.
