-- Modelo propuesto — SPLG
-- Los cambios de modelo de los casos de uso planificados, sobre el esquema que hoy está en la base.
-- PostgreSQL. Se ejecuta en este orden: tipos, columnas nuevas, tablas nuevas,
-- claves foráneas. Generado por generar-modelo-datos.py.

-- ---------- tipos enumerados nuevos ----------

-- ---------- valores nuevos de tipos enumerados existentes ----------

-- ---------- Baja del envase y oferta de retiro ----------
ALTER TABLE "cylinder" ADD COLUMN IF NOT EXISTS "decommissioned_at" timestamptz;
ALTER TABLE "cylinder_recovery_notice" ADD COLUMN IF NOT EXISTS "order_id" uuid;

-- ---------- claves foráneas de lo propuesto ----------
ALTER TABLE "cylinder_recovery_notice" ADD CONSTRAINT "FK_cylinder_recovery_notice_order_id" FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE SET NULL;

-- ---------- relaciones que hoy existen sin clave foránea ----------
-- Las filas huérfanas harían fallar el ALTER: se limpian antes, en la misma migración.
