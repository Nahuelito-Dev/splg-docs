"""Tablas planificadas del módulo de flota ampliada (iteración I-12).

Las lee `generar-modelo-datos.py` y se suman a la constante PROPUESTO: se dibujan aparte, con el
estereotipo <<propuesto>>, hasta que la migración las cree. Cada agregado dice a qué casos de uso
responde, qué columnas nuevas lleva una tabla existente y qué tablas nuevas aparecen.

Las referencias al empleado (`employee_id`) apuntan a la tabla `employee` del módulo de personal
(iteración I-11), que describe `propuesto_personal.py`; la vigencia y el detalle de las tareas de
mantenimiento (`valid_from`, `details`) también los define ese módulo.
"""


def _id(nombre):
    return {"nombre": nombre, "tipo": "uuid", "nulo": False,
            "default": "uuid_generate_v4()", "desc": "Identificador."}


def _ref(nombre, destino, destcol, borrado, desc, nulo=False):
    return {"nombre": nombre, "tipo": "uuid", "nulo": nulo, "desc": desc,
            "ref": (destino, destcol, borrado)}


def _dist():
    return _ref("distributor_id", "distributor", "distributor_id", "CASCADE", "Distribuidora dueña.")


def _creada(updated=True):
    cols = [{"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()",
             "desc": "Cuándo se registró."}]
    if updated:
        cols.append({"nombre": "updatedAt", "tipo": "timestamptz", "nulo": False, "default": "now()",
                     "desc": "Última modificación."})
    return cols


