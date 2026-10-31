# Novedades de la versión 2

La versión 2 de SPLG incorpora un conjunto de nuevas capacidades desarrolladas para optimizar la operatoria de distribución de gas, la gestión financiera y el control administrativo. La versión 1 del sistema quedó formalmente congelada el 24 de octubre de 2026 como línea base documentada de la tesis.

Todas las incorporaciones se estructuraron bajo el prefijo `/api/v2` de la interfaz HTTP y en las pantallas correspondientes del panel de administración y de las aplicaciones móviles, preservando compatibilidad estricta con la versión anterior y sin alterar los contratos vigentes de la versión 1.

A continuación se detallan las funcionalidades completadas y testeadas de punta a punta, organizadas por área operativa.

---

## Ventas y cobros

### Comprobantes de transferencia bancaria
Permite que los clientes que eligen abonar mediante transferencia bancaria visualicen los datos de la cuenta de la distribuidora (CBU, alias y titular) y adjunten el comprobante de pago desde la aplicación. El administrador revisa el comprobante antes de asentar la recepción del dinero, evitando confirmaciones a ciegas.
- **Dónde se ve:** En la app del cliente, en el detalle del pedido pendiente de pago (tarjeta «Pago por transferencia»); en el panel de administración, en los datos bancarios de la distribuidora y en el detalle de cada pedido, donde se ve y se confirma el comprobante.
- **Documentación técnica:** [back/TRANSFERENCIAS.md](back/TRANSFERENCIAS.md)

### Restricción de despacho para cobros con Mercado Pago impagos
Impide la asignación manual o automática de choferes a pedidos abonados con Mercado Pago mientras el cobro no se encuentre efectivamente aprobado en la pasarela de pagos. Evita el despacho de mercadería sin acreditación previa del importe (las reservas con seña abonada sí se habilitan para despacho).
- **Dónde se ve:** En el panel de administración, la acción «Asignar chofer» se muestra deshabilitada con su correspondiente motivo explicativo en los listados de pedidos, detalle del pedido y modales de asignación.
- **Documentación técnica:** [back/PEDIDOS.md](back/PEDIDOS.md)

### Gestión de clientes por distribuidora
Modela la relación entre el cliente de la plataforma y cada distribuidora de forma independiente. Permite dar de baja lógica el vínculo comercial de un cliente con una empresa específica sin alterar su cuenta global ni sus vínculos con otras distribuidoras, con capacidad de reactivación posterior.
- **Dónde se ve:** En el panel de administración, dentro del módulo **Clientes** (acción «Dar de baja», modal con confirmación contextualizada y nueva pestaña «Dados de baja» con opción «Reactivar»).
- **Documentación técnica:** [back/CLIENTES-DE-LA-EMPRESA.md](back/CLIENTES-DE-LA-EMPRESA.md)

---

## Caja y finanzas

### Caja integral, billeteras electrónicas y conciliación
Implementa un circuito financiero estricto donde todo cobro constituye un ingreso y todo desembolso genera un egreso en el libro diario contable. Admite cajas en efectivo con control de sesiones y arqueo, cuentas bancarias para transferencias y billeteras digitales (Mercado Pago), registrando automáticamente cobros, comisiones de pasarela, devoluciones y contracargos, junto con la conciliación frente a reportes de liquidación.
- **Dónde se ve:** En el panel de administración, en **Finanzas**: **Cajas**, **Movimientos**, **Cajas de cobro** (a qué caja entra lo cobrado por Mercado Pago y por transferencia), **Conciliación MP** (comparación con el reporte de liberaciones de Mercado Pago) e **Ingresos y egresos** (resultado de caja por período, categoría y caja). Los gastos de la flota (mantenimiento, neumáticos, siniestros, combustible) y las compras se pagan desde cualquier caja.
- **Documentación técnica:** [back/FINANZAS.md](back/FINANZAS.md)

---

## Flota

### Pólizas y cuotas de seguro automotor
Centraliza la administración de aseguradoras, pólizas vigentes por vehículo y cronogramas de cuotas mensuales. Facilita el pago derivando al enlace electrónico de la aseguradora, permite registrar el comprobante de pago con precarga de datos y asienta en forma automática el egreso correspondiente en Caja, sincronizando además el estado de vigencia en el plan de flota.
- **Dónde se ve:** En el panel de administración, en la pestaña **Seguro** de la ficha de cada vehículo (sección **Flota → Vehículos**), con historial de pólizas, cuotas del período, enlace de pago y registro de comprobantes.
- **Documentación técnica:** [back/SEGUROS.md](back/SEGUROS.md)

