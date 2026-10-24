# Guion de la demo — 30/09/2026

Unos 15 minutos: qué es SPLG, cómo está documentado y el sistema funcionando.
El orden va de lo general a lo concreto: landing → documentación → panel.

## Antes de empezar (5 minutos antes)

| Qué | Dónde | Chequeo |
|---|---|---|
| Landing | http://localhost:4321 | carga la portada |
| Documentación | http://localhost:8090/splg-documentacion.html (o https://splg-atlas.netlify.app) | abre la portada con "El viaje de un pedido" |
| Panel | http://localhost:3001 | entrar con `admin@splg.com` / `Test1234` y dejar abierto el Tablero |
| API de demo | http://localhost:3020/api (base `splg_demo`, limpia) | el panel muestra datos (si el Tablero sale vacío, el back no está arriba) |

La base de demo (`splg_demo`) es aparte de la de desarrollo: tiene 25 clientes, 4 choferes
con vehículo, 180 pedidos de los últimos 90 días, reclamos, incidencias y 190 envases, sin
los datos de las baterías de prueba.

Tener las cuatro pestañas abiertas en ese orden. Cerrar notificaciones y dejar el
navegador en pantalla completa. El superadmin (`superadmin@splg.com`) sólo si
preguntan por la plataforma multi-distribuidora.

## 1. Qué es SPLG — landing (2 min)

- **Qué decir:** SPLG es un sistema para distribuidoras de gas envasado. El
  cliente pide la garrafa desde una app, el pedido se despacha solo al chofer
  más cercano disponible, se sigue en vivo y la distribuidora administra todo
  desde un panel web. Es multi-distribuidora: la misma plataforma sirve a varias
  empresas, cada una aislada.
- **Qué mostrar:** portada, la sección de qué resuelve y los planes. Aclarar que
  la landing es el material comercial, no está publicada todavía.

## 2. Cómo está documentado — sitio de la documentación (5 min)

- **Portada — "El viaje de un pedido":** el recorrido completo de un pedido de
  punta a punta. Sirve para contar el sistema en un minuto.
- **"La documentación en números":** los entregables del Proceso Unificado
  (Plan del Proyecto, Planificación de Iteraciones, Requisitos, Análisis y
  Diseño), 108 casos de uso con sus cuatro artefactos (caso de uso, caso de uso
  extendido, diagrama de secuencia del sistema y de diseño) y la matriz de
  trazabilidad.
- **Abrir un caso de uso real** (por ejemplo CU-001 o CU-012, despacho): mostrar
  el caso, su diagrama de secuencia y cómo baja al diseño. Los 10 CU Reales
  (001, 005, 008, 013, 014, 015, 017, 020, 048 y 079) son los que tienen el
  circuito completo con pantalla construida; el criterio es propio.
- **Diseño:** modelo de datos, arquitectura y los módulos inteligentes
  especificados (planificación de flota, recompra, agrupación por recorrido,
  recupero de envases), que se implementan al final del plan.
- **Si preguntan por el proceso:** páginas de Ramas y Versionado (GitFlow,
  releases automáticas al integrar a `main`).

## 3. El sistema funcionando — panel (7 min)

Recorrido sugerido, siguiendo el menú lateral:

1. **Tablero:** pedidos del día, ventas y el gráfico con datos reales de la base.
2. **Pedidos:** filtrar por estado y buscar un cliente. Abrir la ficha de un
   pedido: renglones, pago, dirección, chofer y el recargo de zona desglosado.
   Mostrar la gestión (cambiar estado o asignar a mano).
3. **Seguimiento en vivo:** los pedidos en camino sobre el mapa.
4. **Zonas de cobertura:** el mapa con los polígonos, crear o editar una zona y
   explicar el recargo fijo o porcentual por zona.
5. **Choferes y vehículos:** habilitar o deshabilitar un chofer (la habilitación
   del admin es independiente de que el chofer esté en línea) y la ficha del
   vehículo. *Si ya está integrada la pantalla de documentación de flota:*
   documentos con vencimiento, adjuntos y la pantalla de Vencimientos.
6. **Envases:** trazabilidad de cada garrafa física (dónde está, quién la tiene,
   su historial).
7. **Posventa:** reclamos e incidencias y cómo se resuelven desde el panel.
8. **Reportes y Auditoría:** ventas por producto, por medio de pago y por chofer;
   el registro de auditoría de quién hizo qué.

**Idea fuerza para cerrar el recorrido:** todo lo que se ve sale de la API real
y de la base; nada está maquetado.

## 4. Cierre (1 min)

- Qué está hecho: API completa del circuito del pedido, panel al día con la API,
  documentación completa según la plantilla de la cátedra.
- Qué sigue: apps del cliente y del chofer (reconexión en tiempo real), módulos
  inteligentes y despliegue.

## Si algo falla en vivo

| Síntoma | Qué hacer |
|---|---|
| El panel no carga datos | Seguir con la documentación publicada en https://splg-atlas.netlify.app y contar el panel con el recorrido de la portada |
| Error al guardar algo | No reintentar en vivo: pasar al siguiente punto del recorrido |
| Se cierra la sesión | Volver a entrar con `admin@splg.com` / `Test1234` |

## Preguntas probables

- **¿Por qué el admin de una distribuidora no edita las direcciones del cliente?**
  Porque un cliente puede comprarle a varias distribuidoras: si una cambiara su
  dirección o su cuenta, afectaría a las otras. Lo administra el administrador
  general (hallazgos H-66 y H-73).
- **¿Cómo se elige el chofer?** Despacho automático: se ofrece al más cercano
  disponible y habilitado; si no acepta en el tiempo límite, pasa al siguiente.
  El admin también puede asignar a mano.
- **¿Qué pasa con un vehículo con la documentación vencida?** La documentación
  de flota tiene vencimientos y avisos diarios por correo; un documento
  inhabilitante vencido deja al vehículo o al chofer inhabilitado.
- **¿Cómo se aíslan las distribuidoras?** Cada consulta se acota por la
  distribuidora del usuario; está verificado con una batería de pruebas entre
  distribuidoras.