AGREGADOS = [
  {
    "clave": "flota-gastos",
    "casos": "CU-195 a CU-202 (I-12)",
    "nota": "La carga de combustible, la multa y el siniestro son registros propios del vehículo y no columnas de `car`: cada uno tiene fecha, importe y ciclo de vida, y alimentan el costo por vehículo. El siniestro no se mezcla con `incident`, que es el contratiempo de calidad de un pedido. El empleado se referencia por `employee_id` y no por `delivery`, porque el responsable de una multa o el que carga combustible puede ser un empleado sin cuenta de acceso. `cash_movement_id` queda sin clave foránea hasta que exista el módulo de caja (I-14).",
    "titulo": "Flota ampliada: combustible, multas y siniestros",
    "pedido": "Llevar las cargas de combustible, las multas de tránsito y los siniestros de cada vehículo, para conocer su consumo y su costo.",
    "enums": {
      "fuel_type_enum": ["diesel", "gasoline", "cng", "lpg"],
      "fuel_payment_method_enum": ["cash_box", "driver_cash", "card", "fuel_account"],
      "traffic_fine_status_enum": ["pending", "appealed", "paid", "voided"],
      "vehicle_accident_status_enum": ["reported", "under_review", "repairing", "closed"],
    },
    "columnas": {
      "car": [
        {"nombre": "fuel_type", "tipo": "fuel_type_enum", "nulo": True,
         "concepto": "tipo de combustible", "desc": "Combustible que usa el vehículo; es el que se propone en cada carga."},
        {"nombre": "tank_capacity_liters", "tipo": "numeric(6,2)", "nulo": True,
         "concepto": "capacidad del tanque", "desc": "Litros que entran en el tanque; una carga no puede superarlos en más de un 5 %."},
      ],
    },
    "tablas": [
      {"nombre": "fuel_load", "concepto": "Carga de combustible",
       "desc": "Una carga de combustible de un vehículo, con su kilometraje y su importe.",
       "columnas": [
         _id("fuel_load_id"), _dist(),
         _ref("car_id", "car", "car_id", "CASCADE", "Vehículo que cargó."),
         _ref("employee_id", "employee", "employee_id", "SET NULL", "Empleado que hizo la carga.", nulo=True),
         {"nombre": "loaded_at", "tipo": "timestamptz", "nulo": False,
          "concepto": "fecha y hora", "desc": "Cuándo se hizo la carga."},
         {"nombre": "fuel_type", "tipo": "fuel_type_enum", "nulo": False,
          "concepto": "tipo de combustible", "desc": "Combustible cargado; por omisión el del vehículo."},
         {"nombre": "liters", "tipo": "numeric(10,2)", "nulo": False,
          "concepto": "litros", "desc": "Litros cargados; mayores que cero."},
         {"nombre": "unit_price", "tipo": "numeric(12,3)", "nulo": False,
          "concepto": "precio por litro", "desc": "Precio de cada litro."},
         {"nombre": "total_amount", "tipo": "numeric(12,2)", "nulo": False,
          "concepto": "importe", "desc": "Importe total; coincide con litros por precio, con un 1 % de tolerancia."},
         {"nombre": "odometer_km", "tipo": "integer", "nulo": False,
          "concepto": "kilometraje", "desc": "Kilometraje del tablero; no puede ser menor que el de la carga anterior."},
         {"nombre": "is_full_tank", "tipo": "boolean", "nulo": False, "default": "true",
          "concepto": "tanque lleno", "desc": "Si se llenó el tanque: base del cálculo de consumo."},
         {"nombre": "station", "tipo": "varchar(120)", "nulo": True,
          "concepto": "estación", "desc": "Estación de servicio."},
         {"nombre": "payment_method", "tipo": "fuel_payment_method_enum", "nulo": False,
          "concepto": "medio de pago", "desc": "Caja, efectivo del chofer, tarjeta o cuenta corriente de combustible."},
         {"nombre": "receipt_number", "tipo": "varchar(40)", "nulo": True,
          "concepto": "comprobante", "desc": "Número del comprobante."},
         {"nombre": "cash_movement_id", "tipo": "uuid", "nulo": True,
          "desc": "Movimiento de caja que originó el pago; lo completa el módulo de caja."},
         {"nombre": "anomaly", "tipo": "boolean", "nulo": False, "default": "false",
          "concepto": "anómala", "desc": "El consumo del tramo se aparta más de un 25 % del promedio."},
         {"nombre": "notes", "tipo": "text", "nulo": True,
          "concepto": "observación", "desc": "Observaciones de quien cargó."},
         _ref("created_by_user_id", "user", "user_id", "SET NULL", "Quién la registró.", nulo=True),
       ] + _creada() + [
         {"nombre": "deletedAt", "tipo": "timestamptz", "nulo": True,
          "concepto": "anulada el", "desc": "Cuándo se anuló; una carga anulada no cuenta en los cálculos."},
       ],
       "pk": ["fuel_load_id"], "unicos": []},
      {"nombre": "traffic_fine", "concepto": "Multa de tránsito",
       "desc": "Una multa de tránsito de un vehículo, con su ciclo de pendiente a pagada o anulada.",
       "columnas": [
         _id("fine_id"), _dist(),
         _ref("car_id", "car", "car_id", "CASCADE", "Vehículo multado."),
         _ref("employee_id", "employee", "employee_id", "SET NULL",
              "Empleado responsable; se deduce de la asignación de vehículo abierta al momento de la infracción.", nulo=True),
         {"nombre": "occurred_at", "tipo": "timestamptz", "nulo": False,
          "concepto": "fecha de la infracción", "desc": "Cuándo ocurrió la infracción."},
         {"nombre": "jurisdiction", "tipo": "varchar(80)", "nulo": False,
          "concepto": "jurisdicción", "desc": "Jurisdicción que labró el acta."},
         {"nombre": "act_number", "tipo": "varchar(40)", "nulo": False,
          "concepto": "número de acta", "desc": "Número del acta; único por distribuidora y jurisdicción."},
         {"nombre": "infraction", "tipo": "text", "nulo": False,
          "concepto": "infracción", "desc": "Descripción de la infracción."},
         {"nombre": "amount", "tipo": "numeric(12,2)", "nulo": False,
          "concepto": "importe", "desc": "Importe de la multa."},
         {"nombre": "voluntary_payment_amount", "tipo": "numeric(12,2)", "nulo": True,
          "concepto": "importe con pago voluntario", "desc": "Importe con el descuento por pagar antes."},
         {"nombre": "due_date", "tipo": "date", "nulo": True,
          "concepto": "vencimiento", "desc": "Fecha de vencimiento del pago."},
         {"nombre": "status", "tipo": "traffic_fine_status_enum", "nulo": False, "default": "'pending'",
          "concepto": "estado", "desc": "Pendiente, apelada, pagada o anulada."},
         {"nombre": "paid_at", "tipo": "timestamptz", "nulo": True,
          "concepto": "pagada el", "desc": "Cuándo se pagó."},
         {"nombre": "paid_amount", "tipo": "numeric(12,2)", "nulo": True,
          "concepto": "importe pagado", "desc": "Importe efectivamente pagado."},
         {"nombre": "charged_to_employee", "tipo": "boolean", "nulo": False, "default": "false",
          "concepto": "imputada al chofer", "desc": "Si la asume el empleado: se descuenta en su liquidación."},
         {"nombre": "cash_movement_id", "tipo": "uuid", "nulo": True,
          "desc": "Movimiento de caja del pago; lo completa el módulo de caja."},
         {"nombre": "void_reason", "tipo": "text", "nulo": True,
          "concepto": "motivo de anulación", "desc": "Motivo con el que se anuló; obligatorio al anular."},
         {"nombre": "alerted_at", "tipo": "timestamptz", "nulo": True,
          "concepto": "avisada el", "desc": "Cuándo se avisó del vencimiento, para no repetir el aviso."},
       ] + _creada(),
       "pk": ["fine_id"], "unicos": [["distributor_id", "jurisdiction", "act_number"]]},
      {"nombre": "vehicle_accident", "concepto": "Siniestro",
       "desc": "Un siniestro de un vehículo, de denunciado a cerrado, con sus costos.",
       "columnas": [
         _id("accident_id"), _dist(),
         _ref("car_id", "car", "car_id", "CASCADE", "Vehículo siniestrado."),
         _ref("employee_id", "employee", "employee_id", "SET NULL", "Empleado que conducía.", nulo=True),
         {"nombre": "occurred_at", "tipo": "timestamptz", "nulo": False,
          "concepto": "fecha", "desc": "Cuándo ocurrió."},
         {"nombre": "location", "tipo": "geometry(Point,4326)", "nulo": True,
          "concepto": "ubicación", "desc": "Punto donde ocurrió."},
         {"nombre": "address", "tipo": "text", "nulo": True,
          "concepto": "domicilio", "desc": "Domicilio aproximado."},
         {"nombre": "description", "tipo": "text", "nulo": False,
          "concepto": "descripción", "desc": "Qué pasó."},
         {"nombre": "injuries", "tipo": "boolean", "nulo": False, "default": "false",
          "concepto": "hubo heridos", "desc": "Si hubo personas heridas."},
         {"nombre": "third_parties_involved", "tipo": "boolean", "nulo": False, "default": "false",
          "concepto": "hubo terceros", "desc": "Si hubo terceros involucrados."},
         {"nombre": "hazmat_release", "tipo": "boolean", "nulo": False, "default": "false",
          "concepto": "derrame de GLP", "desc": "Si hubo fuga o derrame de gas: obliga a avisar a los administradores."},
         {"nombre": "police_report_number", "tipo": "varchar(40)", "nulo": True,
          "concepto": "denuncia policial", "desc": "Número de la denuncia policial."},
         {"nombre": "insurer_claim_number", "tipo": "varchar(40)", "nulo": True,
          "concepto": "reclamo al seguro", "desc": "Número del reclamo a la aseguradora."},
         {"nombre": "status", "tipo": "vehicle_accident_status_enum", "nulo": False, "default": "'reported'",
          "concepto": "estado", "desc": "Denunciado, en revisión, en reparación o cerrado."},
         {"nombre": "vehicle_unusable", "tipo": "boolean", "nulo": False, "default": "false",
          "concepto": "vehículo inutilizable", "desc": "Si el vehículo no puede circular: pasa a fuera de servicio."},
         {"nombre": "repair_cost", "tipo": "numeric(12,2)", "nulo": True,
          "concepto": "costo de reparación", "desc": "Costo de la reparación."},
         {"nombre": "insurer_reimbursement", "tipo": "numeric(12,2)", "nulo": True,
          "concepto": "reintegro del seguro", "desc": "Lo que reintegró la aseguradora."},
         {"nombre": "deductible_amount", "tipo": "numeric(12,2)", "nulo": True,
          "concepto": "franquicia", "desc": "Franquicia a cargo de la distribuidora."},
         {"nombre": "closed_at", "tipo": "timestamptz", "nulo": True,
          "concepto": "cerrado el", "desc": "Cuándo se cerró."},
       ] + _creada(),
       "pk": ["accident_id"], "unicos": []},
    ],
  },
  {
    "clave": "flota-neumaticos",
    "casos": "CU-205 y CU-206 (I-12, opcional)",
    "nota": "Funcionalidad opcional del módulo, que se puede construir aparte. Los movimientos del neumático son un libro que no se modifica: el estado y la posición actuales del neumático se guardan en `tire` para no recorrer el historial en cada consulta.",
    "titulo": "Flota ampliada: neumáticos",
    "pedido": "Llevar cada neumático y sus movimientos —montaje, desmontaje, rotación, recapado y baja— para saber cuántos kilómetros recorrió.",
    "enums": {
      "tire_status_enum": ["in_stock", "mounted", "retired"],
      "tire_event_type_enum": ["mount", "unmount", "rotate", "retread", "retire"],
    },
    "columnas": {},
    "tablas": [
      {"nombre": "tire", "concepto": "Neumático",
       "desc": "Un neumático de la distribuidora, en depósito, montado en un vehículo o dado de baja.",
       "columnas": [
         _id("tire_id"), _dist(),
         _ref("car_id", "car", "car_id", "SET NULL", "Vehículo en el que está montado, si lo está.", nulo=True),
         {"nombre": "serial", "tipo": "varchar(40)", "nulo": False,
          "concepto": "número de serie", "desc": "Número de serie del neumático; único por distribuidora."},
         {"nombre": "brand", "tipo": "varchar(60)", "nulo": False,
          "concepto": "marca", "desc": "Marca."},
         {"nombre": "size", "tipo": "varchar(30)", "nulo": False,
          "concepto": "medida", "desc": "Medida del neumático."},
         {"nombre": "cost", "tipo": "numeric(12,2)", "nulo": False,
          "concepto": "costo", "desc": "Costo de compra."},
         {"nombre": "status", "tipo": "tire_status_enum", "nulo": False, "default": "'in_stock'",
          "concepto": "estado", "desc": "En depósito, montado o dado de baja."},
         {"nombre": "position", "tipo": "varchar(6)", "nulo": True,
          "concepto": "posición", "desc": "Código corto de la posición en el vehículo."},
         {"nombre": "mounted_odometer_km", "tipo": "integer", "nulo": True,
          "concepto": "kilometraje de montaje", "desc": "Kilometraje del vehículo al montarlo."},
       ] + _creada(),
       "pk": ["tire_id"], "unicos": [["distributor_id", "serial"]]},
      {"nombre": "tire_event", "concepto": "Movimiento de neumático",
       "desc": "Un movimiento de un neumático; el libro no se modifica.",
       "columnas": [
         _id("event_id"), _dist(),
         _ref("tire_id", "tire", "tire_id", "CASCADE", "Neumático movido."),
         _ref("car_id", "car", "car_id", "SET NULL", "Vehículo del movimiento, si corresponde.", nulo=True),
         {"nombre": "event_type", "tipo": "tire_event_type_enum", "nulo": False,
          "concepto": "tipo", "desc": "Montaje, desmontaje, rotación, recapado o baja."},
         {"nombre": "odometer_km", "tipo": "integer", "nulo": False,
          "concepto": "kilometraje", "desc": "Kilometraje del vehículo en el movimiento."},
         {"nombre": "position", "tipo": "varchar(6)", "nulo": True,
          "desc": "Posición de destino, en un montaje o una rotación."},
         {"nombre": "occurred_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "concepto": "fecha", "desc": "Cuándo ocurrió."},
         _ref("created_by_user_id", "user", "user_id", "SET NULL", "Quién lo registró.", nulo=True),
       ],
       "pk": ["event_id"], "unicos": []},
    ],
  },
]