### Administración y pago de multas de tránsito
Permite asentar actas de infracción de tránsito vinculadas a vehículos y choferes, consultar el enlace y código de pago electrónico provisto por la entidad emisora, registrar el pago con comprobante e imputar el gasto automáticamente como egreso en la caja seleccionada.
- **Dónde se ve:** En el panel de administración, en **Flota → Multas** y en la pestaña **Multas** de la ficha de cada vehículo, con opciones «Pagar» y «Registrar pago».
- **Documentación técnica:** [back/FLOTA-AMPLIADA.md](back/FLOTA-AMPLIADA.md)

### Alertas de vencimientos de documentación de flota y personal
Notifica con anticipación configurable los vencimientos legales y técnicos críticos (como la VTV con 30 días de antelación o pólizas de seguro) y la falta de documentación obligatoria de los choferes habilitados. Los eventos se integran a la bandeja de entrada administrativa y se consolidan en el correo resumen diario de flota.
- **Dónde se ve:** En el panel de administración, mediante la campana de notificaciones, en **Notificaciones**, y en la pestaña **Documentación** del legajo de cada chofer o vehículo.
- **Documentación técnica:** [back/BANDEJA-ADMIN.md](back/BANDEJA-ADMIN.md)

---

## Auditoría y seguridad

### Auditoría integral mediante triggers en base de datos
Registra de manera inmutable y transparente en el motor relacional cada operación de inserción, actualización o baja lógica sobre 74 tablas del dominio de negocio. Captura usuario, fecha, hora, dirección IP, entidad afectada y valores anteriores y posteriores de cada campo modificado, así como sesiones e intentos de ingreso fallidos.
- **Dónde se ve:** En el panel de administración, en **Administración → Auditoría**, pestaña «Cambios de datos»: filtros por entidad, registro, autor, acción, origen (usuario, sistema o directo en la base) y fechas; el detalle de cada cambio con el valor anterior y el nuevo; y el exporte a CSV o Excel.
- **Documentación técnica:** [back/AUDITORIA.md](back/AUDITORIA.md)

### Control de sesiones en tiempo real y reconexión de sockets
Fortalece la capa de WebSockets revalidando credenciales contra la base de datos, cortando la conexión ante la baja o el bloqueo de un usuario, reconectando sin intervención cuando vence la sesión, y avisándole al chofer cuando cambia la dirección de un pedido asignado.
- **Dónde se ve:** Transparente en la app del cliente y en el panel web (reconexión sin intervención manual) y en la app del chofer (aviso del cambio de dirección o del acceso revocado).
- **Documentación técnica:** [back/TIEMPO-REAL.md](back/TIEMPO-REAL.md)

---

## Archivos y documentos

### Generación de documentos PDF en el backend
Produce remitos de entrega, recibos oficiales de cobro, rendiciones de choferes, liquidaciones de comisiones, balances de cierre de sesión de caja y resúmenes de ventas en formato PDF generado directamente en el servidor. Todos comparten el mismo encabezado y sólo los descarga quien tiene permiso.
- **Dónde se ve:** En el panel de administración, en las acciones del detalle de pedidos, rendiciones, liquidaciones, cierres de caja y reportes.
- **Documentación técnica:** [back/PDFS.md](back/PDFS.md)

### Exportación completa de datos en CSV y Excel
Habilita la descarga de la totalidad de registros que satisfacen los filtros de consulta (hasta un tope de 50.000 filas), superando las limitaciones de la paginación visual en pantalla. Genera archivos CSV estructurados con formato regional local y planillas Excel (.xlsx).
- **Dónde se ve:** En el menú «Más acciones» (tres puntos) de los listados del panel.
- **Documentación técnica:** [back/EXPORTES.md](back/EXPORTES.md)

### Importación masiva con validación previa
Permite dar de alta o actualizar en bloque garrafas, listas de precios, stock inicial por depósito y proveedores mediante la carga de archivos Excel o CSV. Ofrece plantillas descargables, valida exhaustivamente los datos fila por fila y presenta un reporte de inconsistencias antes de confirmar la transacción.
- **Dónde se ve:** En el menú de acciones de las pantallas de **Garrafas**, **Stock** y **Proveedores** («Importar garrafas», «Importar precios», «Importar stock» e «Importar proveedores»).
- **Documentación técnica:** [back/IMPORTACION.md](back/IMPORTACION.md)

