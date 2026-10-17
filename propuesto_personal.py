"""Modelo de datos planificado del módulo Personal (iteración C-08): lo que todavía no está construido.

Las tablas `job_position` y `employee` y sus enumerados ya están en la base (puestos y legajos, CU-176 a CU-182 y
CU-255 a CU-257) y salen de ella; acá quedan las jornadas, las licencias y las columnas de la documentación del personal.

Lo lee generar-modelo-datos.py, que lo suma a la constante PROPUESTO y lo dibuja con el
estereotipo <<propuesto>>, y material-de-trabajo/verificar-mc-der.py, que contrasta el modelo
conceptual con estas tablas en lugar de con la base, que todavía no las tiene.

Es el diseño del Documento 3: tablas y columnas en snake_case, fechas en timestamptz salvo las
de calendario (date), y toda referencia a otra tabla con su clave foránea declarada.
"""


def _id(nombre):
    return {"nombre": nombre, "tipo": "uuid", "nulo": False,
            "default": "uuid_generate_v4()", "desc": "Identificador."}


def _ref(nombre, destino, destcol, borrado, desc, nulo=False):
    return {"nombre": nombre, "tipo": "uuid", "nulo": nulo, "desc": desc,
            "ref": (destino, destcol, borrado)}


def _dist():
    return _ref("distributor_id", "distributor", "distributor_id", "CASCADE", "Distribuidora dueña.")


def _c(nombre, tipo, nulo, desc, default=None):
    d = {"nombre": nombre, "tipo": tipo, "nulo": nulo, "desc": desc}
    if default:
        d["default"] = default
    return d


def _marcas():
    return [_c("createdAt", "timestamptz", False, "Cuándo se creó.", "now()"),
            _c("updatedAt", "timestamptz", False, "Cuándo se modificó por última vez.", "now()")]


AGREGADOS = [
    {
        "clave": "personal-y-legajos",
        "casos": "CU-183 a CU-194 y CU-246 (C-08)",
        "nota": "Los puestos (`job_position`) y los legajos (`employee`) ya están construidos y salen de la base: todo empleado existe como legajo, tenga o no cuenta de acceso, un chofer es un empleado cuya cuenta tiene el perfil de reparto, y ayudantes, depósito y vendedores son legajos sin cuenta (sin roles nuevos). Falta construir lo que cuelga del legajo. La documentación con vencimiento del personal —licencia de conducir, curso de mercancías peligrosas, examen psicofísico, alta en la ART— no tiene tabla propia: reutiliza el plan y la tarea de mantenimiento con un dueño empleado, y hereda los adjuntos, la pantalla de vencimientos, el aviso diario y el bloqueo de despacho que ya leen esas tablas; `delivery_id` queda como columna heredada. Los adjuntos del legajo van en una tabla genérica con dueño (`owner_type`, `owner_id`), sin clave foránea a propósito porque el dueño es polimórfico: lo valida un puerto que registra cada módulo. Dos licencias del mismo empleado no pueden superponerse: lo impide una restricción de exclusión de la base (`btree_gist`), no solo el servicio.",
        "titulo": "Personal y legajos",
        "pedido": "Llevar la asistencia, las licencias y la documentación con vencimiento de cada persona que trabaja en la distribuidora, y que ese control inhabilite para el despacho a quien no esté en regla.",
        "enums": {
            "attendance_source_enum": ["panel", "driver_app"],
            "employee_leave_type_enum": ["vacation", "sick", "work_accident", "study", "marriage", "birth",
                                         "bereavement", "unpaid", "suspension", "unjustified_absence", "other"],
            "employee_leave_status_enum": ["requested", "approved", "rejected", "cancelled"],
            "maintenance_document_kind_enum": ["insurance", "vtv", "hazmat_vehicle_permit", "driver_license",
                                               "hazmat_driver_course", "psychophysical", "art_coverage",
                                               "service", "generic"],
        },
        "enum_valores": {"maintenance_subject_enum": ["employee"]},
        "columnas": {
            "maintenance_plan": [
                {"nombre": "document_kind", "tipo": "maintenance_document_kind_enum", "nulo": True,
                 "concepto": "documento que controla",
                 "desc": "Qué documento controla el plan: le dice al panel qué formulario mostrar y al sistema qué forma de detalle validar."},
                {"nombre": "applies_to_categories", "tipo": "job_position_category_enum[]", "nulo": True,
                 "concepto": "aplica a",
                 "desc": "Categorías de puesto a las que aplica el plan; vacío significa todas."},
            ],
            "maintenance_task": [
                _ref("employee_id", "employee", "employee_id", "CASCADE",
                     "Empleado dueño de la tarea; obligatorio si el plan es de sujeto empleado.", nulo=True),
                {"nombre": "valid_from", "tipo": "timestamptz", "nulo": True,
                 "concepto": "vigente desde",
                 "desc": "Inicio de la vigencia del documento (póliza, habilitación o documentación del personal); lo usa el prorrateo de la prima."},
                {"nombre": "details", "tipo": "jsonb", "nulo": True, "concepto": "detalle",
                 "desc": "Datos propios del tipo de documento (número de certificado, aseguradora, póliza, cobertura, franquicia, cuotas), con la forma que fija cada plan."},
            ],
        },
        "tablas": [
            {"nombre": "employee_attendance", "concepto": "Jornada de trabajo",
             "desc": "Una jornada de un empleado: su ingreso y su egreso.",
             "columnas": [
                 _id("attendance_id"), _dist(),
                 _ref("employee_id", "employee", "employee_id", "CASCADE", "Empleado de la jornada."),
                 _c("work_date", "date", False, "Día argentino del ingreso."),
                 _c("check_in_at", "timestamptz", False, "Ingreso."),
                 _c("check_out_at", "timestamptz", True, "Egreso; vacío mientras la jornada está abierta."),
                 _c("source", "attendance_source_enum", False, "Panel o aplicación del chofer."),
                 _ref("recorded_by_user_id", "user", "user_id", "SET NULL", "Usuario que la cargó.", nulo=True),
                 _c("notes", "text", True, "Observación; obligatoria al corregir."),
                 *_marcas(),
             ],
             "pk": ["attendance_id"], "unicos": []},
            {"nombre": "employee_leave", "concepto": "Licencia laboral",
             "desc": "Licencia o ausencia de un empleado, con su período y su estado.",
             "columnas": [
                 _id("leave_id"), _dist(),
                 _ref("employee_id", "employee", "employee_id", "CASCADE", "Empleado de la licencia."),
                 _c("type", "employee_leave_type_enum", False, "Tipo de licencia o ausencia."),
                 _c("start_date", "date", False, "Primer día."),
                 _c("end_date", "date", False, "Último día, inclusive."),
                 _c("days", "integer", False, "Días corridos del período."),
                 _c("status", "employee_leave_status_enum", False, "Solicitada, aprobada, rechazada o cancelada.", "'requested'"),
                 _c("reason", "text", True, "Motivo de la solicitud."),
                 _c("rejection_reason", "text", True, "Motivo del rechazo; obligatorio al rechazar."),
                 _ref("requested_by_user_id", "user", "user_id", "SET NULL", "Usuario que la cargó.", nulo=True),
                 _ref("decided_by_user_id", "user", "user_id", "SET NULL", "Administrador que la resolvió.", nulo=True),
                 _c("decided_at", "timestamptz", True, "Cuándo se resolvió."),
                 *_marcas(),
             ],
             "pk": ["leave_id"], "unicos": []},
        ],
    },
]

# contexto del modelo físico
CONTEXTO = ("Personal", ["job_position", "employee", "employee_attendance", "employee_leave"])
