# Features nuevas de la v2

Todo lo que se agrega al sistema en la v2 de la API (`/api/v2`). Se desarrolla **en orden
secuencial**: una feature se termina completa (back, panel, apps si corresponde, documentación y
pruebas contra el sistema corriendo) antes de pasar a la siguiente.

Última actualización: 28/10/2026.

## Leyenda

| Estado | Qué significa |
|---|---|
| ⚪ Pendiente | No se empezó. |
| 🟡 En desarrollo | Hay trabajo hecho, pero falta alguna parte (back, panel, apps o documentación). |
| 🔵 Hecho | Completa en todas sus partes e integrada en `develop`. |
| 🟢 Hecho y testeado | Además, probada de punta a punta contra la API y el panel corriendo, con revisión cruzada. |

El **% de desarrollo** estima cuánto de la feature está construido, contando back, panel, apps y
documentación.

## Lista

| # | Feature | Estado | % | Detalle |
|---|---|---|---|---|
| F1 | Exportes completos (todas las filas) en CSV y Excel desde el back | 🟢 Hecho y testeado | 100 % | Back y panel en `develop`; probado contra la API y en el panel (escritorio y 320 px). Ver `sistema/back/EXPORTES.md` |
| F2 | PDF generados en el back: remito, recibo, rendición, liquidación, comisiones y cierre de caja | 🟢 Hecho y testeado | 100 % | Back, panel y apps (cliente: remito y recibo; chofer: rendición) en `develop`; probado contra la API, en el panel y en iPhone y Android. Ver `sistema/back/PDFS.md` |
| F3 | Importación masiva (garrafas, precios, stock y proveedores) con plantilla, vista previa y errores por fila | 🟢 Hecho y testeado | 100 % | Back y panel en `develop`; probado contra la API y en el panel. Los clientes no se importan: se registran solos. Ver `sistema/back/IMPORTACION.md` |
| F4 | Comprobante de transferencia: el cliente lo sube, CBU/alias de la distribuidora y el admin lo ve | 🟢 Hecho y testeado | 100 % | Back, panel y app del cliente en `develop`; probado de punta a punta (panel, iPhone y API). Ver `sistema/back/TRANSFERENCIAS.md` |
| F5 | Clientes de la empresa: alta, baja y reactivación | 🟢 Hecho y testeado | 100 % | Back y panel en `develop`; la baja es lógica y por distribuidora (el panel dejó de usar la baja de la cuenta entera); probado contra la API y la base. Ver `sistema/back/CLIENTES-DE-LA-EMPRESA.md` |
| F6 | Adjuntos: los tres tipos de dueño (rendición, movimiento de caja, cuenta corriente) y Word, Excel y CSV | 🟢 Hecho y testeado | 100 % | El back ya los soportaba (verificado contra la API); el panel acepta los tipos nuevos y suma adjuntos en rendición, caja y cuenta corriente. Ver `sistema/back/ADJUNTOS.md` |
| F7 | Sockets: eventos que nadie escucha, revalidar la identidad y reconexión de la app del cliente | 🟢 Hecho y testeado | 100 % | Back, panel y las dos apps: corte por token vencido y por bloqueo/baja, origen limitado, avisos de toda incidencia y de reclamos, sin el alias duplicado; el panel y la app del cliente reconectan, el chofer rehace la ruta si cambia la dirección. Ver `sistema/back/TIEMPO-REAL.md` |
| F8 | Fotos en proveedores, envases y cargas de camión; fotos reales en la demo | 🟢 Hecho y testeado | 100 % | Back (v2) y panel en `develop`; probado contra la API (otra empresa 404, chofer 403/404, v1 sin la ruta) y en el panel. La demo quedó sin figuras generadas: fotos de Wikimedia con licencia libre y auditadas. Ver `sistema/back/S3.md` |
| F9 | No permitir asignar a mano un chofer a un pedido de Mercado Pago impago | 🟢 Hecho y testeado | 100 % | Una sola regla en el back: el pedido MP impago no se ofrece, no figura en disponibles, no se acepta ni se asigna (409); la reserva con seña paga sí sale. Arregla además el despacho común, que los ofrecía. Panel: asignar apagado con el motivo en todas las pantallas. Ver `sistema/back/PEDIDOS.md` |
| F10 | Bandeja de notificaciones del admin: campana en el panel, aviso en vivo y por correo | 🟢 Hecho y testeado | 100 % | Back (v2, avisos guardados sin repetir, lectura por admin, socket y mail opcional a admins activos) y panel (campana con lo guardado y página «Notificaciones»). Base de F11, F14 y F15. Ver `sistema/back/BANDEJA-ADMIN.md` |
| F11 | Vencimientos de flota y personal por la bandeja: VTV 30 días antes con notificación y correo | 🟢 Hecho y testeado | 100 % | Cada vencimiento («por vencer» y «vencido») y cada documento faltante de chofer entra a la bandeja; el mail sigue siendo el resumen diario (VTV 30 días antes). Arregla que un vencimiento ya avisado no volviera a avisar al vencer; el faltante lleva a la pestaña Documentación del legajo. Ver `sistema/back/BANDEJA-ADMIN.md` |
| F12 | Lector de comprobantes y documentos con IA (Claude): lee PDF y fotos y el admin confirma los datos | 🟡 En desarrollo | 40 % | Lector hecho en el back; falta la clave de la API y la prueba con un comprobante real |
| F13 | Documentos del vehículo: al subir el PDF se leen las fechas de vencimiento, la aseguradora y la póliza. Foto de la patente: se guarda aparte y se lee para avisar si no coincide con la cargada | ⚪ Pendiente | 0 % | Necesita F12. La patente hoy es sólo texto (validada y única por distribuidora) |
| F14 | Seguros: aseguradoras, póliza por vehículo, cuotas mensuales, pago por el link de la aseguradora, comprobante, egreso en Caja y recibo en la ficha del vehículo. Avisos: cuota 5 días y póliza 30 días antes | 🟢 Hecho y testeado | 95 % | Back y panel en `develop`, probado de punta a punta. El comprobante se escanea solo al subirlo; falta probar el escaneo real cuando la API tenga crédito (F12). Ver `sistema/back/SEGUROS.md` |
| F15 | Multas: pago por link, comprobante leído, egreso en Caja y aviso en la bandeja | 🟢 Hecho y testeado | 100 % | Back 4df559f (`/api/v2/traffic-fines`: enlace y código de pago, comprobante de dueño propio escaneado al subirlo, pago con egreso desde efectivo/banco/billetera, avisos por la bandeja con mail), panel 56daa82 (Pagar y Registrar pago en la multa y en la ficha del vehículo). Probado contra la API y en Chrome. Escaneo real pendiente del crédito de la API de Claude |
| F16 | M2 — Flota predictiva | ⚪ Pendiente | 0 % | |
| F17 | M3 — Recompra | ⚪ Pendiente | 0 % | |
| F18 | M4 — Agrupación por recorrido | ⚪ Pendiente | 0 % | |
| F19 | M5 — Recupero de envases | ⚪ Pendiente | 0 % | |
| F20 | Documentación de la v2 y página «Novedades de la v2» | 🟡 En desarrollo | 30 % | |
| F21 | Colección de Postman de la v2 | ⚪ Pendiente | 0 % | |
| F22 | Capturas reales de las apps en la documentación | ⚪ Pendiente | 0 % | |
| F23 | Telegram: avisos de seguridad para el dueño del sistema | ⚪ Pendiente | 0 % | Pedido por nahue el 28/10. Falta definir qué avisos |
| F24 | WhatsApp: ventas por WhatsApp (pedidos y avisos al cliente) | ⚪ Pendiente | 0 % | Pedido por nahue el 28/10. Falta definir el circuito de venta y el número de WhatsApp Business |
| F25 | Auditoría total en la base (pedido de la cátedra): triggers en cada tabla que registran toda alta, cambio y baja (quién, cuándo, desde dónde, valor anterior y nuevo), sesiones e intentos de ingreso, y consulta en el panel con filtros y exporte | 🟢 Hecho y testeado | 100 % | Pedido por nahue el 28/10. Back 363a74a + exporte 5acc09d (triggers en 74 tablas, sesiones, inmutabilidad, rol `splg_mantenimiento`, `/api/v2/audit/entries` con filtro de origen), panel 9bf7a81 (filtro Origen, Sesión, origen técnico, 74 entidades en castellano), doc `sistema/back/AUDITORIA.md`. Probado contra la API y en Chrome |
| F26 | Foto de perfil en todo el panel: donde aparece una persona (clientes, choferes, legajos, usuarios, pedidos, reclamos, incidencias, «En uso por», campana, historial) se ve su foto y no sólo las iniciales | 🟢 Hecho y testeado | 100 % | Pedido por nahue el 28/10. Back c086608 (`POST /api/v2/people/photos`, aislamiento por distribuidora probado contra la base y con mutación, no ensucia la bitácora), panel d69462a (`PersonAvatar` en tablas, fichas, historiales y menús). Sin foto posible (el dato no trae la persona): Reservas, Movimientos de stock, eventos de la campana, ventas por chofer, cargas de camión |
| F27 | Caja completa: todo gasto es egreso y todo cobro es ingreso. Billetera Mercado Pago de la distribuidora (ventas aprobadas entran solas; pagos con MP salen de ahí, con la comisión de MP aparte), transferencias confirmadas entran a la cuenta del banco, VTV/service/tareas/neumáticos/siniestros con su costo salen de la caja elegida, combustible y multas también por banco o billetera, y tablero de ingresos y egresos por período, caja y vehículo | 🟡 En desarrollo | 80 % | Por etapas. Hechas: multas (F15); gastos de flota y compras desde efectivo/banco/billetera con el reintegro del seguro como ingreso (back 89dde88, panel 5a566a6); ventas cobradas por Mercado Pago, transferencias y señas como ingreso, con comisiones, devoluciones y contracargos como egresos (back a8ef06c, panel 9de3ed6). conciliación de la caja de Mercado Pago con el reporte de liberaciones (back 663f958, panel 67feca1; el reporte real se pide bien, falta verlo generado con una cuenta con movimientos). Falta: tablero de ingresos y egresos |
| F28 | Relevamiento de transacciones en la base: en cada operación del sistema, dónde corresponde una transacción explícita (commit y rollback), dónde conviene un procedimiento almacenado y dónde un trigger; documentarlo para la cátedra y aplicar lo que falte | ⚪ Pendiente | 0 % | Pedido por nahue el 30/10, para cuando terminen las demás F |
| F29 | Artefactos del Proceso Unificado de las features nuevas: CU, CUE, CUA, DSS y DSD de cada una, en UML 2.5 como el resto de los casos de uso, y su lugar en los documentos de la cátedra | ⚪ Pendiente | 0 % | Pedido por nahue el 30/10: se hace al final, cuando estén todas las F |

## Arreglos menores anotados

- App del cliente: los íconos de la barra de estado se ven oscuros sobre el menú naranja.
- No se puede dar de baja al administrador de una distribuidora eliminada.
