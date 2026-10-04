"""Modelo de datos planificado del módulo Personal (iteración I-11).

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
        "casos": "CU-176 a CU-194 (I-11)",
        "nota": "Todo empleado existe como legajo, tenga o no cuenta de acceso: un chofer es un empleado cuya cuenta tiene el perfil de reparto, y ayudantes, depósito y vendedores son legajos sin cuenta (sin roles nuevos). La documentación con vencimiento del personal —licencia de conducir, curso de mercancías peligrosas, examen psicofísico, alta en la ART— no tiene tabla propia: reutiliza el plan y la tarea de mantenimiento con un dueño empleado, y hereda los adjuntos, la pantalla de vencimientos, el aviso diario y el bloqueo de despacho que ya leen esas tablas; `delivery_id` queda como columna heredada. Los adjuntos del legajo van en una tabla genérica con dueño (`owner_type`, `owner_id`), sin clave foránea a propósito porque el dueño es polimórfico: lo valida un puerto que registra cada módulo. Dos licencias del mismo empleado no pueden superponerse: lo impide una restricción de exclusión de la base (`btree_gist`), no sólo el servicio.",
        "titulo": "Personal y legajos",
        "pedido": "Llevar el legajo de cada persona que trabaja en la distribuidora, su asistencia, sus licencias y la documentación con vencimiento, y que ese control inhabilite para el despacho a quien no esté en regla.",
        "enums": {
            "job_position_category_enum": ["driver", "helper", "warehouse", "administration", "sales", "management", "other"],
            "employee_document_type_enum": ["dni", "passport", "other"],
            "employee_termination_reason_enum": ["resignation", "dismissal", "end_of_contract", "retirement", "other"],
            "employment_type_enum": ["permanent", "fixed_term", "part_time", "contractor"],
            "employee_status_enum": ["active", "terminated"],
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
            {"nombre": "job_position", "concepto": "Puesto de trabajo",
             "desc": "Puesto que ocupa el personal de una distribuidora; su categoría gobierna las reglas.",
             "columnas": [
                 _id("position_id"), _dist(),
                 _c("name", "varchar(80)", False, "Nombre del puesto, único entre los vigentes de la distribuidora sin distinguir mayúsculas."),
                 _c("category", "job_position_category_enum", False, "Categoría que manda las reglas: el nombre es libre."),
                 _c("is_active", "boolean", False, "Si el puesto se ofrece.", "true"),
                 *_marcas(),
                 _c("deletedAt", "timestamptz", True, "Baja lógica."),
             ],
             "pk": ["position_id"], "unicos": []},
            {"nombre": "employee", "concepto": "Empleado",
             "desc": "Legajo de una persona que trabaja en la distribuidora, con o sin cuenta de acceso.",
             "columnas": [
                 _id("employee_id"), _dist(),
                 _ref("user_id", "user", "user_id", "SET NULL",
                      "Cuenta de acceso del empleado, si la tiene; única entre los legajos vigentes.", nulo=True),
                 _ref("position_id", "job_position", "position_id", "RESTRICT", "Puesto que ocupa."),
                 _c("file_number", "varchar(20)", False, "Número de legajo, único por distribuidora."),
                 _c("first_name", "varchar(80)", False, "Nombre."),
                 _c("last_name", "varchar(80)", False, "Apellido."),
                 _c("document_type", "employee_document_type_enum", False, "Tipo de documento."),
                 _c("document_number", "varchar(20)", False, "Número de documento, único por distribuidora."),
                 _c("cuil", "varchar(11)", True, "CUIL de once dígitos, con dígito verificador válido."),
                 _c("birth_date", "date", True, "Fecha de nacimiento."),
                 _c("address_line", "varchar(200)", True, "Domicilio."),
                 _c("city", "varchar(80)", True, "Localidad."),
                 _c("province", "varchar(80)", True, "Provincia."),
                 _c("postal_code", "varchar(10)", True, "Código postal."),
                 _c("phone", "varchar(30)", True, "Teléfono."),
                 _c("personal_email", "varchar(120)", True, "Correo personal."),
                 _c("emergency_contact_name", "varchar(120)", True, "Contacto de emergencia."),
                 _c("emergency_contact_phone", "varchar(30)", True, "Teléfono del contacto de emergencia."),
                 _c("emergency_contact_relationship", "varchar(40)", True, "Vínculo con el contacto de emergencia."),
                 _c("hire_date", "date", False, "Fecha de ingreso."),
                 _c("termination_date", "date", True, "Fecha de egreso; vacía mientras está activo."),
                 _c("termination_reason", "employee_termination_reason_enum", True, "Motivo del egreso."),
                 _c("employment_type", "employment_type_enum", False, "Modalidad de contratación."),
                 _c("status", "employee_status_enum", False, "Activo o egresado; está egresado si y sólo si tiene fecha de egreso.", "'active'"),
                 _c("bank_cbu", "varchar(22)", True, "CBU, para pagar liquidaciones."),
                 _c("notes", "text", True, "Observaciones."),
                 *_marcas(),
                 _c("deletedAt", "timestamptz", True, "Baja lógica, sólo para altas erróneas."),
             ],
             "pk": ["employee_id"],
             "unicos": [["user_id"], ["distributor_id", "file_number"], ["distributor_id", "document_number"]]},
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
