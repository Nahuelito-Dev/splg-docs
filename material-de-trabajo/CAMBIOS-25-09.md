# Cambios del 25/09/2026 que tiene que reflejar la documentación

Fuente: commits de `splg-app-backend` en la rama `fix/alineacion-nest` del 25/09
y `HALLAZGOS.md` (H-77 a H-87). Todo verificado contra la API corriendo.

## A. Aislamiento entre distribuidoras (H-77 a H-84)

Regla: con una distribuidora en contexto (la del admin de empresa, la del chofer,
o la que eligió el super admin con "ver como"), lo de otra distribuidora **no
existe**: el sistema responde que no lo encontró (404), sin revelar que existe.
El control está en el controlador, antes de operar, con un método del servicio
dueño (`OrderService.assertDeLaDistribuidora(id, distributorId)`,
`CustomersService.assertDeLaDistribuidora`, `UserAddressService.assertDeLaDistribuidora`,
`DeliveryService.assertAlcance`). El cliente no se acota por distribuidora: su
control es que el recurso sea suyo.

Endpoints y CU afectados:

| CU | Qué cambió |
|---|---|
| CU-008 Cancelar Pedido (Cliente) | Si el pedido no es del cliente: **no encontrado (404)**, y el control va ANTES de mirar el estado (antes respondía 400 "No autorizado" después de revelar si estaba en camino). |
| CU-009 Cancelar Pedido (Chofer) | Pedido de otra distribuidora: no encontrado. **Sólo el chofer asignado** puede liberarlo (403 si no): antes cualquier chofer de la misma empresa liberaba el pedido de otro (H-79). |
| CU-010 Cancelar Pedido (Administrador) | Pedido de otra distribuidora: no encontrado. |
| CU-012 Asignar Chofer Manualmente | Pedido de otra distribuidora: no encontrado. El chofer tiene que ser **de la misma distribuidora que el pedido** (si no, "Repartidor no encontrado", 404). |
| CU-015 Aceptar Pedido | Pedido de otra distribuidora: no encontrado. El chofer que acepta tiene que ser de la misma distribuidora que el pedido. |
| CU-016 Rechazar / Ignorar Pedido | Pedido de otra distribuidora: no encontrado. |
| CU-018 Marcar Pedido "En Camino" (y demás cambios de estado por PATCH /orders/:id/status) | Pedido de otra distribuidora: no encontrado. |
| CU-019 Avisar Llegada al Cliente | Pedido de otra distribuidora: no encontrado. |
| CU-078 Obtener el Código de Entrega | Pedido de otra distribuidora: no encontrado (antes un admin de otra empresa leía el código). |
| CU-079 Confirmar Entrega Escaneando el QR | Pedido de otra distribuidora (para un admin): no encontrado. |
| CU-081 Consultar los Pedidos Asignados al Chofer | Un chofer sólo consulta los suyos: si pide los de otro chofer, 403. |
| (PATCH /orders/:id/location, ubicación del chofer sobre el pedido) | Pedido de otra distribuidora: no encontrado; sólo el chofer asignado (403). Buscar el CU que lo describe (probablemente CU-017). |
| CU-032 Validar / Invalidar Chofer, CU-033 Activar / Desactivar Chofer, CU-049 (saldo, PATCH /delivery/:id/balance), CU-097 Eliminar Chofer, CU-017 (PATCH /delivery/:id/location) | Chofer de otra distribuidora: no encontrado (H-80). |
| CU-096 Actualizar Perfil del Chofer (PATCH /delivery/:id) | Además: **sólo acepta `validated` e `isActive`**; cualquier otro campo (correo, contraseña, nombre, calificación) es rechazado (400). Los datos de la persona se cambian por PATCH /users/:id. |
| CU-093 Validar / Invalidar Cliente, CU-094 Actualizar Ubicación del Cliente, CU-129 Consultar Detalle del Cliente, CU-130 Buscar Cliente por Usuario, CU-131 Editar Datos del Cliente | Para un admin: si el cliente nunca le compró a su distribuidora, no encontrado (H-81). |
| CU-095 Eliminar Cliente (baja lógica) | Cliente que no le compró a su distribuidora: no encontrado. Y **la baja de un cliente la hace sólo el Administrador General** (403 para el admin de empresa): un cliente puede comprarle a varias distribuidoras. |
| CU-046, CU-117, CU-121 (consultas de direcciones) | Para un admin de empresa: direcciones de un usuario que no es de su distribuidora, no encontrado. |
| CU-116, CU-118, CU-119, CU-120 (alta, edición, baja, predeterminada de direcciones) | Para un admin de empresa: no encontrado si el usuario no es de su distribuidora, y 403 si lo es: **las direcciones las administra el cliente o el Administrador General**. |
| CU-023 Registrar Reclamo | Un admin de empresa no registra reclamos sobre pedidos de otra distribuidora (no encontrado). |
| CU-060 Registrar Incidencia | Pedido de otra distribuidora: no encontrado. **El chofer sólo reporta sobre el pedido que tiene asignado** (403). |
| CU-062 Consultar Incidencias de un Pedido | Pedido de otra distribuidora: no encontrado (antes devolvía una lista vacía). |
| CU-099 Consultar los Tokens de un Usuario | Los tokens de OTRO usuario sólo los ve el **Administrador General** (antes cualquier admin). |
| CU-101 Reenviar Notificación de Confirmación | Sólo el **Administrador General** (antes cualquier admin). También el envío de prueba de notificación. |
| CU-087 / alta de perfil de administrador (POST /admin) | El perfil de admin toma el rol **del usuario**: el usuario tiene que tener rol admin o super_admin, distribuidora sólo para admin de empresa, un perfil por usuario (409). Ya no recibe role_id (H-77). Buscar qué CU lo describe. |
| Búsqueda de admin por correo o id (GET /admin/term/:term) | Admin de otra distribuidora: no encontrado (H-84). Buscar el CU. |

