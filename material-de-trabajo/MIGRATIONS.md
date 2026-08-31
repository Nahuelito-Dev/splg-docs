# Migraciones (TypeORM)

El esquema se gestiona con **migraciones** — son la fuente de verdad, en todos
los ambientes. `synchronize` está en **false** por defecto (en dev se puede
optar por `DB_SYNC=true` para iterar rápido, nunca en prod).

## Comandos

```bash
# Generar una migración con el diff entre las entidades y la DB actual
npm run migration:generate -- src/migrations/NombreDescriptivo

# Aplicar las migraciones pendientes
npm run migration:run

# Revertir la última
npm run migration:revert

# Ver estado
npm run migration:show
```

La config del CLI vive en `src/data-source.ts` (lee el `.env`). En runtime la app
usa la config de `app.module.ts`.

## Flujo de trabajo

1. Cambiás una entidad (columna, índice, relación).
2. `npm run migration:generate -- src/migrations/LoQueHiciste`.
3. **Revisás** el archivo generado (que no tenga DROPs inesperados por drift).
4. `npm run migration:run` para aplicarla.
5. Commiteás la migración junto con el cambio de entidad.

## ⚠️ Baseline para una DB NUEVA (primer deploy a prod)

La primera migración del repo (`AddHotIndexes`) **solo agrega índices**: asume que
el esquema (tablas) ya existe (se creó por `synchronize` en dev). Una base de datos
**vacía** de prod NO tiene las tablas, así que hay que crearlas primero. Dos opciones:

- **Opción A (recomendada):** generar una migración baseline del esquema completo
  contra una DB vacía, y commitearla ANTES de `AddHotIndexes`:
  ```bash
  # apuntar DB_NAME a una base vacía y:
  npm run migration:generate -- src/migrations/000_InitialSchema
  ```
- **Opción B:** en el primer arranque de prod, correr `synchronize` UNA vez para
  crear el esquema y después dejarlo en false + `migration:run` para el resto.

Definir esto antes del primer deploy productivo.
