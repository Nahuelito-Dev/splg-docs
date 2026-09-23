# Dónde estamos y qué sigue

Foto del sistema al **23/09/2026**, hecha contra el backend corriendo y no sobre
el código leído. Es el documento que se mira para decidir en qué trabajar.

---

## 1. Lo que anda

**131 endpoints probados con los cuatro roles reales: cero rotos.** 120 responden
correctamente, 10 rechazan aplicando una regla de negocio —que también es
funcionar— y 1 quedó fuera de la batería a propósito.

**20 de los 21 módulos tienen todos sus endpoints en pie.**

| Grupo | Endpoints |
|---|---:|
| Users, Customers, Delivery, Admin, Role, Auth | 45 |
| Orders | 19 |
| Gas Cylinders, Cylinders, Time Slots | 19 |
| User Addresses, Coverage Zones | 12 |
| Cars, Incidents, Claims, Ratings | 17 |
| Notifications, Email, Reports, Health | 14 |

El único incompleto es **Distributors**, 4 de 5.

### Flujos completos, verificados punta a punta

El recorrido de la demo cierra **19 de 19 pasos**, corrido tres veces seguidas:

registro de cliente desde la app → registro de chofer desde el panel → login de
los dos → alta de garrafa → dirección del cliente → pedido → el chofer consulta
el pool → asignación → aceptar → en camino → tracking → aviso de llegada →
código de entrega → confirmación → calificación.

### Medido, no supuesto

| Qué | Resultado |
|---|---|
| Tracking en tiempo real | 8 de 8 posiciones, **4 ms** de promedio (mínima 3, máxima 7) |
| Despacho automático (CU-013/014) | Ofrece al más cercano, el chofer recibe la oferta, vence a los 30 s |
| Varias direcciones por cliente | Anda; el pedido puede ir a la dirección de un tercero; usar una ajena da 404 |
| Cupo de acceso | Independiente por cuenta: bloquear una no deja afuera a las demás |
| Salas de tiempo real | Un cliente ya no puede escuchar el pedido de otro |

**116 de los 153 casos de uso andan y están verificados.**

---

## 2. Lo que hay que refactorizar

### Servicios y controladores largos

| Archivo | Líneas | Por qué molesta |
|---|---:|---|
| `order.controller.ts` | 456 | ABM, estados, tracking, despacho y entrega en un solo archivo |
| `order.service.ts` | 422 | Fachada que fue creciendo |
| `create-order.use-case.ts` | 413 | Quince dependencias en el constructor |
| `email.service.ts` | 329 | Plantillas y envío mezclados |
| `reservation.service.ts` | 291 | |
| `delivery`, `customer`, `users`, `cylinder`, `notifications` | 274–288 | En el límite |

Se parten por responsabilidad, no por cantidad de líneas: un servicio por cosa
que el módulo hace, y el resto pasa a llamarlo.

### El más importante, que no es de tamaño

De los **21 módulos con controlador, sólo 2 tienen DTO de respuesta** (`order` y
`auth`). Los otros 19 devuelven la entidad de TypeORM tal como sale de la base.

El contrato de la API pasa a ser "lo que tenga la tabla": agregar una columna
cambia la respuesta sin que nadie lo haya decidido, y un campo interno se filtra
sin que nadie se entere. Es la deuda que más conviene saldar antes de que las
apps se acoplen a la forma cruda de las entidades.

### Deuda puntual anotada

| Qué | Dónde duele |
|---|---|
| Coordenadas como `varchar(50)` | Sin PostGIS no se puede indexar ni consultar por cercanía |
| El chofer se identifica por `user_id` en el socket y por `delivery_id` en la asignación | Quien integra tiene que saber cuál va en cada llamada, y el contrato no lo dice |
| Sin geocoding | El punto de una dirección entra sin que nadie verifique que es esa calle |
| `driver:update-location` sin throttle | Cada posición: un GEOADD, un GET y dos emisiones. Crece lineal con los choferes en la calle |
| El miembro del radar GEO no vence | Si el proceso muere o el teléfono pierde señal sin cerrar el socket, el chofer queda en el radar con una posición vieja |

---

## 3. Lo que hay que construir

**28 casos de uso**, que no son 28 cosas sueltas sino **seis bloques**:

| Bloque | CU | Cuántos |
|---|---|---:|
| Carrito | CU-122 a CU-128 | 7 |
| Flota: seguros, verificación técnica, licencias, mantenimiento | CU-136 a CU-142 | 7 |
| Vigencia de envases | CU-132 a CU-135 | 4 |
| Consumo declarado y recompra | CU-143 a CU-146 | 4 |
| Entrega express | CU-147 a CU-149 | 3 |
| Vigencia de zonas de cobertura | CU-150, CU-151 | 2 |
| Modificar capacidad de franja horaria | CU-043 | 1 |

Más los **cuatro módulos inteligentes** (CU-105 a CU-108), que son el corazón de
la tesis.

---

## 4. El orden, y por qué

**Cuatro de esos seis bloques son los datos que los módulos inteligentes
necesitan para existir.** No son trabajo aparte de la tesis: son su cimiento. Hoy
M2 no se puede construir porque no hay dónde leer los vencimientos de la flota, y
M3 tampoco porque no existe el consumo declarado. Al revés no se puede.

| # | Qué | Por qué va acá |
|---|---|---|
| 1 | DTO de respuesta en los 19 módulos | Lo más barato y lo que más cubre: fija el contrato antes de que las apps se acoplen a la entidad cruda. Es mecánico |
| 2 | Partir `order.controller.ts` | Sin tocar rutas ni respuestas. La colección de Postman y el recorrido de 19 pasos son la red que avisa si algo cambió |
| 3 | Bloques de datos: flota, vigencias, consumo | Habilitan los módulos inteligentes |
| 4 | Carrito | Independiente de todo lo anterior |
| 5 | Módulos inteligentes | Con el colchón de las últimas semanas |
| 6 | Express y vigencia de zonas | Los menos críticos |

Las coordenadas a PostGIS conviene meterlas antes de que haya volumen, pero
pueden ir en cualquier punto: es una migración acotada.

---

## Cómo se trabaja

Reglas acordadas el 23/09, que aplican a todo lo de arriba:

- **El backend primero.** Panel y apps después, no en paralelo.
- **La fuente de verdad son los casos de uso**, no lo que hoy consumen los clientes.
- **Primero entender qué hace lo que está y cómo lo usan los clientes; después
  refactorizar sin cambiar el comportamiento.** No se rompe lo que funciona.
- **Nada se da por bueno sin probarlo contra la API corriendo**, y probándolo más
  de una vez.
- Lo que se encuentra mal **se anota** y se corrige de a uno, no sobre la marcha.
