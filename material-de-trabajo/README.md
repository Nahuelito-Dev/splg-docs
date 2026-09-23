# Material de trabajo

Los documentos que se usan para **construir** el sistema. No son entregables de
la cátedra: los cinco documentos del Proceso Unificado están en la raíz del
repositorio, y el sitio publicado se genera de ahí.

Acá hay ocho, y cada uno responde una pregunta distinta.

| Si querés saber… | Abrí |
|---|---|
| **en qué trabajar ahora** | [ESTADO-Y-PRIORIDADES](ESTADO-Y-PRIORIDADES.md) |
| si un endpoint o un caso de uso puntual anda | [ESTADO-DETALLE](ESTADO-DETALLE.md) |
| qué está mal y falta corregir | [HALLAZGOS](HALLAZGOS.md) |
| cómo está armado el backend y qué refactorizar | [ARQUITECTURA](ARQUITECTURA.md) |
| cómo están el panel y las dos apps por dentro | [CLIENTES](CLIENTES.md) |
| qué cumple el esquema y cómo se lo modifica | [BASE-DE-DATOS](BASE-DE-DATOS.md) |
| qué son los procesos automáticos de la tesis | [MODULOS-INTELIGENTES](MODULOS-INTELIGENTES.md) |
| qué hay alrededor: mercado y otros sistemas propios | [REFERENCIAS](REFERENCIAS.md) |

**Empezá por `ESTADO-Y-PRIORIDADES`.** Los demás son el detalle que respalda lo
que ese documento afirma.

## historico/

Trabajo que ya cumplió su propósito y se guarda por si hay que remitirse a él:
las auditorías de fidelidad entre los casos de uso y el código, la trazabilidad,
la cobertura, las revisiones de notación UML y mermaid, las guías de diagramas y
la revisión de arquitectura de julio, que se resolvió entera.

No se borró nada: en una tesis el rastro de cómo se verificó algo a veces se
pide, y son varios miles de líneas que no se recuperan.

## Una nota sobre las fechas

Todo lo que dice "verificado" está verificado **contra el sistema corriendo**, no
deducido del código. Cuando un documento afirma que algo anda, hubo una petición
real que respondió. Si se cambia el código, la afirmación caduca: se vuelve a
correr la batería y se actualiza.
