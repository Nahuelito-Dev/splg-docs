# Informe de Hallazgos — Documentación contra Código

**Proyecto:** SPLG — Sistema de Pedidos y Logística de Garrafas de Gas
**Fecha:** 2026-08-30

---

## Qué es este documento

La especificación de casos de uso se redactó en mayo de 2026, antes de que el sistema
estuviera construido. El código evolucionó hasta agosto y la documentación no se actualizó.
Este informe recoge el contraste de cada caso de uso contra el código que lo implementa.

Los apartamientos se resolvieron de dos maneras. Cuando la documentación describía algo que
el sistema no hace, **se corrigió la documentación** para que describa el sistema real —esas
correcciones ya están aplicadas—. Cuando lo que falta es una función que conviene construir,
quedó registrada como limitación en el campo Comentarios del caso de uso correspondiente, y
se enumera acá para que sirva de plan de trabajo.

**Este informe no propone tocar el código.** Es el inventario de lo que se encontró.

---

## Resumen

De los 108 casos de uso, **54 requirieron corrección**. El desvío se concentra en los más
antiguos: los casos CU-001 a CU-060, escritos antes de construir el sistema, acumulan
34 de las 36 discrepancias graves. Los casos CU-061 a CU-104, redactados leyendo el código,
salieron fieles en 36 de 44.

| Tramo | Fiel | Discrepancia menor | Discrepancia grave |
|-------|-----:|-------------------:|-------------------:|
| CU-001 a CU-030 | 2 | 5 | 23 |
| CU-031 a CU-060 | 12 | 7 | 11 |
| CU-061 a CU-104 | 36 | 6 | 2 |
| **Total** | **50** | **18** | **36** |

---

## Hallazgos que comprometen la seguridad

Verificados uno por uno sobre el código.

| # | Hallazgo | Dónde | Consecuencia |
|---|----------|-------|--------------|
| 1 | `PATCH /delivery/:id` no declara `@Roles`, y el objeto de actualización admite `validated`, `isActive` y `distributorId` | `delivery.controller.ts:77`, `update-delivery.dto.ts` | Cualquier usuario autenticado puede habilitarse como chofer o cambiarse de distribuidora |
| 2 | Ningún punto de entrada verifica que el chofer sea el asignado al pedido | `update-order-status.use-case.ts` | Cualquier chofer puede marcar en camino, entregar y dar por cobrado el pedido de otro |
| 3 | Al aceptar un pedido no se comprueba que no tenga chofer | `update-order-status.use-case.ts:118` | Un segundo chofer desplaza al primero y regenera el código de entrega, invalidando su QR |
| 4 | La consulta de usuario por correo está expuesta sin autenticación | `users.controller.ts:54` | Se pueden obtener datos de usuario sin credenciales |
| 5 | La prueba de envío de correo está expuesta sin autenticación | `email.controller.ts:50` | Se pueden disparar envíos desde afuera. El propio código la marca como temporal |
| 6 | El bloqueo de usuario no impide nada | `users.service.ts:266` | El atributo se escribe pero no se lee en el ingreso ni en los guardas: un usuario bloqueado opera con normalidad |
| 7 | La habilitación del chofer no gobierna nada | `order.service.ts:265` | El único lugar donde se lee es un contador del panel; el despacho no la consulta |
| 8 | Fuga de aislamiento al asignar envases | `cylinder.service.ts:156` | El pedido se busca sin acotar por distribuidora: se pueden asignar envases propios a un pedido ajeno |
| 9 | Fuga de aislamiento al registrar incidencias | `incident.service.ts:27` | Ídem: la incidencia queda asentada bajo la distribuidora ajena |

## Hallazgos que comprometen los datos

| # | Hallazgo | Dónde | Consecuencia |
|---|----------|-------|--------------|
| 10 | La actualización de stock **suma** en lugar de fijar el valor | `gascylinder.service.ts:146` | Operar siguiendo la documentación anterior corrompía el inventario |
| 11 | Los errores de dominio se convierten en error interno | `create-order.use-case.ts:321` | La falta de stock devuelve 500 en lugar de 400: el filtro global nunca llega a mapearlos |
| 12 | La cancelación de pedido no es atómica | `cancel-order.use-case.ts` | La restitución de stock y el guardado corren en transacciones separadas |
| 13 | La asignación de envases no es atómica | `cylinder.service.ts:164` | Si falla a mitad, los anteriores quedan despachados con su movimiento registrado |
| 14 | Las promociones no validan su contenido | `order-pricing.service.ts:40` | Un descuento mayor a 100 produce un subtotal negativo |
| 15 | La baja de usuario es física, no lógica | `users.service.ts:183` | La documentación anterior prometía baja lógica |

## Funciones documentadas que no existen

| Función | Estado |
|---------|--------|
| Modificar una franja horaria | No existe la operación. Solo se puede crear, consultar y eliminar (CU-043) |
| Reactivar un producto dado de baja | Solo existe la desactivación; el atributo no es escribible (CU-040) |
| Estado "llegué" del pedido | El estado y su marca de tiempo no existen en el modelo (CU-019) |
| Aviso al cliente según el estado | El texto es siempre el de confirmación; el método con los textos correctos es código muerto (CU-021) |
| Credencial propia del sistema | La autenticación usa directamente el identificador del proveedor externo; no hay token propio (CU-001) |
| Manejo del pago rechazado | Está sin implementar; lo resuelve por descarte un proceso temporal media hora más tarde (CU-048) |

---

## Detalle completo

El contraste caso por caso, con la cita textual de la documentación anterior, el fragmento de
código que la refuta y su ubicación exacta, está en los informes de auditoría que acompañan a
este documento.

---

## Estado de la corrección

- **54 casos de uso reescritos** para que describan el sistema real.
- **12 diagramas corregidos**: tres de diseño que inventaban métodos inexistentes y modelaban
  una difusión a todos los choferes que el código ya no realiza, y nueve de secuencia con
  caminos alternativos que el sistema no contempla.
- **Las limitaciones detectadas quedaron registradas** en el campo Comentarios de cada caso de
  uso, de modo que la especificación indica tanto lo que el sistema hace como lo que le falta.
