# Dónde quedamos — 24/09/2026 (cierre)

Se lee junto con `splg-app-backend/CONVENCIONES.md` (las reglas y los 12 puntos
de "módulo terminado") y `MODELO-DE-DOMINIO.md` (el modelo nuevo).

**Objetivo:** dejar las bases del backend alineadas a rajatabla con Nest y
TypeScript estricto, seguras y escalables, para desarrollar la tesis encima.

**Ramas:** backend en `fix/alineacion-nest`; panel y app de clientes en
`feature/alta-unificada`; docs en `develop`. Todo commiteado y pusheado.

---

## Estado de los módulos del backend

Medido sobre el código el 24/09 a la noche: lint = errores de ESLint estricto
(`any` y promesas sueltas prohibidos), pruebas = archivos `.spec.ts`.

### Terminados: cumplen Nest + TypeScript estricto

DTO de entrada y de salida, mapper explícito, `@Auth`, cada módulo dueño de sus
tablas, sin `forwardRef`, sin `process.env`, lint en 0 y prueba unitaria.

| Módulo | Pruebas | Nota |
|---|---|---|
| `role`, `auth`, `admin`, `claims`, `incident`, `rating`, `distributor`, `coverage-zone`, `car`, `notifications`, `email`, `payments`, `user-address` | sí | `auth`, `email`, `notifications` y `payments` no devuelven entidades: sus DTO se arman directo |
| `registro` (nuevo) | sí (25) | El alta única de todos los roles, con la política de quién crea qué |
| `reports` | sí | Excepción documentada: lee entidades ajenas, sólo lectura (CQRS) |
| `health`, `redis`, `firebase`, `gateways`, `common`, `adapters` | parcial | Infraestructura; `common` usa `process.env` sólo en las fábricas de config, como permite la convención |
| `customer`, `time-slot`, `cylinder` | sí | Terminados salvo un punto cada uno que depende de `order` (ver tanda 3) |

### A medias: funcionan y son seguros, falta alinearlos

| Módulo | Qué falta |
|---|---|
| `users` | Devuelve la entidad sin mapper, errores de lint heredados, sin pruebas. Seguridad y aislamiento entre distribuidoras ya resueltos (H-62, H-63, H-65, H-66, H-73, H-75, H-76) |
| `delivery` | Devuelve la entidad sin mapper. Lint en 0 y seguridad corregida (H-61, H-64) |
| `gascylinder` | Sin mapper, 3 errores de lint, sin pruebas |

### A refactorizar

| Módulo | Qué tiene |
|---|---|
| `order` | 221 errores de lint, controlador de 456 líneas, 5 entidades ajenas registradas, 2 `process.env`. Es el último de la tanda 3 y cierra los pendientes de `customer`, `time-slot` y `cylinder` |

### A hacer (no existe todavía o es transversal)

| Tema | Detalle |
|---|---|
| Normalización del modelo de datos | Análisis formal tabla por tabla: dependencias funcionales, 1FN a FNBC, 4FN y 5FN, y justificación de cada desnormalización. Candidatos ya vistos: `admin.role_id` repite `user.role_id`; `lat_lang`/`latLng` guardan "lat,lng" en un texto; `customer.validated` es texto y `delivery.validated` booleano |
| Soft delete y auditoría (H-74) | Sólo 4 de 20 entidades tienen borrado lógico; 6 borrados físicos (el peor, `DELETE /users/:id`); no hay registro de quién creó, modificó o borró. **Falta recuperar lo acordado la noche del 23/09 sobre la auditoría** |
| Pasada final | camelCase con `@Column({ name })` y renombres de archivos (`isPublic.decorator.ts`, `timeout.interceptors.ts`) |
| Documentación | Swagger completo del back (todas las respuestas y errores); mejorar la web y rehacer el visor de imágenes; publicar el sitio. Los `.svg`/`.png` de `diagramas/` son del primer commit y nunca se regeneraron: el sitio no los usa, pero están viejos |
| `.env.example` | No existe: falta para levantar el proyecto desde cero |
| Barrido de aislamiento entre distribuidoras | `users` ya cumple. Falta probar **todos** los endpoints de los demás módulos con dos distribuidoras (admin A contra datos de B), como se hizo con `users`. Pendiente conocido: `PATCH /customers/:id` (validar un cliente) cambia un dato compartido entre distribuidoras |
| Panel: acciones sobre clientes | Un admin de empresa ya no puede editar, bloquear ni resetear la contraseña de un cliente (403). El panel todavía le muestra esos botones: hay que ocultarlos según el rol |
| Módulo de auditoría | Pedido de la cátedra: registrar qué pasa en el sistema (quién cambió qué y cuándo). Va con soft delete (H-74) |
| Reportes | nahue pidió un módulo de reportes: ya existe `reports` (ventas por distribuidora); definir si es ampliarlo o uno nuevo |