### Soporte extendido para archivos adjuntos
Amplía los tipos de documentos admitidos para respaldar operaciones del sistema, incorporando formatos Word (.docx), Excel (.xlsx) y CSV además de imágenes y PDFs. Habilita la carga de comprobantes en rendiciones de choferes, movimientos de caja y cuentas corrientes comerciales.
- **Dónde se ve:** En el panel de administración, en las secciones de rendiciones, movimientos de caja y cuentas corrientes (sección o columna «Comprobantes»), con validación de tipo real de archivo e integración con almacenamiento seguro.
- **Documentación técnica:** [back/ADJUNTOS.md](back/ADJUNTOS.md)

### Almacenamiento seguro en Amazon S3 y catálogo fotográfico
Guarda las imágenes y los adjuntos en Amazon S3 y los entrega sólo con enlaces firmados que vencen. Suma fotografías a proveedores, envases y cargas del camión, y la demostración usa fotografías reales.
- **Dónde se ve:** En la carga y visualización de fotografías de proveedores, envases, comprobantes y cargas de camiones a lo largo de todo el panel administrativo.
- **Documentación técnica:** [back/S3.md](back/S3.md)

---

## Panel y avisos

### Bandeja centralizada de notificaciones administrativas
Consolida en un punto único todos los sucesos operativos que demandan atención de los administradores (reclamos de clientes, incidencias en reparto, transferencias pendientes, bloqueos de despacho o vencimientos). Evita avisos duplicados, se actualiza en tiempo real y algunos avisos también llegan por correo.
- **Dónde se ve:** En la barra superior del panel mediante el ícono de campana con contador de no leídos, y en la pantalla completa **Notificaciones**, con marcación individual o masiva de lectura y enlaces directos a cada caso.
- **Documentación técnica:** [back/BANDEJA-ADMIN.md](back/BANDEJA-ADMIN.md)

### Identidad visual con fotos de perfil
Reemplaza avatares genéricos de iniciales por fotografías reales de las personas registradas en el sistema en todas las vistas donde intervienen operadores, clientes o choferes, facilitando el reconocimiento visual rápido en la operatoria cotidiana.
- **Dónde se ve:** En las tablas y fichas de clientes, choferes y legajos, en los pedidos (cliente y chofer), en reclamos, incidencias, auditoría y en el menú del usuario.
- **Documentación técnica:** [back/S3.md](back/S3.md)

---

## Módulos inteligentes

### Módulo M2 — Mantenimiento predictivo y planificación de taller
Estima la fecha de vencimiento de las tareas de mantenimiento de los vehículos a partir del kilometraje diario real (calculado mediante recorridos de entrega y lecturas verificadas de odómetro). Planifica automáticamente ventanas de servicio en días y horarios de taller sin desabastecer la cobertura mínima de vehículos en cada zona de entrega, le propone el turno al chofer, que lo acepta o propone otro, y el administrador lo confirma; si no hay acuerdo, el caso pasa al administrador.
- **Dónde se ve:** En el panel de administración, en **Flota → Planificador de taller** (`/fleet/planner`), con visualización de estado de casos, proyecciones de kilometraje, ventanas sugeridas y confirmación de agendas; en la app del chofer, mediante notificación y pantalla específica para aceptar o sugerir fechas alternativas.
- **Documentación técnica:** [back/PLANIFICADOR-FLOTA.md](back/PLANIFICADOR-FLOTA.md)

### Módulos en desarrollo
Con posterioridad a la estabilización de los módulos M1 (despacho automático) y M2 (planificación predictiva de flota), se encuentran en etapa de desarrollo e integración los siguientes procesos automatizados:
- **Módulo M3 — Anticipación de recompra:** estima, por el consumo de cada cliente, cuándo se le termina la garrafa y lo invita a recomprar a tiempo.
- **Módulo M4 — Agrupación por recorrido:** Optimización de despachos consolidando pedidos geográficamente cercanos en una misma ventana de entrega.
- **Módulo M5 — Recuperación de envases:** seguimiento de los envases que quedan en manos de los clientes para recuperarlos.
