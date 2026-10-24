# Barrido de aislamiento entre distribuidoras

Regla (CONVENCIONES §4): con una distribuidora en contexto, lo de otra no existe
(404). Esta batería la prueba endpoint por endpoint contra la API corriendo.

- `fixture-b.sql` siembra en la distribuidora B (`prueba-169888`) una franja,
  una zona, un producto, un vehículo, dos pedidos (uno entregado, otro
  pendiente), un envase, un reclamo, una incidencia, una calificación, un pago y
  una dirección. Ids fijos `bbbb0000-…`.
- `reset-b.sql` los borra y restaura lo que las escrituras pudieran haber
  cambiado. `run.sh` lo corre antes de cada actor, porque si el aislamiento
  falla una escritura de A modifica de verdad los datos de B.
- Actores: admin, chofer y cliente de A, y el super admin con `X-Distributor`
  de A. Los usuarios tienen que existir en Firebase (ver `CUENTAS`).

```bash
SPLG_CLAVE=... scripts/alineacion/aislamiento/run.sh aislamiento.txt
```

Resultado del 25/09: 205 casos, 0 fallas (antes de los arreglos: 66).

Resultado del 26/09, con los casos de flota (`fleet/plans`, `fleet/tasks`,
`fleet/expirations`, `cars/{id}/documents`, `delivery/{id}/documents`)
agregados: 231 casos, 0 fallas. Corrido contra la instancia de flota (:3400):
usa dos planes base fijos de B (`planVtv`, `planLicencia`, sembrados por la
migración `SembrarPlanesBaseDeFlota`, con UUID aleatorio anotado a mano) y el
plan VTV de A (Distribuidora Demo) como contraparte.
