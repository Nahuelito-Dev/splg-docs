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
| F2 | PDF generados en el back: remito, recibo, rendición, liquidación, comisiones y cierre de caja | 🟡 En desarrollo | 40 % | Back hecho con 5 observaciones de la revisión por corregir; falta el panel |
| F3 | Importación masiva (productos, clientes, stock y precios) con vista previa y errores por fila | 🟡 En desarrollo | 35 % | Back hecho; falta revisión, migración y panel |
| F4 | Comprobante de transferencia: el cliente lo sube, CBU/alias de la distribuidora y el admin lo ve | 🟡 En desarrollo | 50 % | Back en `develop`; faltan el panel y la app del cliente |
| F5 | Clientes de la empresa: alta, baja y reactivación | 🟡 En desarrollo | 50 % | Back en `develop`; falta el panel |
| F6 | Adjuntos: arreglar los tres tipos rotos (rendición, movimiento de caja, cuenta corriente) y aceptar Word y Excel | ⚪ Pendiente | 0 % | |
| F7 | Sockets: eventos que nadie escucha, revalidar la identidad y reconexión de la app del cliente | ⚪ Pendiente | 0 % | |
| F8 | Fotos en proveedores, envases y cargas de camión; fotos reales en la demo | ⚪ Pendiente | 0 % | |
| F9 | No permitir asignar a mano un chofer a un pedido de Mercado Pago impago | ⚪ Pendiente | 0 % | |
| F10 | Bandeja de notificaciones del admin: campana en el panel, aviso en vivo y por correo | ⚪ Pendiente | 0 % | Base de F11, F14 y F15 |
| F11 | Vencimientos de flota y personal por la bandeja: VTV 30 días antes con notificación y correo | ⚪ Pendiente | 0 % | Necesita F10 |
| F12 | Lector de comprobantes y documentos con IA (Claude): lee PDF y fotos y el admin confirma los datos | 🟡 En desarrollo | 40 % | Lector hecho en el back; falta la clave de la API y la prueba con un comprobante real |
| F13 | Documentos del vehículo: al subir el PDF se leen las fechas de vencimiento, la aseguradora y la póliza | ⚪ Pendiente | 0 % | Necesita F12 |
| F14 | Seguros: aseguradoras, póliza por vehículo, cuotas mensuales, pago por el link de la aseguradora, comprobante, egreso en Caja y recibo en la ficha del vehículo. Avisos: cuota 5 días y póliza 30 días antes | ⚪ Pendiente | 0 % | Necesita F10 y F12 |
| F15 | Multas: pago por link, comprobante leído, egreso en Caja y aviso en la bandeja | ⚪ Pendiente | 0 % | Necesita F10 y F12 |
| F16 | M2 — Flota predictiva | ⚪ Pendiente | 0 % | |
| F17 | M3 — Recompra | ⚪ Pendiente | 0 % | |
| F18 | M4 — Agrupación por recorrido | ⚪ Pendiente | 0 % | |
| F19 | M5 — Recupero de envases | ⚪ Pendiente | 0 % | |
| F20 | Documentación de la v2 y página «Novedades de la v2» | 🟡 En desarrollo | 30 % | |
| F21 | Colección de Postman de la v2 | ⚪ Pendiente | 0 % | |
| F22 | Capturas reales de las apps en la documentación | ⚪ Pendiente | 0 % | |

## Arreglos menores anotados

- App del cliente: los íconos de la barra de estado se ven oscuros sobre el menú naranja.
- No se puede dar de baja al administrador de una distribuidora eliminada.