## B. Baja lógica (H-74)

Nada que el sistema haya usado se borra físicamente: queda con fecha de baja,
deja de aparecer y se conserva para el historial y la auditoría.

| CU | Qué cambió |
|---|---|
| CU-085 Eliminar Usuario (baja lógica) | Antes borraba la fila y la cuenta de Firebase (o 409 si tenía pedidos). Ahora: baja lógica del usuario **y de su perfil de cliente o chofer, sus vehículos y sus direcciones**; la cuenta de Firebase se **deshabilita** (no se borra): no puede volver a entrar (su ingreso responde 401 "La cuenta no está habilitada") y el correo sigue ocupado. Ya no existe el 409 por pedidos asociados. Si deshabilitar en Firebase falla, la baja igual queda hecha y se registra en el log. |
| CU-112 Eliminar Vehículo | Baja lógica. La patente se puede volver a registrar (única sólo entre vehículos vigentes). |
| CU-059 Eliminar Zona de Cobertura | Baja lógica; la validación de cobertura (CU-058) ignora las zonas dadas de baja. |
| CU-119 Eliminar Dirección de Entrega | Baja lógica: los pedidos que la usaron la siguen mostrando. |
| Historiales (pedidos, incidencias, reclamos, calificaciones, informes) | Siguen mostrando el chofer, el cliente o la dirección aunque estén dados de baja. |

## C. Stock (refactor de order, sin cambio de comportamiento salvo H-85)

- La reserva y la devolución de stock las hace `GasCylinderService` (dueño de
  `gas_cylinder`): `reservarStock(manager, gasCylinderId, cantidad)` y
  `restituirStock(manager, items)`, dentro de la transacción del pedido y con
  lock pesimista. **Ya no existe `StockReservationService`.** Los DSD que lo
  nombran (crear pedido CU-005, cancelar CU-008/CU-010, expirar reservas y
  pedidos MP CU-077 y el cron de reservas) tienen que nombrar `GasCylinderService`.
- `CreateOrderUseCase` ya no lee repositorios ajenos: el cliente con
  `CustomersService.buscarComprador(userId)`, la dirección con
  `UserAddressService.buscarDelUsuario(addressId, userId)`.
- `UpdateOrderStatusUseCase`, `OrderService` y `DispatchOrchestratorService` leen
  choferes con `DeliveryService` (`buscarPorIdOUsuario`, `findById`,
  `contarDisponibles`, `choferesDeLaDistribuidora`) en lugar de un repositorio de
  Delivery. En los DSD, el participante "RepositoryDelivery" pasa a ser
  `DeliveryService`.
- **H-85 (CU-005 Crear Pedido):** pedir más que el stock disponible responde 400
  "Stock insuficiente para <producto>", y un producto inexistente 404 "Garrafa no
  encontrada"; antes los dos respondían 500 "Error al crear el pedido".

## D. Normalización

- CU-093: la validación del cliente es sí/no (booleano), ya no un texto.
- CU-094, CU-017: la ubicación se guarda como punto geográfico (PostGIS); la API
  sigue recibiendo "latitud,longitud" y **rechaza (400) lo que no sea un par de
  coordenadas válido**.
- CU-039 Configurar Promociones: cada promoción es una fila propia (desde N
  unidades, descuento en %), única por producto y cantidad; **dos promociones
  para la misma cantidad se rechazan (400)**; la cantidad mínima es 2 y el
  descuento entre 0 y 100.
- CU-116 / CU-118 Direcciones: **ya existen los campos piso, departamento, id del
  lugar en el mapa y precisión** (exacta, aproximada, sin resolver; por defecto
  sin resolver). **Sigue pendiente** la resolución automática contra el servicio
  de mapas. Latitud y longitud se cambian juntas (400 si viene una sola).
- Perfil de administrador: ya no guarda el rol; es el del usuario.

## E. Auditoría (CU-152 y CU-153) — IMPLEMENTADOS

- CU-153: un interceptor global registra en `audit_log` cada POST, PUT, PATCH y
  DELETE que pasa la autenticación, exitoso o rechazado: quién (usuario y rol),
  distribuidora, recurso e identificador, ruta (el patrón, sin datos personales),
  aplicación de origen, IP, resultado, código HTTP, motivo del rechazo y el cuerpo
  **depurado** (contraseñas, tokens y el código de entrega quedan como
  "[depurado]"). Se guarda sin demorar la respuesta; si la base lo rechaza, la
  operación no se cae y queda en el log. Lo que un guard rechaza (sin credencial o
  sin rol) no se registra. La base impide modificar o borrar asientos (trigger);
  sólo deja vaciar el autor o la distribuidora cuando éstos se borran.
- CU-152: `GET /audit` (admin y super admin) con filtros por persona, recurso,
  identificador, resultado y período, del más reciente al más viejo, paginado. Un
  admin de empresa ve sólo lo de su distribuidora.
- Clases: `AuditInterceptor`, `AuditService` (registrar, consultar),
  `AuditController`, entidad `AuditLog`.

## F. Otros

- CU-084 Verificar Existencia de Usuario: informa el correo y el teléfono por
  separado; antes marcaba el correo como usado aunque coincidiera sólo el teléfono.
- GET /users/email/:email y /users/phone/:phoneNumber validan el parámetro (400).
- Las respuestas de usuarios y choferes ya no incluyen el identificador de
  Firebase ni el token de notificaciones.
- H-86 y H-87 (reconexión del socket en las apps) siguen ABIERTOS: si algún CUE de
  tiempo real lo menciona, puede agregarse como comentario "todavía no".