---

## Lo que se hizo el 24/09

**Seguridad** (cada punto verificado contra la API, con commit propio): H-58,
H-59, H-61 a H-65, H-67 a H-70, H-73, H-75. Los críticos:

- **H-70:** un alta repetida borraba de Firebase la cuenta de quien ya existía.
  Sin token, cualquiera dejaba afuera a cualquier usuario, super admin incluido.
- **H-73:** un admin de empresa podía cambiarle el correo a un usuario de otra
  distribuidora y así entrar como esa persona.
- **H-63 / H-62:** cualquiera podía darse de alta como super admin, y un admin
  de empresa podía volverse super admin.

**Alta unificada de usuarios:** las seis altas (cliente desde la app, chofer y
cliente desde el panel, usuario base, admin y primer super admin) pasaron a un
solo caso de uso, `RegistroService`, con dos puertas: `POST /auth/registro`
(pública, siempre cliente, 10 por minuto por IP) y `POST /users` (panel, rol en
el cuerpo). El primer super admin se crea con `npm run crear-superadmin` desde
el servidor. Resolvió H-71 (el panel no podía crear clientes) y H-72 hacia
adelante (altas sin cuenta de acceso).

**Documentación de las altas:** CUA, CUE, DSS y DSD de CU-002, 003, 031, 082,
086 y 087 reescritos y sincronizados en todas sus copias; CU-082 pasó a ser el
caso incluido (`«include»`) por los otros cinco, también entre subsistemas;
tabla 7.7 y diagrama de clases de servicios actualizados. Los diagramas pasan
el parser de Mermaid 10.9.1 y el verificador de la cátedra.

---

## Por dónde seguir mañana

1. **Revisar y mergear** `feature/alta-unificada` del panel y de la app. Probar
   el panel con sesión: crear chofer, admin y cliente, y resetear una contraseña.
   (Claude no puede escribir contraseñas en el navegador: el login lo hace nahue.)
2. **Barrido de aislamiento entre distribuidoras** en todos los módulos, con
   dos distribuidoras contra la API (regla de nahue: la empresa A no ve ni
   hace nada sobre la B).
3. **Tanda 3:** `users` y `delivery` (mapper y pruebas), `gascylinder`, y
   `order` al final.
4. **Normalización + soft delete + auditoría** del modelo de datos, con sus
   migraciones y el diagrama de base de datos.
5. Pasada final, Swagger completo, web y publicación.

## Hallazgos abiertos (detalle en `HALLAZGOS.md`)

- **H-74:** borrados físicos y soft delete parcial.
- **H-53:** `/health` da 503 bajo la batería completa (umbral de 300 MB).
- **H-54:** el evento "en camino" se llama distinto en cliente y panel.
- **H-55:** la asignación manual no avisa al chofer por socket.
- **H-57:** la granularidad semanal de los informes se acepta y se ignora.

## Cómo se trabaja un módulo

```bash
bash splg-app-backend/postman/refrescar-ids.sh
python3 splg-app-backend/postman/generar-coleccion.py
splg-app-backend/scripts/alineacion/modulo.sh <etiqueta> src/<modulo>
splg-app-backend/scripts/alineacion/aceptar.sh <etiqueta>   # después del commit
```

- El back de prueba corre en **:3100** (el 3000 es del MCP de Excalidraw).
- Después de regenerar la colección, **no revertir** `SPLG-local.postman_environment.json`
  sin conservar `distribuidoraBaseId`: las altas de choferes la usan.
- `openapi.json` se baja de una instancia en :3101 con `SWAGGER_USER=` y
  `SWAGGER_PASSWORD=` vacías (así no hace falta leer las credenciales).
- Los DSD tienen tres copias (`.mmd`, Doc 3, `Casos-de-Uso.md` §7): `dsd.py`.
  Los DSS, dos (Doc 2 y §6) además del `.mmd`. Los CUE, Doc 1 y §5. Los CUA,
  Doc 0 y §4. Siempre `verificar-conformidad.py` y el validador de Mermaid.

## Reglas acordadas

- A rajatabla lo que pide Nest y TypeScript; seguro por sobre todo.
- No se cambia comportamiento sin decirlo; lo visible que cambie va en el commit.
- Los diagramas se presentan a la cátedra: no se rompen, se actualizan en todas
  sus copias.
- La autorización según quién pide puede quedar en el controlador; las
  invariantes del negocio van al servicio. La regla de quién crea qué usuario
  vive en `autorizarAlta`.
