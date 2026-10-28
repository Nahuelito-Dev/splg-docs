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
| F15 | Multas: pago por link, comprobante leído, egreso en Caja y aviso en la bandeja | ⚪ Pendiente | 0 % | Necesita F10 y F12 |
| F16 | M2 — Flota predictiva | ⚪ Pendiente | 0 % | |
| F17 | M3 — Recompra | ⚪ Pendiente | 0 % | |
| F18 | M4 — Agrupación por recorrido | ⚪ Pendiente | 0 % | |
| F19 | M5 — Recupero de envases | ⚪ Pendiente | 0 % | |
| F20 | Documentación de la v2 y página «Novedades de la v2» | 🟡 En desarrollo | 30 % | |
| F21 | Colección de Postman de la v2 | ⚪ Pendiente | 0 % | |
| F22 | Capturas reales de las apps en la documentación | ⚪ Pendiente | 0 % | |
| F23 | Telegram: avisos de seguridad para el dueño del sistema | ⚪ Pendiente | 0 % | Pedido por nahue el 28/10. Falta definir qué avisos |
| F24 | WhatsApp: ventas por WhatsApp (pedidos y avisos al cliente) | ⚪ Pendiente | 0 % | Pedido por nahue el 28/10. Falta definir el circuito de venta y el número de WhatsApp Business |
| F25 | Auditoría total en la base (pedido de la cátedra): triggers en cada tabla que registran toda alta, cambio y baja (quién, cuándo, desde dónde, valor anterior y nuevo), sesiones e intentos de ingreso, y consulta en el panel con filtros y exporte | ⚪ Pendiente | 0 % | Pedido por nahue el 28/10: «todo, cada acción del sistema, ej. si un usuario pasa de chofer tipo A a chofer B». Hoy la auditoría de datos la hace la aplicación (subscriber), no la base |

## Arreglos menores anotados

- App del cliente: los íconos de la barra de estado se ven oscuros sobre el menú naranja.
- No se puede dar de baja al administrador de una distribuidora eliminada.
