# Dónde quedamos — 23/09/2026

Lo que se hizo hoy y lo que sigue. Se lee junto con `ESTADO-Y-PRIORIDADES.md`,
que tiene la foto completa del sistema.

**Compromiso:** presentar avances la semana que viene.

---

## Lo que quedó hecho hoy

### Backend — 23 commits en `fix/alineacion-nest`

| Qué | Cómo se verificó |
|---|---|
| **CU-011** — sólo el chofer asignado avisa la llegada, y el aviso también sale por push | Chofer ajeno 403, asignado 200, admin 200. El push se probó con token FCM registrado: falla, queda en el log y el endpoint igual responde 200 |
| **CU-020** — un chofer sólo mueve pedidos que ya son suyos | Antes: un chofer sin relación con el pedido lo ponía en entregado y recibía 200, y en efectivo quedaba dado por cobrado. Ahora 403 |
| **Salas de tiempo real** — se arman con el token, no con lo que manda el cliente | Con dos clientes reales: el ajeno ya no recibe nada, el legítimo sigue recibiendo lo suyo, y un chofer que reporta un id falso entra al radar con el id real de su token |
| **Cupo de acceso** — por cuenta además de por IP | Con una cuenta bloqueada, otra entra desde la misma IP. Variando el email, el corte llega en el intento 101 |
| **Colección de Postman** — carpeta nueva `02 · Recorrido del pedido` | Un pedido encadenado de punta a punta más el caso del chofer ajeno |

**Estado del backend:** 157 tests en verde, camino completo de la demo 19/19 en
tres corridas, 131 endpoints sin ninguno roto.

**Medido hoy, no supuesto:** el tracking en tiempo real entrega la posición al
cliente en **4 ms de promedio** (8 de 8 posiciones), y el despacho automático
ofrece el pedido y el chofer recibe la oferta.

### Documentación

- **CU-150 y CU-151** — vigencia temporal de las zonas de cobertura
- **CU-152 y CU-153** — registro de auditoría del sistema, más **IRQ-16**
- **Cinco CU existentes modificados**: CU-116 y CU-118 (resolución de la
  dirección contra el mapa, más piso y departamento), CU-056 (recargo
  porcentual, etiqueta y color), CU-013 (chofer "casi libre") y CU-017 (tiempo
  estimado de llegada junto con la posición)
- Los cuatro casos nuevos están en **los cuatro documentos de la cátedra**, con
  sus cinco artefactos cada uno, y el sitio publicado y verificado en vivo
- `material-de-trabajo` pasó de **31 documentos a 8**, con los cumplidos en
  `historico/`

---

## Lo primero para mañana

**Paso 1 de la lista: los DTO de respuesta.** De 21 módulos con controlador,
sólo 2 tienen DTO de respuesta (`order` y `auth`). Los otros 19 devuelven la
entidad de TypeORM cruda, así que el contrato de la API es "lo que tenga la
tabla": agregar una columna cambia la respuesta sin que nadie lo decida, y un
campo interno se filtra sin que nadie se entere.

Es lo más barato, lo más mecánico y lo que más cubre antes de que las apps se
acoplen a la forma de las tablas.

**Después**, en este orden: partir `order.controller.ts` (456 líneas) sin tocar
rutas ni respuestas; los bloques de datos que habilitan los módulos
inteligentes; el carrito; los módulos inteligentes; express y vigencia de zonas.

---

## Decidido hoy, pendiente de ejecutar

| Qué | Decisión | Cuándo |
|---|---|---|
| Mover el webhook de MercadoPago a `payments` | Hacerlo: hoy vive en `order`, que no tiene por qué saber de MercadoPago | Pendiente |
| Tabla de historial de estados del pedido | Hacerlo: hoy no queda registro de quién cambió un estado ni por qué | Pendiente |
| Módulo de auditoría (CU-152, CU-153) | **Especificado, no construido.** Alcanza a toda escritura, es de sólo lectura y depura credenciales | Pendiente |
| Sacar reservas a su propio módulo | **No**: una reserva es un pedido, el módulo nuevo dependería de `order` igual | Descartado |
| Módulo de chat | **No**: ningún CU lo pide y Reclamos ya cubre el problema con registro | Descartado |
| Módulo de almacenamiento (S3) | Más adelante. Cuando toque: puerto propio, como ya hace `payments` | Diferido |

### Del lado de los clientes — **no se tocó nada, como acordamos**

| Qué | Decisión |
|---|---|
| Botón "Nuevo Cliente" del panel | Sacarlo: ningún CU tiene alta de cliente por el administrador, y hoy da 404 |
| Pantalla de modificar pedido en la app cliente | Sacarla: no existe CU de modificar un pedido, y las rutas que llama dan 404 |
| Cancelar devuelve el 90% | **Regla nueva del 23/09.** Falta incorporarla a CU-008, que hoy no dice nada de reembolso. No se puede implementar hasta que esté la integración de cobro |

Lo que se creía que faltaba y **ya funciona**: mandar el pedido a una dirección
distinta de la del registro —comprarle a la madre, por ejemplo—. Verificado
contra la API.

---

## Cosas que conviene no olvidar

- **El watcher del backend se colgó** en medio de la sesión: estuve veinte
  minutos probando contra código viejo creyendo que el arreglo no funcionaba.
  Si algo no responde a un cambio, sospechar de eso primero y reiniciar.
- **El sitio no lee los diagramas del markdown**: los toma de archivos `.mmd`
  sueltos en `diagramas/`. Escribir el diagrama en `Casos-de-Uso.md` no alcanza.
- **`fix/alineacion-nest` no tenía upstream**: los 23 commits del backend
  estaban sólo en la máquina.
- Quedan **dos deudas de forma** en la documentación: los subsistemas aparecen
  con dos nombres distintos según la sección (SS-03, SS-04, SS-07, SS-08,
  SS-10), y `gateways` y `payments` no figuran en `app.module.ts` porque los
  importa `order.module.ts`.
