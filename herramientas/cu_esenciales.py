"""Los casos de uso esenciales: los únicos que llevan su caso de uso expandido en el Documento 1.

Decisión de nahue (31/10/2026): la cátedra no pide los artefactos de todos los casos; quedan los 21 del
circuito del pedido, los cinco módulos inteligentes y la auditoría. Los demás casos siguen en la lista
con su importancia (Documento 1 §4) y en el diagrama de su subsistema.
"""

ESENCIALES = (
    "CU-001", "CU-002", "CU-005", "CU-008", "CU-022", "CU-013", "CU-014", "CU-015", "CU-017",
    "CU-078", "CU-079", "CU-292", "CU-301", "CU-048", "CU-023", "CU-025",
    "CU-105", "CU-106", "CU-107", "CU-108", "CU-152",
)

# Retirados del alcance (el chofer cobra un sueldo mensual, sin comisiones por entrega): siguen en el catálogo
# de Casos-de-Uso.md y en el Documento 0, pero el Documento 1 los lista como retirados y no los cuenta en los
# IRQ ni en la matriz. Las ganancias del chofer y las comisiones con su liquidación (decisión de nahue, 31/10/2026).
RETIRADOS_ALCANCE = ("CU-049", "CU-240", "CU-241", "CU-242", "CU-243", "CU-244",
                     "CU-333", "CU-334", "CU-335", "CU-347")
