#!/usr/bin/env python3
"""Genera el modelo de datos de SPLG leyendo la base que corre en Docker.

    python3 generar-modelo-datos.py

Sale, en diagramas/base-de-datos/:

  SPLG-base-de-datos.sql                  el esquema tal cual lo devuelve pg_dump
  SPLG-base-de-datos-lucidchart.sql       el esquema actual en SQL portable
  SPLG-base-de-datos-propuesta.sql        solo los agregados pedidos por la catedra
  SPLG-base-de-datos-completa-lucidchart.sql  actual + propuesta, portable, para importar
  SPLG-modelo-fisico.puml/.png/.svg       entidad-relacion con tablas y columnas
  SPLG-modelo-conceptual.puml/...         entidades del negocio y cardinalidades
  SPLG-modelo-de-datos.md                 el diccionario de datos en texto
  LEEME.md                                como usar cada archivo

Se lee de la base y no de las entidades de TypeORM porque la base es la que manda:
incluye lo que agregaron las migraciones y los indices que no estan en el codigo.

Lo implementado sale de la base. Lo que la catedra pidio agregar vive en la
constante PROPUESTO y se dibuja aparte, con estereotipo <<propuesto>>, para que
en la defensa se distinga de un vistazo lo que ya corre de lo que falta.
"""
import subprocess, os, re, sys, collections

D = os.path.dirname(os.path.abspath(__file__)) + "/"
SAL = D + "diagramas/base-de-datos/"
os.makedirs(SAL, exist_ok=True)

BACK = os.path.abspath(D + "../splg-app-backend") + "/"
CONTENEDOR = "splg-bd"
env = {}
for l in open(BACK + ".env", encoding="utf-8"):
    m = re.match(r'\s*([A-Z_]+)\s*=\s*(.*)', l)
    if m: env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
USR, BD = env.get("DB_USERNAME", "postgres"), env.get("DB_NAME", "postgres")

def psql(sql):
    r = subprocess.run(["docker", "exec", CONTENEDOR, "psql", "-U", USR, "-d", BD,
                        "-At", "-F", "\x1f", "-c", sql], capture_output=True, text=True)
    if r.returncode:
        sys.exit("psql: " + r.stderr.strip())
    # strip() a secas se come el separador: para Python \x1f es un espacio en
    # blanco y las filas que terminan en campos vacios perdian columnas.
    return [l.split("\x1f") for l in r.stdout.strip("\n").split("\n") if l]

SALTAR = "('migrations','spatial_ref_sys','geography_columns','geometry_columns')"

# ---------------------------------------------------------------- lo implementado

tablas = [t[0] for t in psql(f"""
  select table_name from information_schema.tables
  where table_schema='public' and table_type='BASE TABLE' and table_name not in {SALTAR}
  order by table_name;""")]

columnas = collections.defaultdict(list)
for t, c, tipo, nul, dflt, largo, num, esc in psql(f"""
  select table_name, column_name, udt_name, is_nullable,
         replace(replace(coalesce(column_default,''), chr(10), ' '), chr(13), ' '),
         coalesce(character_maximum_length::text,''), coalesce(numeric_precision::text,''),
         coalesce(numeric_scale::text,'')
  from information_schema.columns
  where table_schema='public' and table_name not in {SALTAR}
  order by table_name, ordinal_position;"""):
    columnas[t].append({"nombre": c, "udt": tipo, "nulo": nul == "YES", "default": dflt,
                        "largo": largo, "prec": num, "esc": esc})

pk = collections.defaultdict(list)
for t, c in psql(f"""
  select tc.table_name, kcu.column_name
  from information_schema.table_constraints tc
  join information_schema.key_column_usage kcu
    on kcu.constraint_name=tc.constraint_name and kcu.constraint_schema=tc.constraint_schema
  where tc.constraint_type='PRIMARY KEY' and tc.table_schema='public'
    and tc.table_name not in {SALTAR}
  order by tc.table_name, kcu.ordinal_position;"""):
    pk[t].append(c)

# Los unicos se agrupan POR RESTRICCION: cylinder tiene UNIQUE(distributor_id,
# serial) y rating UNIQUE(order_id, from_role). Si se aplanan las columnas, esas
# claves compuestas se leen como si cada columna fuera unica por si sola y las
# relaciones salen dibujadas uno a uno cuando en realidad son uno a muchos.
_uq = collections.defaultdict(lambda: collections.defaultdict(list))
for t, cons, c in psql(f"""
  select tc.table_name, tc.constraint_name, kcu.column_name
  from information_schema.table_constraints tc
  join information_schema.key_column_usage kcu
    on kcu.constraint_name=tc.constraint_name and kcu.constraint_schema=tc.constraint_schema
  where tc.constraint_type='UNIQUE' and tc.table_schema='public'
    and tc.table_name not in {SALTAR}
  order by tc.table_name, tc.constraint_name, kcu.ordinal_position;"""):
    _uq[t][cons].append(c)
unicos = {t: list(v.values()) for t, v in _uq.items()}          # [[col, col], [col]]
unicos_simples = {t: {g[0] for g in v if len(g) == 1} for t, v in unicos.items()}

fks = []
for t, c, dt, dc, borrado in psql(f"""
  select tc.table_name, kcu.column_name, ccu.table_name, ccu.column_name, rc.delete_rule
  from information_schema.table_constraints tc
  join information_schema.key_column_usage kcu on kcu.constraint_name=tc.constraint_name
  join information_schema.constraint_column_usage ccu on ccu.constraint_name=tc.constraint_name
  join information_schema.referential_constraints rc on rc.constraint_name=tc.constraint_name
  where tc.constraint_type='FOREIGN KEY' and tc.table_schema='public'
  order by 1,2;"""):
    fks.append({"tabla": t, "col": c, "destino": dt, "destcol": dc, "borrado": borrado})

enums = {n: v.split(",") for n, v in psql("""
  select t.typname, string_agg(e.enumlabel, ',' order by e.enumsortorder)
  from pg_type t join pg_enum e on e.enumtypid=t.oid
  join pg_namespace n on n.oid=t.typnamespace and n.nspname='public'
  group by t.typname;""")}

# ------------------------------------------------- relaciones que existen sin FK
# Columnas que apuntan a otra tabla y se usan como referencia en el codigo, pero
# que nunca se declararon como FOREIGN KEY: la base no las valida ni las
# propaga al borrar. El destino de cada una se leyo de la entidad de TypeORM
# correspondiente (los comentarios del backend dicen a que apunta cada columna).
SIN_FK = [
  # Un pago o un movimiento de envase son registro contable y de trazabilidad:
  # no se pierden porque se borre lo que referencian. RESTRICT, no CASCADE.
  {"tabla": "payment", "col": "order_id", "destino": "order", "destcol": "order_id",
   "borrado": "RESTRICT"},
  {"tabla": "payment", "col": "distributor_id", "destino": "distributor",
   "destcol": "distributor_id", "borrado": "CASCADE"},
  {"tabla": "cylinder_movement", "col": "cylinder_id", "destino": "cylinder",
   "destcol": "cylinder_id", "borrado": "RESTRICT"},
  {"tabla": "cylinder_movement", "col": "distributor_id", "destino": "distributor",
   "destcol": "distributor_id", "borrado": "CASCADE"},
  {"tabla": "cylinder_movement", "col": "order_id", "destino": "order",
   "destcol": "order_id", "borrado": "SET NULL"},
  {"tabla": "cylinder_movement", "col": "actor_user_id", "destino": "user",
   "destcol": "user_id", "borrado": "SET NULL"},
  {"tabla": "cylinder", "col": "gas_cylinder_id", "destino": "gas_cylinder",
   "destcol": "gas_cylinder_id", "borrado": "SET NULL"},
  {"tabla": "cylinder", "col": "current_customer_id", "destino": "user",
   "destcol": "user_id", "borrado": "SET NULL"},
  {"tabla": "cylinder", "col": "current_order_id", "destino": "order",
   "destcol": "order_id", "borrado": "SET NULL"},
  # Estas aparecieron al barrer el resto del esquema, mas alla de las tres
  # tablas que se revisaron primero.
  {"tabla": "order_dispatch_offer", "col": "distributor_id", "destino": "distributor",
   "destcol": "distributor_id", "borrado": "CASCADE"},
  {"tabla": "order_dispatch_offer", "col": "driver_id", "destino": "user",
   "destcol": "user_id", "borrado": "CASCADE"},
  {"tabla": "incident", "col": "reported_by", "destino": "user",
   "destcol": "user_id", "borrado": "CASCADE"},
  {"tabla": "rating", "col": "to_user_id", "destino": "user",
   "destcol": "user_id", "borrado": "CASCADE"},
]

# ---------------------------------------------------------------- lo propuesto
# El modelo de dominio del 24/09/2026 (material-de-trabajo/MODELO-DE-DOMINIO.md),
# en tablas. Cada agregado dice a que casos de uso responde, que columnas nuevas
# lleva cada tabla existente y que tablas nuevas aparecen. "concepto" es la
# etiqueta en castellano para el modelo conceptual: si esta vacia, el atributo
# no se muestra ahi (claves y campos tecnicos).
#
# Convencion para lo nuevo: columnas en snake_case, fechas en timestamptz, y
# toda referencia a otra tabla con su clave foranea declarada.

def _id(nombre):
    return {"nombre": nombre, "tipo": "uuid", "nulo": False,
            "default": "uuid_generate_v4()", "desc": "Identificador."}

def _ref(nombre, destino, destcol, borrado, desc, nulo=False):
    return {"nombre": nombre, "tipo": "uuid", "nulo": nulo, "desc": desc,
            "ref": (destino, destcol, borrado)}

def _dist():
    return _ref("distributor_id", "distributor", "distributor_id", "CASCADE",
                "Distribuidora dueña.")

# Estados comunes a toda propuesta con vigencia que se negocia con alguien:
# la ventana de taller (M1), la invitacion de recompra (M2), la oferta de lote
# (M3) y el retiro del envase (M4). La oferta de despacho que ya existe usa el
# mismo ciclo con su propio tipo (order_dispatch_offer_status_enum).
PROPUESTA_ESTADOS = ["pending", "accepted", "rejected", "expired"]

PROPUESTO = [
  {
    "clave": "vencimiento-envases",
    "casos": "CU-132 a CU-135",
    "nota": "`cylinder.expires_at` y `cylinder.last_inspection_at` se derivan de la última fila de `cylinder_inspection`. Se guardan desnormalizadas a propósito: el despacho consulta el vencimiento en cada asignación y no conviene recalcularlo por subconsulta.",
    "titulo": "Vigencia de envases",
    "pedido": "Registrar el vencimiento del envase y las revisiones periódicas que "
              "lo renuevan, para no despachar garrafas fuera de norma.",
    "enums": {"cylinder_inspection_result_enum": ["approved", "conditional", "rejected"]},
    "columnas": {
      "cylinder": [
        {"nombre": "manufactured_at", "tipo": "timestamptz", "nulo": True,
         "concepto": "fecha de fabricación", "desc": "Fecha de fabricación grabada en el envase."},
        {"nombre": "last_inspection_at", "tipo": "timestamptz", "nulo": True,
         "concepto": "última revisión", "desc": "Fecha de la última revisión aprobada."},
        {"nombre": "expires_at", "tipo": "timestamptz", "nulo": True,
         "concepto": "vencimiento", "desc": "Fecha hasta la cual el envase puede despacharse."},
      ],
    },
    "tablas": [
      {"nombre": "cylinder_inspection", "concepto": "Revisión de envase",
       "desc": "Una fila por revisión técnica del envase.",
       "columnas": [
         _id("inspection_id"),
         _ref("cylinder_id", "cylinder", "cylinder_id", "CASCADE", "Envase revisado."),
         _dist(),
         {"nombre": "inspected_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "concepto": "fecha", "desc": "Cuándo se hizo la revisión."},
         {"nombre": "result", "tipo": "cylinder_inspection_result_enum", "nulo": False,
          "concepto": "resultado", "desc": "Apta, apta con salvedades o rechazada."},
         {"nombre": "next_due_at", "tipo": "timestamptz", "nulo": True,
          "concepto": "próxima revisión", "desc": "Vencimiento de esta revisión."},
         {"nombre": "notes", "tipo": "text", "nulo": True,
          "concepto": "observaciones", "desc": "Detalle del técnico."},
       ],
       "pk": ["inspection_id"], "unicos": []},
    ],
  },
  {
    "clave": "consumo-recompra",
    "casos": "CU-143 a CU-146 y CU-106 (M2)",
    "nota": "Las columnas van en `customer`, pero el resto del sistema identifica al cliente por `user.user_id` (`order.customer_id` apunta a `user`). Por eso la invitación apunta a `user`. La invitación guarda el pedido sugerido como JSON porque todavía no es un pedido: recién al aceptarla se crean `order` y `order_item`.",
    "titulo": "Consumo declarado y recompra",
    "pedido": "Que el cliente declare cuánto consume por mes, estimar cuándo se le "
              "acaba el gas y ofrecerle la reposición antes, con el pedido armado.",
    "enums": {"repurchase_invitation_status_enum": PROPUESTA_ESTADOS},
    "columnas": {
      "customer": [
        {"nombre": "avg_monthly_consumption_kg", "tipo": "numeric(10,2)", "nulo": True,
         "concepto": "consumo mensual declarado", "desc": "Kilos de gas por mes que declara el cliente."},
        {"nombre": "declared_cylinder_type_id", "tipo": "uuid", "nulo": True,
         "ref": ("gas_cylinder", "gas_cylinder_id", "SET NULL"),
         "concepto": "garrafa habitual", "desc": "Tipo de garrafa que usa habitualmente."},
        {"nombre": "repurchase_notice_days", "tipo": "integer", "nulo": True, "default": "3",
         "concepto": "días de aviso", "desc": "Con cuántos días de anticipación quiere el aviso."},
        {"nombre": "next_repurchase_estimate_at", "tipo": "timestamptz", "nulo": True,
         "concepto": "próxima recompra estimada", "desc": "Fecha estimada de la próxima compra."},
      ],
    },
    "tablas": [
      {"nombre": "repurchase_invitation", "concepto": "Invitación de recompra",
       "desc": "Una oferta de reposición al cliente, con el pedido sugerido y una vigencia.",
       "columnas": [
         _id("invitation_id"), _dist(),
         _ref("user_id", "user", "user_id", "CASCADE", "Cliente invitado."),
         _ref("address_id", "user_address", "address_id", "SET NULL",
              "Dirección sugerida para la entrega.", nulo=True),
         {"nombre": "projected_depletion_at", "tipo": "timestamptz", "nulo": False,
          "concepto": "agotamiento estimado", "desc": "Cuándo se estima que se le acaba el gas."},
         {"nombre": "suggested_items", "tipo": "jsonb", "nulo": False,
          "concepto": "pedido sugerido", "desc": "Productos y cantidades que sugiere el historial."},
         {"nombre": "status", "tipo": "repurchase_invitation_status_enum", "nulo": False,
          "default": "'pending'", "concepto": "estado", "desc": "Pendiente, aceptada, rechazada o caducada."},
         {"nombre": "expires_at", "tipo": "timestamptz", "nulo": False,
          "concepto": "vence", "desc": "Fin de la vigencia de la invitación."},
         {"nombre": "responded_at", "tipo": "timestamptz", "nulo": True,
          "desc": "Cuándo respondió el cliente."},
         _ref("order_id", "order", "order_id", "SET NULL",
              "Pedido creado al aceptar.", nulo=True),
         {"nombre": "created_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "desc": "Cuándo se emitió."},
       ],
       "pk": ["invitation_id"], "unicos": []},
    ],
  },
  {
    "clave": "flota",
    "casos": "CU-136 a CU-142 y CU-105 (M1)",
    "nota": "Seguro, verificación técnica, licencia y mantenimientos son la misma abstracción: un **plan** (la regla: cada cuánto, con qué anticipación, si inhabilita) y sus **tareas** (cada vencimiento concreto). El seguro es un plan de fecha fija que bloquea; el cambio de aceite, uno por kilómetros que no bloquea. La licencia es de la persona y no del vehículo: por eso la tarea apunta a un vehículo **o** a un chofer. Reemplaza la propuesta anterior de columnas sueltas en `car` y `delivery` más una tabla `fleet_maintenance`, que no podía expresar la regla ni alimentar al planificador de M1.",
    "titulo": "Flota: habilitaciones, mantenimiento y uso",
    "pedido": "Llevar seguro, verificación técnica, licencia y mantenimientos, y "
              "planificar el taller antes de que algo venza.",
    "enums": {
      "fleet_status_enum": ["active", "in_service", "grounded"],
      "maintenance_subject_enum": ["vehicle", "driver"],
      "maintenance_trigger_enum": ["by_km", "by_time", "by_fixed_date"],
      "maintenance_criticality_enum": ["blocking", "non_blocking"],
      "maintenance_task_status_enum": ["forecast", "scheduled", "in_progress", "done",
                                       "overdue", "cancelled"],
      "proposal_status_enum": PROPUESTA_ESTADOS,
    },
    "columnas": {
      "car": [
        {"nombre": "tare_weight_kg", "tipo": "numeric(10,2)", "nulo": True,
         "concepto": "tara", "desc": "Peso del vehículo vacío, en kilos."},
        {"nombre": "max_load_kg", "tipo": "numeric(10,2)", "nulo": True,
         "concepto": "carga máxima", "desc": "Carga máxima admitida, en kilos."},
        {"nombre": "odometer_km", "tipo": "integer", "nulo": True,
         "concepto": "kilometraje", "desc": "Última lectura conocida del odómetro."},
        {"nombre": "fleet_status", "tipo": "fleet_status_enum", "nulo": False,
         "default": "'active'", "concepto": "estado en la flota",
         "desc": "Activo, en taller o inhabilitado. Un vehículo inhabilitado no recibe ofertas."},
        {"nombre": "in_service_since", "tipo": "timestamptz", "nulo": True,
         "desc": "Desde cuándo está en taller o inhabilitado."},
      ],
    },
    "tablas": [
      {"nombre": "maintenance_plan", "concepto": "Plan de mantenimiento",
       "desc": "La regla: qué se controla, cada cuánto, con qué anticipación y si inhabilita.",
       "columnas": [
         _id("plan_id"), _dist(),
         {"nombre": "name", "tipo": "varchar(120)", "nulo": False,
          "concepto": "nombre", "desc": "Seguro, VTV, cambio de aceite, licencia..."},
         {"nombre": "subject", "tipo": "maintenance_subject_enum", "nulo": False,
          "concepto": "sobre qué", "desc": "Vehículo o chofer."},
         {"nombre": "trigger", "tipo": "maintenance_trigger_enum", "nulo": False,
          "concepto": "disparo", "desc": "Por kilómetros, por tiempo o por fecha fija."},
         {"nombre": "interval_km", "tipo": "integer", "nulo": True,
          "concepto": "cada cuántos km", "desc": "Intervalo, si el disparo es por kilómetros."},
         {"nombre": "interval_months", "tipo": "integer", "nulo": True,
          "concepto": "cada cuántos meses", "desc": "Intervalo, si el disparo es por tiempo."},
         {"nombre": "lead_time_days", "tipo": "integer", "nulo": False,
          "concepto": "anticipación", "desc": "Con cuántos días de anticipación se planifica."},
         {"nombre": "criticality", "tipo": "maintenance_criticality_enum", "nulo": False,
          "concepto": "criticidad", "desc": "Si al vencer inhabilita o no."},
         {"nombre": "car_type", "tipo": "varchar", "nulo": True,
          "desc": "Tipo de vehículo al que aplica; vacío, a todos."},
         {"nombre": "is_active", "tipo": "boolean", "nulo": False, "default": "true",
          "desc": "Si el plan está vigente."},
       ],
       "pk": ["plan_id"], "unicos": []},
      {"nombre": "maintenance_task", "concepto": "Tarea de mantenimiento",
       "desc": "Cada vencimiento concreto de un plan: una póliza, una VTV, un service.",
       "columnas": [
         _id("task_id"),
         _ref("plan_id", "maintenance_plan", "plan_id", "RESTRICT", "Plan del que sale."),
         _dist(),
         _ref("car_id", "car", "car_id", "CASCADE", "Vehículo, si el plan es de vehículo.", nulo=True),
         _ref("delivery_id", "delivery", "delivery_id", "CASCADE",
              "Chofer, si el plan es de chofer.", nulo=True),
         {"nombre": "status", "tipo": "maintenance_task_status_enum", "nulo": False,
          "default": "'forecast'", "concepto": "estado", "desc": "Proyectada, programada, en curso, hecha, vencida o cancelada."},
         {"nombre": "due_at", "tipo": "timestamptz", "nulo": True,
          "concepto": "vence", "desc": "Fecha de vencimiento, si es de fecha fija."},
         {"nombre": "due_km", "tipo": "integer", "nulo": True,
          "desc": "Kilometraje al que vence, si es por kilómetros."},
         {"nombre": "predicted_due_at", "tipo": "timestamptz", "nulo": True,
          "concepto": "vencimiento proyectado", "desc": "Fecha estimada por el planificador."},
         {"nombre": "scheduled_at", "tipo": "timestamptz", "nulo": True,
          "concepto": "programada para", "desc": "Ventana de taller acordada."},
         {"nombre": "performed_at", "tipo": "timestamptz", "nulo": True,
          "concepto": "realizada", "desc": "Cuándo se hizo."},
         {"nombre": "odometer_km", "tipo": "integer", "nulo": True,
          "desc": "Odómetro al hacerla."},
         {"nombre": "cost", "tipo": "numeric(10,2)", "nulo": True,
          "concepto": "costo", "desc": "Importe del trabajo."},
         {"nombre": "provider", "tipo": "varchar(120)", "nulo": True,
          "concepto": "prestador", "desc": "Aseguradora, taller o ente emisor."},
         {"nombre": "reference_number", "tipo": "varchar(60)", "nulo": True,
          "concepto": "número", "desc": "Póliza, número de licencia u oblea."},
         {"nombre": "category", "tipo": "varchar(10)", "nulo": True,
          "desc": "Categoría habilitante, para la licencia."},
         {"nombre": "notes", "tipo": "text", "nulo": True, "desc": "Detalle."},
       ],
       "pk": ["task_id"], "unicos": []},
      {"nombre": "maintenance_window_proposal", "concepto": "Propuesta de ventana de taller",
       "desc": "Una ventana ofrecida al chofer, de a una por vez, con vigencia.",
       "columnas": [
         _id("proposal_id"),
         _ref("task_id", "maintenance_task", "task_id", "CASCADE", "Tarea a programar."),
         _ref("delivery_id", "delivery", "delivery_id", "CASCADE", "Chofer que decide."),
         {"nombre": "window_start", "tipo": "timestamptz", "nulo": False,
          "concepto": "desde", "desc": "Comienzo de la ventana."},
         {"nombre": "window_end", "tipo": "timestamptz", "nulo": False,
          "concepto": "hasta", "desc": "Fin de la ventana."},
         {"nombre": "rank", "tipo": "integer", "nulo": False,
          "desc": "Orden en que se ofrece."},
         {"nombre": "status", "tipo": "proposal_status_enum", "nulo": False,
          "default": "'pending'", "concepto": "estado", "desc": "Pendiente, aceptada, rechazada o vencida."},
         {"nombre": "expires_at", "tipo": "timestamptz", "nulo": False,
          "concepto": "vence", "desc": "Fin de la vigencia."},
         {"nombre": "responded_at", "tipo": "timestamptz", "nulo": True, "desc": "Cuándo respondió."},
       ],
       "pk": ["proposal_id"], "unicos": []},
      {"nombre": "vehicle_usage_log", "concepto": "Registro de uso del vehículo",
       "desc": "Kilómetros, pedidos y horas en ruta por vehículo y día. Sólo se agrega.",
       "columnas": [
         _id("log_id"),
         _ref("car_id", "car", "car_id", "CASCADE", "Vehículo."),
         _dist(),
         {"nombre": "day", "tipo": "date", "nulo": False, "concepto": "día", "desc": "Día registrado."},
         {"nombre": "km", "tipo": "numeric(10,2)", "nulo": False,
          "concepto": "kilómetros", "desc": "Kilómetros recorridos ese día."},
         {"nombre": "orders", "tipo": "integer", "nulo": False, "default": "0",
          "concepto": "pedidos", "desc": "Pedidos entregados ese día."},
         {"nombre": "route_hours", "tipo": "numeric(6,2)", "nulo": False, "default": "0",
          "desc": "Horas en ruta."},
       ],
       "pk": ["log_id"], "unicos": [["car_id", "day"]]},
    ],
  },
  {
    "clave": "carrito",
    "casos": "CU-122 a CU-126",
    "nota": "El carrito es uno solo por cliente y distribuidora: al confirmarse se vuelca a `order` y `order_item`, que siguen siendo el registro definitivo. `unit_price` guarda el precio del momento en que se agregó el producto, que puede diferir del precio vigente al confirmar.",
    "titulo": "Carrito de compra",
    "pedido": "Que el cliente arme el pedido de a varios productos y lo deje "
              "guardado antes de confirmarlo.",
    "enums": {},
    "columnas": {},
    "tablas": [
      {"nombre": "cart", "concepto": "Carrito",
       "desc": "Un carrito abierto por cliente y distribuidora.",
       "columnas": [
         _id("cart_id"),
         _ref("user_id", "user", "user_id", "CASCADE", "Cliente dueño del carrito."),
         _ref("distributor_id", "distributor", "distributor_id", "CASCADE",
              "Distribuidora a la que le compra."),
         {"nombre": "updated_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "concepto": "última modificación", "desc": "Cuándo se tocó por última vez."},
       ],
       "pk": ["cart_id"], "unicos": [["user_id", "distributor_id"]]},
      {"nombre": "cart_item", "concepto": "Ítem del carrito",
       "desc": "Cada producto cargado en el carrito, con su cantidad.",
       "columnas": [
         _id("cart_item_id"),
         _ref("cart_id", "cart", "cart_id", "CASCADE", "Carrito al que pertenece."),
         _ref("gas_cylinder_id", "gas_cylinder", "gas_cylinder_id", "CASCADE",
              "Tipo de garrafa elegido."),
         {"nombre": "quantity", "tipo": "integer", "nulo": False,
          "concepto": "cantidad", "desc": "Unidades cargadas."},
         {"nombre": "unit_price", "tipo": "numeric(10,2)", "nulo": False,
          "concepto": "precio unitario", "desc": "Precio vigente al agregarlo."},
       ],
       "pk": ["cart_item_id"], "unicos": [["cart_id", "gas_cylinder_id"]]},
    ],
  },
  {
    "clave": "direccion-receptor",
    "casos": "CU-127 y CU-128",
    "titulo": "Cambio de dirección y quién recibe",
    "pedido": "Poder cambiar la dirección de entrega de un pedido ya hecho y "
              "registrar quién lo recibe si no es el cliente.",
    "enums": {},
    "columnas": {
      "order": [
        {"nombre": "receiver_name", "tipo": "varchar(120)", "nulo": True,
         "concepto": "quién recibe", "desc": "Nombre de quien recibe si no es el cliente."},
        {"nombre": "receiver_document", "tipo": "varchar(20)", "nulo": True,
         "concepto": "documento de quien recibe", "desc": "Documento de quien recibe."},
        {"nombre": "receiver_relationship", "tipo": "varchar(40)", "nulo": True,
         "concepto": "vínculo", "desc": "Vínculo con el cliente (familiar, encargado, vecino)."},
      ],
    },
    "tablas": [
      {"nombre": "order_address_change", "concepto": "Cambio de dirección",
       "desc": "Historial de cambios de dirección de entrega sobre un pedido.",
       "columnas": [
         _id("change_id"),
         _ref("order_id", "order", "order_id", "CASCADE", "Pedido afectado."),
         _ref("from_address_id", "user_address", "address_id", "RESTRICT", "Dirección anterior."),
         _ref("to_address_id", "user_address", "address_id", "RESTRICT", "Dirección nueva."),
         _ref("changed_by_user_id", "user", "user_id", "RESTRICT", "Quién hizo el cambio."),
         {"nombre": "changed_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "concepto": "fecha", "desc": "Cuándo se cambió."},
         {"nombre": "reason", "tipo": "text", "nulo": True,
          "concepto": "motivo", "desc": "Motivo declarado del cambio."},
       ],
       "pk": ["change_id"], "unicos": []},
    ],
  },
  {
    "clave": "historial-estados",
    "casos": "CU-018 a CU-020, CU-008 a CU-010 (decidido el 23/09)",
    "nota": "Hoy el pedido guarda sólo su estado actual y algunas marcas de tiempo sueltas (`acceptedAt`, `onTheWayAt`, `deliveredAt`): no queda quién hizo cada cambio ni por qué. Las marcas de tiempo se conservan porque los listados las leen sin unir tablas.",
    "titulo": "Historial de estados del pedido",
    "pedido": "Dejar registro de cada cambio de estado de un pedido: de cuál a "
              "cuál, quién lo hizo, cuándo y por qué.",
    "enums": {},
    "columnas": {},
    "tablas": [
      {"nombre": "order_status_history", "concepto": "Cambio de estado del pedido",
       "desc": "Una fila por transición de estado de un pedido.",
       "columnas": [
         _id("history_id"),
         _ref("order_id", "order", "order_id", "CASCADE", "Pedido."),
         {"nombre": "from_status", "tipo": "order_status_enum", "nulo": True,
          "concepto": "desde", "desc": "Estado anterior; vacío en el alta."},
         {"nombre": "to_status", "tipo": "order_status_enum", "nulo": False,
          "concepto": "hacia", "desc": "Estado nuevo."},
         _ref("changed_by_user_id", "user", "user_id", "SET NULL",
              "Quién lo cambió; vacío si fue un proceso automático.", nulo=True),
         {"nombre": "reason", "tipo": "text", "nulo": True,
          "concepto": "motivo", "desc": "Motivo, cuando la transición lo pide."},
         {"nombre": "changed_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "concepto": "fecha", "desc": "Cuándo."},
       ],
       "pk": ["history_id"], "unicos": []},
    ],
  },
  {
    "clave": "momento-incidencia",
    "casos": "CU de incidencias",
    "titulo": "Momento de la incidencia",
    "pedido": "Distinguir si la incidencia ocurrió antes, durante o después de la "
              "entrega, para saber a quién corresponde resolverla.",
    "enums": {"incident_moment_enum": ["pre_delivery", "in_delivery", "post_delivery"]},
    "columnas": {
      "incident": [
        {"nombre": "moment", "tipo": "incident_moment_enum", "nulo": True,
         "concepto": "momento", "desc": "Antes, durante o después de la entrega."},
      ],
    },
    "tablas": [],
  },
  {
    "clave": "express",
    "casos": "CU-147 a CU-149",
    "nota": "La propuesta anterior sumaba además `is_express`, que repetía lo que ya dice `delivery_mode`. Se saca: con una sola columna no hay forma de que las dos digan cosas distintas.",
    "titulo": "Entrega express",
    "pedido": "Ofrecer una modalidad de entrega inmediata en moto, separada del "
              "reparto programado.",
    "enums": {"order_delivery_mode_enum": ["standard", "express"]},
    "columnas": {
      "order": [
        {"nombre": "delivery_mode", "tipo": "order_delivery_mode_enum", "nulo": False,
         "default": "'standard'", "concepto": "modalidad de entrega",
         "desc": "Reparto programado o express."},
      ],
    },
    "tablas": [],
  },
  {
    "clave": "zonas",
    "casos": "CU-056, CU-150 y CU-151",
    "nota": "Una zona usa recargo fijo o porcentual, nunca los dos: `surcharge` guarda el valor y `surcharge_type` dice cómo leerlo. La vigencia sólo tiene fin; el comienzo programado quedó como decisión pendiente en CU-150.",
    "titulo": "Recargo porcentual y vigencia de zonas",
    "pedido": "Que el recargo de una zona pueda ser un porcentaje, que la zona tenga "
              "etiqueta y color, y que se pueda programar hasta cuándo rige.",
    "enums": {"coverage_zone_surcharge_type_enum": ["fixed", "percentage"]},
    "columnas": {
      "coverage_zone": [
        {"nombre": "surcharge_type", "tipo": "coverage_zone_surcharge_type_enum", "nulo": False,
         "default": "'fixed'", "concepto": "tipo de recargo", "desc": "Monto fijo o porcentaje del pedido."},
        {"nombre": "label", "tipo": "varchar(40)", "nulo": True,
         "concepto": "etiqueta", "desc": "Etiqueta corta para el mapa del panel."},
        {"nombre": "color", "tipo": "varchar(7)", "nulo": True,
         "concepto": "color", "desc": "Color hexadecimal para el mapa del panel."},
        {"nombre": "valid_until", "tipo": "timestamptz", "nulo": True,
         "concepto": "vigente hasta", "desc": "Cuándo deja de aplicarse. Vacío, sin vencimiento."},
      ],
    },
    "tablas": [],
  },
  {
    "clave": "direcciones",
    "casos": "CU-116 y CU-118",
    "nota": "`location` reemplaza a `latitude` y `longitude`, que hoy son `varchar` y no se pueden indexar ni consultar por cercanía. Las dos columnas viejas se conservan hasta que los clientes dejen de mandarlas y después se borran.",
    "titulo": "Dirección resuelta contra el mapa",
    "pedido": "Piso y departamento, y guardar el punto que devuelve el servicio de "
              "mapas junto con la precisión con que se resolvió.",
    "enums": {"address_geocode_precision_enum": ["exact", "approximate", "unresolved"]},
    "columnas": {
      "user_address": [
        {"nombre": "floor", "tipo": "varchar(10)", "nulo": True,
         "concepto": "piso", "desc": "Piso."},
        {"nombre": "apartment", "tipo": "varchar(10)", "nulo": True,
         "concepto": "departamento", "desc": "Departamento."},
        {"nombre": "location", "tipo": "geography(Point,4326)", "nulo": True,
         "concepto": "punto", "desc": "Punto resuelto, en PostGIS."},
        {"nombre": "place_id", "tipo": "varchar(255)", "nulo": True,
         "desc": "Identificador estable del lugar en el servicio de mapas."},
        {"nombre": "geocode_precision", "tipo": "address_geocode_precision_enum", "nulo": False,
         "default": "'unresolved'", "concepto": "precisión", "desc": "Exacta, aproximada o sin resolver."},
      ],
    },
    "tablas": [],
  },
  {
    "clave": "agrupacion",
    "casos": "CU-107 (M3)",
    "nota": "El lote no reemplaza al pedido: cada pedido sigue su ciclo de entrega. El lote sólo decide a quién se asignan juntos y en qué orden. Si no se acepta, se deshace y los pedidos vuelven al despacho individual.",
    "titulo": "Agrupación de pedidos por recorrido",
    "pedido": "Armar lotes de pedidos que se entregan en un mismo viaje y "
              "ofrecerlos a los choferes de a uno.",
    "enums": {"route_batch_status_enum": ["forming", "offered", "assigned", "dissolved", "completed"]},
    "columnas": {},
    "tablas": [
      {"nombre": "route_batch", "concepto": "Lote de recorrido",
       "desc": "Un grupo de pedidos que se entregan en un mismo viaje.",
       "columnas": [
         _id("batch_id"), _dist(),
         {"nombre": "status", "tipo": "route_batch_status_enum", "nulo": False,
          "default": "'forming'", "concepto": "estado", "desc": "Ciclo del lote."},
         {"nombre": "total_weight_kg", "tipo": "numeric(10,2)", "nulo": False,
          "concepto": "peso total", "desc": "Suma del peso de los pedidos."},
         _ref("delivery_id", "delivery", "delivery_id", "SET NULL",
              "Chofer que lo aceptó.", nulo=True),
         {"nombre": "created_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "desc": "Cuándo se armó."},
       ],
       "pk": ["batch_id"], "unicos": []},
      {"nombre": "route_batch_stop", "concepto": "Parada del lote",
       "desc": "Cada pedido del lote, en su orden de entrega.",
       "columnas": [
         _id("stop_id"),
         _ref("batch_id", "route_batch", "batch_id", "CASCADE", "Lote."),
         _ref("order_id", "order", "order_id", "CASCADE", "Pedido."),
         {"nombre": "sequence", "tipo": "integer", "nulo": False,
          "concepto": "orden", "desc": "Posición en el recorrido."},
       ],
       "pk": ["stop_id"], "unicos": [["batch_id", "order_id"]]},
      {"nombre": "route_batch_offer", "concepto": "Oferta de lote",
       "desc": "El lote ofrecido a un chofer, con vigencia.",
       "columnas": [
         _id("offer_id"),
         _ref("batch_id", "route_batch", "batch_id", "CASCADE", "Lote ofrecido."),
         _ref("delivery_id", "delivery", "delivery_id", "CASCADE", "Chofer."),
         {"nombre": "status", "tipo": "proposal_status_enum", "nulo": False,
          "default": "'pending'", "concepto": "estado", "desc": "Pendiente, aceptada, rechazada o vencida."},
         {"nombre": "expires_at", "tipo": "timestamptz", "nulo": False,
          "concepto": "vence", "desc": "Fin de la vigencia."},
         {"nombre": "responded_at", "tipo": "timestamptz", "nulo": True, "desc": "Cuándo respondió."},
       ],
       "pk": ["offer_id"], "unicos": []},
    ],
  },
  {
    "clave": "recupero",
    "casos": "CU-108 (M4)",
    "nota": "El caso se abre sobre un envase que sigue en poder del cliente pasado el plazo, y cada escalón deja su aviso. Ningún depósito se cobra ni ningún envase se da de baja sin una resolución registrada del administrador.",
    "titulo": "Recupero de envases no devueltos",
    "pedido": "Gestionar la devolución de los envases retenidos por escalones, y "
              "escalar al administrador cuando no vuelven.",
    "enums": {
      "recovery_case_status_enum": ["open", "returned", "escalated", "deposit_charged",
                                    "written_off", "closed_no_charge"],
      "recovery_notice_kind_enum": ["reminder", "pickup_offer", "deposit_warning"],
    },
    "columnas": {},
    "tablas": [
      {"nombre": "cylinder_recovery_case", "concepto": "Caso de recupero",
       "desc": "La gestión de un envase retenido por un cliente.",
       "columnas": [
         _id("case_id"), _dist(),
         _ref("cylinder_id", "cylinder", "cylinder_id", "CASCADE", "Envase retenido."),
         _ref("user_id", "user", "user_id", "CASCADE", "Cliente que lo tiene."),
         {"nombre": "delivered_at", "tipo": "timestamptz", "nulo": False,
          "concepto": "entregado el", "desc": "Cuándo se le entregó el envase."},
         {"nombre": "deposit_amount", "tipo": "numeric(10,2)", "nulo": False,
          "concepto": "depósito", "desc": "Importe comprometido."},
         {"nombre": "step", "tipo": "integer", "nulo": False, "default": "1",
          "concepto": "escalón", "desc": "Escalón en curso."},
         {"nombre": "status", "tipo": "recovery_case_status_enum", "nulo": False,
          "default": "'open'", "concepto": "estado", "desc": "Ciclo del caso."},
         {"nombre": "opened_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "desc": "Cuándo se abrió."},
         {"nombre": "closed_at", "tipo": "timestamptz", "nulo": True, "desc": "Cuándo se cerró."},
         _ref("resolved_by_user_id", "user", "user_id", "SET NULL",
              "Administrador que resolvió.", nulo=True),
         {"nombre": "resolution_note", "tipo": "text", "nulo": True,
          "concepto": "resolución", "desc": "Lo que decidió el administrador."},
       ],
       "pk": ["case_id"], "unicos": []},
      {"nombre": "cylinder_recovery_notice", "concepto": "Aviso de recupero",
       "desc": "Cada aviso u oferta de retiro enviados dentro de un caso.",
       "columnas": [
         _id("notice_id"),
         _ref("case_id", "cylinder_recovery_case", "case_id", "CASCADE", "Caso."),
         {"nombre": "step", "tipo": "integer", "nulo": False,
          "concepto": "escalón", "desc": "Escalón al que pertenece."},
         {"nombre": "kind", "tipo": "recovery_notice_kind_enum", "nulo": False,
          "concepto": "tipo", "desc": "Recordatorio, oferta de retiro o aviso de depósito."},
         {"nombre": "status", "tipo": "proposal_status_enum", "nulo": True,
          "desc": "Respuesta, sólo para la oferta de retiro."},
         {"nombre": "sent_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "concepto": "enviado", "desc": "Cuándo se envió."},
         {"nombre": "expires_at", "tipo": "timestamptz", "nulo": False,
          "concepto": "vence", "desc": "Plazo del escalón."},
       ],
       "pk": ["notice_id"], "unicos": []},
    ],
  },
  {
    "clave": "configuracion",
    "casos": "CU-105 a CU-108 y CU-149 (parametrización)",
    "nota": "La cátedra exige que un proceso automatizado sea configurable desde el sistema. Cada módulo guarda sus parámetros en un JSON validado por su propio DTO: los parámetros de M1 no se parecen a los de M3, y una tabla por módulo sería una tabla de una sola fila.",
    "titulo": "Configuración de los procesos automáticos",
    "pedido": "Que el administrador ajuste los parámetros de cada proceso "
              "automático de su distribuidora.",
    "enums": {"configurable_process_enum": ["fleet_planner", "repurchase", "route_batching",
                                            "cylinder_recovery", "express_dispatch"]},
    "columnas": {},
    "tablas": [
      {"nombre": "module_config", "concepto": "Configuración de módulo",
       "desc": "Los parámetros de un proceso automático para una distribuidora.",
       "columnas": [
         _id("config_id"), _dist(),
         {"nombre": "module", "tipo": "configurable_process_enum", "nulo": False,
          "concepto": "módulo", "desc": "Qué proceso configura: uno de los módulos inteligentes o el despacho express."},
         {"nombre": "params", "tipo": "jsonb", "nulo": False,
          "concepto": "parámetros", "desc": "Parámetros, validados por el DTO del módulo."},
         {"nombre": "updated_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "desc": "Última modificación."},
         _ref("updated_by_user_id", "user", "user_id", "SET NULL",
              "Quién la modificó.", nulo=True),
       ],
       "pk": ["config_id"], "unicos": [["distributor_id", "module"]]},
    ],
  },
  {
    "clave": "auditoria",
    "casos": "CU-152 y CU-153",
    "nota": "El registro es de sólo escritura: no hay modificación ni baja para ningún rol. Las referencias al autor y a la distribuidora quedan vacías si esos registros se borran, pero el asiento no se pierde. Necesita índices por fecha, por autor y por distribuidora (CU-152, rendimiento).",
    "titulo": "Registro de auditoría",
    "pedido": "Dejar constancia de toda operación que modifica datos: quién, qué, "
              "sobre qué, cuándo, desde dónde y con qué resultado.",
    "enums": {"audit_result_enum": ["success", "failure"]},
    "columnas": {},
    "tablas": [
      {"nombre": "audit_log", "concepto": "Asiento de auditoría",
       "desc": "Una fila por operación de escritura, exitosa o fallida.",
       "columnas": [
         _id("audit_id"),
         _ref("distributor_id", "distributor", "distributor_id", "SET NULL",
              "Distribuidora de la operación.", nulo=True),
         _ref("actor_user_id", "user", "user_id", "SET NULL",
              "Quién la originó, según su credencial.", nulo=True),
         {"nombre": "actor_role", "tipo": "varchar(30)", "nulo": True,
          "concepto": "rol", "desc": "Rol con que operó."},
         {"nombre": "http_method", "tipo": "varchar(10)", "nulo": False,
          "concepto": "operación", "desc": "POST, PUT, PATCH o DELETE."},
         {"nombre": "resource", "tipo": "varchar(60)", "nulo": False,
          "concepto": "recurso", "desc": "Tipo de recurso afectado."},
         {"nombre": "resource_id", "tipo": "varchar(64)", "nulo": True,
          "desc": "Identificador del recurso, si lo hay."},
         {"nombre": "path", "tipo": "varchar(255)", "nulo": False, "desc": "Ruta invocada."},
         {"nombre": "client_source", "tipo": "varchar(30)", "nulo": True,
          "concepto": "aplicación", "desc": "Panel, app de cliente o app de chofer."},
         {"nombre": "ip", "tipo": "varchar(45)", "nulo": True, "desc": "Dirección de red."},
         {"nombre": "result", "tipo": "audit_result_enum", "nulo": False,
          "concepto": "resultado", "desc": "Exitosa o fallida."},
         {"nombre": "status_code", "tipo": "integer", "nulo": False, "desc": "Código HTTP."},
         {"nombre": "changes", "tipo": "jsonb", "nulo": True,
          "concepto": "cambios", "desc": "Lo que cambió, con credenciales depuradas."},
         {"nombre": "error_message", "tipo": "text", "nulo": True, "desc": "Motivo del rechazo."},
         {"nombre": "created_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "concepto": "fecha", "desc": "Cuándo."},
       ],
       "pk": ["audit_id"], "unicos": []},
    ],
  },
]

# ---------------------------------------------------------------- verificaciones
# El diccionario conceptual mapea etiqueta del negocio -> columna real. Si una
# etiqueta apunta a una columna que no existe, el script corta: en el modelo
# conceptual no puede haber atributos inventados.
CONCEPTO = {
  "distributor": ("Distribuidora", [("razón social", "legal_name"), ("CUIT", "tax_id"),
                                    ("estado", "status")]),
  "user": ("Usuario", [("nombre", "full_name"), ("correo", "email"),
                       ("teléfono", "phone_number")]),
  "role": ("Rol", [("tipo", "type")]),
  "admin": ("Administrador", []),
  "customer": ("Cliente", [("ubicación", "lat_lang"), ("validado", "validated")]),
  "delivery": ("Chofer", [("calificación", "calification"), ("disponible", "isActive"),
                          ("posición", "actual_location"), ("saldo", "balance")]),
  "car": ("Vehículo", [("patente", "car_patent"), ("tipo", "type_car"),
                       ("capacidad", "car_capacity")]),
  "user_address": ("Dirección de entrega", [("calle", "street"), ("ciudad", "city"),
                                            ("predeterminada", "isDefault")]),
  "coverage_zone": ("Zona de cobertura", [("nombre", "name"), ("área", "area"),
                                          ("recargo", "surcharge")]),
  "time_slot": ("Franja horaria", [("nombre", "name"), ("desde", "startTime"),
                                   ("hasta", "endTime"), ("cupo", "capacity")]),
  "gas_cylinder": ("Tipo de garrafa", [("tipo", "type"), ("peso en kg", "weight"),
                                       ("precio", "price"), ("stock", "stock")]),
  "cylinder": ("Envase", [("número de serie", "serial"), ("estado", "state"),
                          ("depósito", "deposit")]),
  "cylinder_movement": ("Movimiento de envase", [("desde", "from_state"), ("hacia", "to_state"),
                                                 ("fecha", "createdAt")]),
  "order": ("Pedido", [("estado", "status"), ("total", "totalAmount"),
                       ("método de pago", "paymentMethod"), ("fecha agendada", "scheduled_date")]),
  "order_item": ("Ítem del pedido", [("cantidad", "quantity"), ("precio unitario", "unitPrice"),
                                     ("subtotal", "subtotal")]),
  "order_dispatch_offer": ("Oferta de despacho", [("estado", "status"), ("vence", "expiresAt")]),
  "payment": ("Pago", [("importe", "amount"), ("pasarela", "gateway"), ("estado", "status")]),
  "claims": ("Reclamo", [("motivo", "reason"), ("estado", "status")]),
  "incident": ("Incidencia", [("tipo", "type"), ("estado", "status")]),
  "rating": ("Calificación", [("puntaje", "stars"), ("comentario", "comment")]),
}

avisos = []
faltan = []
for t, (nom, atts) in CONCEPTO.items():
    if t not in columnas:
        faltan.append(f"CONCEPTO['{t}'] no existe como tabla")
        continue
    reales = {c["nombre"] for c in columnas[t]}
    for etiqueta, col in atts:
        if col not in reales:
            faltan.append(f"CONCEPTO['{t}'] · «{etiqueta}» apunta a {t}.{col}, que no existe")
for t in tablas:
    if t not in CONCEPTO:
        avisos.append(f"la tabla {t} no tiene nombre conceptual")
if faltan:
    sys.exit("El modelo conceptual tiene atributos que no existen en la base:\n  - "
             + "\n  - ".join(faltan))

# Las relaciones sin FK se verifican contra la base: la columna tiene que
# existir, la tabla destino tambien, y no puede haber ya una FK declarada. Si
# algun dia se declara, el script la saca sola de la lista y avisa.
declaradas = {(f["tabla"], f["col"]) for f in fks}
sin_fk = []
for s in SIN_FK:
    if s["tabla"] not in columnas or s["destino"] not in columnas:
        sys.exit(f"SIN_FK: la tabla {s['tabla']} o {s['destino']} no existe")
    col = next((c for c in columnas[s["tabla"]] if c["nombre"] == s["col"]), None)
    if col is None:
        sys.exit(f"SIN_FK: la columna {s['tabla']}.{s['col']} no existe")
    if (s["tabla"], s["col"]) in declaradas:
        avisos.append(f"{s['tabla']}.{s['col']} ya tiene FK declarada: sale de la lista")
        continue
    # Se cuenta contra los datos de hoy cuantas filas apuntan a un destino que
    # ya no existe: son las que harian fallar el ALTER TABLE.
    huerfanas = int(psql(f'''
      select count(*) from "{s["tabla"]}" o
      where o."{s["col"]}" is not null
        and not exists (select 1 from "{s["destino"]}" d
                        where d."{s["destcol"]}" = o."{s["col"]}");''')[0][0])
    s = dict(s, nulo=col["nulo"], huerfanas=huerfanas)
    sin_fk.append(s)

# Lo propuesto tampoco puede pisar lo que ya existe.
enums_prop = {}
for ag in PROPUESTO:
    for n, v in ag["enums"].items():
        if n in enums: sys.exit(f"PROPUESTO: el tipo {n} ya existe en la base")
        enums_prop[n] = v
tablas_prop = []
for ag in PROPUESTO:
    for tb in ag["tablas"]:
        if tb["nombre"] in columnas: sys.exit(f"PROPUESTO: la tabla {tb['nombre']} ya existe")
        tablas_prop.append(tb)
cols_prop = collections.defaultdict(list)   # tabla existente -> columnas nuevas
for ag in PROPUESTO:
    for t, cs in ag["columnas"].items():
        if t not in columnas: sys.exit(f"PROPUESTO: la tabla {t} no existe en la base")
        reales = {c["nombre"] for c in columnas[t]}
        for c in cs:
            if c["nombre"] in reales:
                sys.exit(f"PROPUESTO: la columna {t}.{c['nombre']} ya existe")
            cols_prop[t].append(c)

# ---------------------------------------------------------------------- tipos
def tipo_sql(c):
    """El tipo tal cual esta en la base."""
    u = c["udt"]
    if u in enums: return u
    if u == "varchar": return f"varchar({c['largo']})" if c["largo"] else "varchar"
    if u == "bpchar": return f"char({c['largo']})"
    if u == "numeric" and c["prec"]: return f"numeric({c['prec']},{c['esc']})"
    return {"int4":"integer","int8":"bigint","int2":"smallint","float8":"double precision",
            "float4":"real","bool":"boolean","timestamptz":"timestamptz","timestamp":"timestamp",
            "text":"text","uuid":"uuid","jsonb":"jsonb","date":"date"}.get(u, u)

def portable(tipo):
    """Sin nada propio de PostGIS ni enums: asi lo entiende cualquier
    herramienta que importe SQL."""
    if tipo in enums or tipo in enums_prop: return "varchar(32)"
    if tipo.startswith(("geography", "geometry")): return "varchar(255)"
    return tipo

def tipo_portable(c): return portable(tipo_sql(c))

# ------------------------------------------------------- el modelo, en una pieza
# Se arma una sola estructura con lo implementado y, si corresponde, lo
# propuesto encima. Con eso se escriben todos los archivos sin repetir logica.
def armar(con_propuesta, con_sin_fk):
    m = {}
    for t in tablas:
        cs = [{"nombre": c["nombre"], "tipo": tipo_sql(c), "nulo": c["nulo"], "prop": False}
              for c in columnas[t]]
        rel = [dict(f, prop=False, sinfk=False) for f in fks if f["tabla"] == t]
        if con_sin_fk:
            rel += [{"tabla": t, "col": s["col"], "destino": s["destino"],
                     "destcol": s["destcol"], "borrado": s["borrado"],
                     "prop": False, "sinfk": True} for s in sin_fk if s["tabla"] == t]
        if con_propuesta:
            for c in cols_prop.get(t, []):
                cs.append({"nombre": c["nombre"], "tipo": c["tipo"], "nulo": c["nulo"], "prop": True})
                if "ref" in c:
                    d, dc, br = c["ref"]
                    rel.append({"tabla": t, "col": c["nombre"], "destino": d, "destcol": dc,
                                "borrado": br, "prop": True, "sinfk": False})
        m[t] = {"columnas": cs, "pk": pk[t], "unicos": unicos.get(t, []), "fks": rel, "prop": False}
    if con_propuesta:
        for tb in tablas_prop:
            cs, rel = [], []
            for c in tb["columnas"]:
                cs.append({"nombre": c["nombre"], "tipo": c["tipo"], "nulo": c["nulo"], "prop": True})
                if "ref" in c:
                    d, dc, br = c["ref"]
                    rel.append({"tabla": tb["nombre"], "col": c["nombre"], "destino": d,
                                "destcol": dc, "borrado": br, "prop": True, "sinfk": False})
            m[tb["nombre"]] = {"columnas": cs, "pk": tb["pk"], "unicos": tb["unicos"],
                               "fks": rel, "prop": True}
    return m

def orden_dependencias(modelo):
    """Deja primero las tablas de las que dependen las demas, para que el SQL
    se pueda ejecutar de corrido. A igual nivel, alfabetico."""
    pend, orden, puestas = sorted(modelo), [], set()
    while pend:
        libres = [t for t in pend
                  if all(f["destino"] in puestas or f["destino"] == t for f in modelo[t]["fks"])]
        if not libres: libres = [pend[0]]          # ciclo: se corta por lo alfabetico
        for t in libres:
            orden.append(t); puestas.add(t); pend.remove(t)
    return orden

def crear_tabla(t, d, con_fks=True):
    """CREATE TABLE portable, con PK, UNIQUE y FK adentro."""
    ln = []
    for c in d["columnas"]:
        ln.append(f'  "{c["nombre"]}" {portable(c["tipo"])}' + ("" if c["nulo"] else " NOT NULL"))
    if d["pk"]:
        ln.append("  PRIMARY KEY (" + ", ".join(f'"{c}"' for c in d["pk"]) + ")")
    for g in d["unicos"]:
        ln.append("  UNIQUE (" + ", ".join(f'"{c}"' for c in g) + ")")
    if con_fks:
        for f in d["fks"]:
            ln.append(f'  FOREIGN KEY ("{f["col"]}") REFERENCES "{f["destino"]}" ("{f["destcol"]}")'
                      + ("" if f["borrado"] in ("NO ACTION", "RESTRICT") else f' ON DELETE {f["borrado"]}'))
    return f'CREATE TABLE "{t}" (\n' + ",\n".join(ln) + "\n);\n"

actual = armar(con_propuesta=False, con_sin_fk=False)
completo = armar(con_propuesta=True, con_sin_fk=True)

# ---------------------------------------------- 1. esquema tal cual (pg_dump)
r = subprocess.run(["docker", "exec", CONTENEDOR, "pg_dump", "-U", USR, "-d", BD,
                    "--schema-only", "--schema=public", "--no-owner", "--no-privileges",
                    "-T", "public.migrations", "-T", "public.spatial_ref_sys"],
                   capture_output=True, text=True)
if r.returncode == 0:
    open(SAL + "SPLG-base-de-datos.sql", "w", encoding="utf-8").write(r.stdout)

# ------------------------------------------- 2. esquema actual en SQL portable
sql = ["-- Esquema de SPLG — Sistema de Pedidos y Logística de Garrafas de Gas",
       f"-- Estado actual de la base: {len(tablas)} tablas, {len(fks)} claves foráneas.",
       "-- Generado por generar-modelo-datos.py",
       "-- Los tipos enumerados y los geográficos de PostGIS se escriben como varchar para",
       "-- que cualquier herramienta de diagramación pueda leer el archivo.",
       "-- Las tablas van en orden de dependencia: se puede ejecutar de corrido.", ""]
for t in orden_dependencias(actual):
    sql.append(crear_tabla(t, actual[t]))
open(SAL + "SPLG-base-de-datos-lucidchart.sql", "w", encoding="utf-8").write("\n".join(sql))

# ------------------------------------------------------ 3. solo lo propuesto
prop = ["-- Modelo propuesto — SPLG",
        "-- Los agregados que pidió la cátedra, sobre el esquema que hoy está en la base.",
        "-- PostgreSQL. Se ejecuta en este orden: tipos, columnas nuevas, tablas nuevas,",
        "-- claves foráneas. Generado por generar-modelo-datos.py.", ""]
prop.append("-- ---------- tipos enumerados nuevos ----------")
for ag in PROPUESTO:
    for n, v in ag["enums"].items():
        prop.append(f'CREATE TYPE "{n}" AS ENUM (' + ", ".join(f"'{x}'" for x in v) + ");")
prop.append("")
for ag in PROPUESTO:
    if not ag["columnas"] and not ag["tablas"]: continue
    prop.append(f'-- ---------- {ag["titulo"]} ----------')
    for t, cs in ag["columnas"].items():
        for c in cs:
            d = f' DEFAULT {c["default"]}' if c.get("default") else ""
            prop.append(f'ALTER TABLE "{t}" ADD COLUMN IF NOT EXISTS "{c["nombre"]}" '
                        f'{c["tipo"]}{"" if c["nulo"] else " NOT NULL"}{d};')
    for tb in ag["tablas"]:
        ln = []
        for c in tb["columnas"]:
            d = f' DEFAULT {c["default"]}' if c.get("default") else ""
            ln.append(f'  "{c["nombre"]}" {c["tipo"]}{"" if c["nulo"] else " NOT NULL"}{d}')
        ln.append(f'  CONSTRAINT "PK_{tb["nombre"]}" PRIMARY KEY ('
                  + ", ".join(f'"{c}"' for c in tb["pk"]) + ")")
        for g in tb["unicos"]:
            ln.append(f'  CONSTRAINT "UQ_{tb["nombre"]}_{"_".join(g)}" UNIQUE ('
                      + ", ".join(f'"{c}"' for c in g) + ")")
        prop.append(f'CREATE TABLE IF NOT EXISTS "{tb["nombre"]}" (\n' + ",\n".join(ln) + "\n);")
    prop.append("")
prop.append("-- ---------- claves foráneas de lo propuesto ----------")
for t in orden_dependencias(completo):
    for f in completo[t]["fks"]:
        if not f["prop"]: continue
        prop.append(f'ALTER TABLE "{t}" ADD CONSTRAINT "FK_{t}_{f["col"]}" '
                    f'FOREIGN KEY ("{f["col"]}") REFERENCES "{f["destino"]}" ("{f["destcol"]}") '
                    f'ON DELETE {f["borrado"]};')
prop.append("")
prop.append("-- ---------- relaciones que hoy existen sin clave foránea ----------")
prop.append("-- Las filas huérfanas harían fallar el ALTER: se limpian antes, en la misma migración.")
for s in sin_fk:
    extra = f"  -- {s['huerfanas']} filas huérfanas hoy" if s["huerfanas"] else ""
    prop.append(f'ALTER TABLE "{s["tabla"]}" ADD CONSTRAINT "FK_{s["tabla"]}_{s["col"]}" '
                f'FOREIGN KEY ("{s["col"]}") REFERENCES "{s["destino"]}" ("{s["destcol"]}") '
                f'ON DELETE {s["borrado"]};{extra}')
prop.append("")
open(SAL + "SPLG-base-de-datos-propuesta.sql", "w", encoding="utf-8").write("\n".join(prop))

# --------------------------------------- 4. actual + propuesta, SQL portable
n_fk_completo = sum(len(d["fks"]) for d in completo.values())
comp = ["-- Modelo completo de SPLG — lo implementado más lo que pidió la cátedra",
        f"-- {len(completo)} tablas y {n_fk_completo} relaciones.",
        f"-- Hoy en la base hay {len(tablas)} tablas y {len(fks)} claves foráneas declaradas;",
        f"-- este archivo suma {len(tablas_prop)} tablas nuevas, "
        f"{sum(len(v) for v in cols_prop.values())} columnas nuevas y declara además las",
        f"-- {len(sin_fk)} relaciones que hoy existen en el dominio pero no están declaradas",
        "-- como FOREIGN KEY (ver «Relaciones no declaradas» en SPLG-modelo-de-datos.md).",
        "-- SQL portable: sin tipos enumerados ni tipos de PostGIS, sin defaults ni índices.",
        "-- Las tablas van en orden de dependencia. Generado por generar-modelo-datos.py.", ""]
for t in orden_dependencias(completo):
    d = completo[t]
    comp.append(("-- tabla propuesta\n" if d["prop"] else "") + crear_tabla(t, d))
open(SAL + "SPLG-base-de-datos-completa-lucidchart.sql", "w", encoding="utf-8").write("\n".join(comp))

# ------------------------------------------------------------ estilo comun
AZUL, TINTA = "#1F5E8C", "#2C4257"
CAB = f"""skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam defaultFontName Helvetica
skinparam defaultFontSize 12
skinparam dpi 150
skinparam linetype ortho
skinparam class {{
  BorderColor {TINTA}
  BackgroundColor #FFFFFF
  ArrowColor {TINTA}
  FontSize 12
}}
skinparam class<<propuesto>> {{
  BorderColor {AZUL}
  BackgroundColor #E4EDF4
}}
skinparam legendBackgroundColor #FFFFFF
skinparam legendBorderColor {TINTA}
"""
def leyenda(marca_ref):
    """La misma leyenda en los dos diagramas; solo el físico marca las columnas
    con «ref», porque el conceptual no muestra columnas."""
    return f"""legend bottom
|<#FFFFFF> **implementado** | tabla o atributo que ya existe en la base |
|<#E4EDF4> **propuesto** | agregado pedido por la cátedra, todavía sin implementar |
|<#FFFFFF> **línea punteada{' · «ref»' if marca_ref else ''}** | la relación existe en el dominio pero la base no la declara como clave foránea |
endlegend"""

def marca(c, d):
    """PK, FK, referencia sin declarar o nada, para el modelo físico."""
    if c["nombre"] in d["pk"]: return "<<PK>>", f'**{c["nombre"]}**'
    f = next((x for x in d["fks"] if x["col"] == c["nombre"]), None)
    if f: return ("<<ref>>" if f["sinfk"] else "<<FK>>"), f'//{c["nombre"]}//'
    return "", c["nombre"]

# ----------------------------------------------------------- 5. modelo físico
n_prop_cols = sum(len(v) for v in cols_prop.values())
fis = ["@startuml",
       "title Modelo Físico de Datos — SPLG\\n"
       f"{len(tablas)} tablas y {len(fks)} claves foráneas implementadas · "
       f"{len(sin_fk)} relaciones sin declarar · "
       f"{len(tablas_prop)} tablas y {n_prop_cols} columnas propuestas",
       CAB, "hide circle", ""]
for t in orden_dependencias(completo):
    d = completo[t]
    fis.append(f'entity "{t}" as e_{t}' + (" <<propuesto>> " if d["prop"] else " ") + "{")
    for c in d["columnas"]:
        mk, nom = marca(c, d)
        obl = "" if c["nulo"] else " *"
        linea = f'{nom} : {c["tipo"]}{obl} {mk}'
        fis.append("  {field} " + (f"<color:{AZUL}>{linea} <<propuesto>></color>"
                                   if c["prop"] and not d["prop"] else linea))
    fis.append("}")
fis.append("")
for t in orden_dependencias(completo):
    for f in completo[t]["fks"]:
        uno = f["col"] in unicos_simples.get(t, set())
        der = "||" if uno else "o{"
        if f["sinfk"]:
            fis.append(f'e_{f["destino"]} ||..{der} e_{t} : {f["col"]} (sin FK)')
        elif f["prop"]:
            fis.append(f'e_{f["destino"]} ||--{der} e_{t} #line:{AZUL[1:]};text:{AZUL[1:]} : {f["col"]}')
        else:
            fis.append(f'e_{f["destino"]} ||--{der} e_{t} : {f["col"]}')
fis += ["", leyenda(True), "@enduml"]
open(SAL + "SPLG-modelo-fisico.puml", "w", encoding="utf-8").write("\n".join(fis))

# ------------------------------------------------------- 6. modelo conceptual
# El conceptual habla del negocio: nombres en castellano, sin columnas técnicas
# ni claves. Cada atributo listado corresponde a una columna real, verificada
# más arriba contra la base.
CONCEPTO_PROP = {tb["nombre"]: tb["concepto"] for tb in tablas_prop}

def nombre_concepto(t):
    if t in CONCEPTO: return CONCEPTO[t][0]
    return CONCEPTO_PROP.get(t, t)

# Contextos del negocio (MODELO-DE-DOMINIO.md): cada entidad pertenece a uno.
# Si aparece una tabla sin contexto, el script corta: el modelo tiene que decir
# dónde vive cada cosa.
CONTEXTOS = [
  ("Organización y acceso", ["distributor", "role", "user", "admin", "module_config", "audit_log"]),
  ("Clientes", ["customer", "user_address", "repurchase_invitation"]),
  ("Catálogo e inventario de envases", ["gas_cylinder", "cylinder", "cylinder_movement",
                                        "cylinder_inspection", "cylinder_recovery_case",
                                        "cylinder_recovery_notice"]),
  ("Venta y pedidos", ["cart", "cart_item", "order", "order_item", "order_status_history",
                       "order_address_change", "coverage_zone", "time_slot"]),
  ("Pagos", ["payment"]),
  ("Despacho y logística", ["order_dispatch_offer", "route_batch", "route_batch_stop",
                            "route_batch_offer"]),
  ("Flota y choferes", ["delivery", "car", "maintenance_plan", "maintenance_task",
                        "maintenance_window_proposal", "vehicle_usage_log"]),
  ("Posventa", ["claims", "incident", "rating"]),
]
_en_contexto = [t for _, ts in CONTEXTOS for t in ts]
_sin = sorted(set(completo) - set(_en_contexto))
_sobra = sorted(set(_en_contexto) - set(completo))
if _sin or _sobra:
    sys.exit(f"CONTEXTOS: sin contexto {_sin} · inexistentes {_sobra}")

con = ["@startuml",
       "title Modelo Conceptual — SPLG\\nEntidades del negocio por contexto: lo implementado y lo propuesto",
       CAB, "hide circle", "skinparam linetype polyline",
       "skinparam packageStyle rectangle", f"skinparam package {{\n  BorderColor {TINTA}\n  FontSize 13\n}}", ""]
_orden = orden_dependencias(completo)
for ctx, ts in CONTEXTOS:
  con.append(f'package "{ctx}" {{')
  for t in [x for x in _orden if x in ts]:
    d = completo[t]
    con.append(f'entity "{nombre_concepto(t)}" as c_{t}'
               + (" <<propuesto>> " if d["prop"] else " ") + "{")
    if not d["prop"]:
        for etiqueta, _ in CONCEPTO.get(t, (t, []))[1]:
            con.append("  {field} " + etiqueta)
        for c in cols_prop.get(t, []):
            if c.get("concepto"):
                con.append("  {field} " + f'<color:{AZUL}>{c["concepto"]} <<propuesto>></color>')
    else:
        for c in next(x for x in tablas_prop if x["nombre"] == t)["columnas"]:
            if c.get("concepto"): con.append("  {field} " + c["concepto"])
    con.append("}")
  con.append("}")
con.append("")
vistas = set()
for t in orden_dependencias(completo):
    d = completo[t]
    for f in d["fks"]:
        # Todo pertenece a una distribuidora: esa relación se declara una vez en
        # la leyenda en lugar de dibujar una línea desde cada entidad.
        if f["destino"] == "distributor": continue
        par = (f["destino"], t, f["sinfk"], f["prop"])
        if par in vistas: continue
        vistas.add(par)
        uno = f["col"] in unicos_simples.get(t, set())
        der = "||" if uno else "o{"
        col = next((c for c in d["columnas"] if c["nombre"] == f["col"]), None)
        izq = "|o" if (col and col["nulo"]) else "||"
        if f["sinfk"]:
            con.append(f'c_{f["destino"]} {izq}..{der} c_{t} : sin FK')
        elif f["prop"]:
            con.append(f'c_{f["destino"]} {izq}--{der} c_{t} #line:{AZUL[1:]};text:{AZUL[1:]}')
        else:
            con.append(f'c_{f["destino"]} {izq}--{der} c_{t}')
con += ["", leyenda(False).replace("endlegend",
         "|<#FFFFFF> **distribuidora** | toda entidad pertenece a una distribuidora (multi-tenant): "
         "esas relaciones no se dibujan |\nendlegend"), "@enduml"]
open(SAL + "SPLG-modelo-conceptual.puml", "w", encoding="utf-8").write("\n".join(con))

# --------------------------------------------------- 7. diccionario de datos
md = ["# Modelo de Datos — SPLG", "",
      f"{len(tablas)} tablas y {len(fks)} claves foráneas, leídas de la base en ejecución.", "",
      f"Además de lo implementado, este documento registra {len(sin_fk)} relaciones que el "
      "sistema usa pero que la base no declara, y los agregados que pidió la cátedra.", "",
      "| Sección | Qué contiene |", "|---|---|",
      "| [Diccionario de datos](#diccionario-de-datos) | Las tablas tal cual están hoy en la base |",
      "| [Relaciones no declaradas](#relaciones-no-declaradas) | Columnas que apuntan a otra tabla sin clave foránea |",
      "| [Modelo propuesto](#modelo-propuesto) | Lo que hay que agregar, por pedido de la cátedra |",
      "| [Tipos enumerados](#tipos-enumerados) | Los valores admitidos por cada enumerado |", "",
      "## Diccionario de datos", ""]
for t in tablas:
    nom = CONCEPTO.get(t, (t, []))[0]
    md += [f"### `{t}` — {nom}", "", "| Columna | Tipo | Obligatoria | Clave | Referencia |",
           "|---|---|:-:|:-:|---|"]
    for c in columnas[t]:
        ref = next((f'`{f["destino"]}.{f["destcol"]}`' for f in fks
                    if f["tabla"] == t and f["col"] == c["nombre"]), "")
        if not ref:
            ref = next((f'`{s["destino"]}.{s["destcol"]}` (sin FK)' for s in sin_fk
                        if s["tabla"] == t and s["col"] == c["nombre"]), "")
        clave = ("PK" if c["nombre"] in pk[t]
                 else "FK" if any(f["tabla"] == t and f["col"] == c["nombre"] for f in fks)
                 else "U" if c["nombre"] in unicos_simples.get(t, set()) else "")
        md.append(f'| `{c["nombre"]}` | {tipo_sql(c)} | {"sí" if not c["nulo"] else "no"} '
                  f'| {clave} | {ref} |')
    compuestos = [g for g in unicos.get(t, []) if len(g) > 1]
    if compuestos:
        md += ["", "Claves únicas compuestas: "
               + ", ".join("(" + ", ".join(f"`{c}`" for c in g) + ")" for g in compuestos) + "."]
    md.append("")

md += ["## Relaciones no declaradas", "",
       f"{len(sin_fk)} columnas apuntan a otra tabla y el sistema las usa como referencia, "
       "pero la base no las declara como `FOREIGN KEY`. La consecuencia práctica es que "
       "PostgreSQL no valida que el destino exista ni propaga el borrado: la integridad "
       "queda a cargo de la aplicación. En los diagramas se dibujan con línea punteada y la "
       "etiqueta «sin FK».", "",
       "El destino de cada columna se tomó de la entidad de TypeORM que la define. "
       "La regla de borrado propuesta sigue el patrón del resto del esquema: `CASCADE` "
       "para las columnas obligatorias y para el tenant, `SET NULL` para los punteros "
       "opcionales, `RESTRICT` donde el borrado no debería propagarse.", "",
       "| Tabla | Columna | Apunta a | Obligatoria | Filas huérfanas | Borrado propuesto |",
       "|---|---|---|:-:|:-:|---|"]
for s in sin_fk:
    md.append(f'| `{s["tabla"]}` | `{s["col"]}` | `{s["destino"]}.{s["destcol"]}` '
              f'| {"no" if s["nulo"] else "sí"} | {s["huerfanas"]} | `ON DELETE {s["borrado"]}` |')
md += ["", "El DDL que las declararía:", "", "```sql"]
for s in sin_fk:
    md.append(f'ALTER TABLE "{s["tabla"]}" ADD CONSTRAINT "FK_{s["tabla"]}_{s["col"]}"')
    md.append(f'  FOREIGN KEY ("{s["col"]}") REFERENCES "{s["destino"]}" ("{s["destcol"]}") '
              f'ON DELETE {s["borrado"]};')
_huerfanas = sum(s["huerfanas"] for s in sin_fk)
md += ["```", "",
       ("> La columna «filas huérfanas» se midió contra los datos que hoy tiene la base: "
        + ("no hay ninguna, así que el DDL se puede aplicar tal cual."
           if _huerfanas == 0 else
           f"hay {_huerfanas} filas que apuntan a un identificador que ya no existe y que "
           "hacen fallar el `ALTER TABLE`; hay que limpiarlas antes.")), ""]

md += ["## Modelo propuesto", "",
       f"{len(PROPUESTO)} agregados pedidos por la cátedra: {len(tablas_prop)} tablas nuevas, "
       f"{sum(len(v) for v in cols_prop.values())} columnas nuevas sobre tablas existentes y "
       f"{len(enums_prop)} tipos enumerados nuevos. El DDL completo está en "
       "`SPLG-base-de-datos-propuesta.sql`.", ""]
for i, ag in enumerate(PROPUESTO, 1):
    md += [f"### {i}. {ag['titulo']}", "", f"**Pedido de la cátedra:** {ag['pedido']}", "",
           "| Tabla | Columna | Tipo | Obligatoria | Qué guarda |", "|---|---|---|:-:|---|"]
    for t, cs in ag["columnas"].items():
        for c in cs:
            md.append(f'| `{t}` | `{c["nombre"]}` | {c["tipo"]} '
                      f'| {"sí" if not c["nulo"] else "no"} | {c["desc"]} |')
    for tb in ag["tablas"]:
        for c in tb["columnas"]:
            md.append(f'| `{tb["nombre"]}` **(tabla nueva)** | `{c["nombre"]}` | {c["tipo"]} '
                      f'| {"sí" if not c["nulo"] else "no"} | {c["desc"]} |')
    md.append("")
    for tb in ag["tablas"]:
        refs = [f'`{c["nombre"]}` → `{c["ref"][0]}`' for c in tb["columnas"] if "ref" in c]
        uq = ["(" + ", ".join(f"`{c}`" for c in g) + ")" for g in tb["unicos"]]
        md.append(f'`{tb["nombre"]}` — {tb["desc"]} Clave primaria `{tb["pk"][0]}`.'
                  + (" Referencias: " + ", ".join(refs) + "." if refs else "")
                  + (" Única: " + ", ".join(uq) + "." if uq else ""))
    if ag["enums"]:
        md.append("")
        for n, v in ag["enums"].items():
            md.append(f'Tipo enumerado `{n}`: {", ".join("`"+x+"`" for x in v)}.')
    if ag.get("nota"):
        md += ["", "> **Decisión de modelado.** " + ag["nota"]]
    md.append("")

md += ["## Tipos enumerados", "", "| Tipo | Valores | Estado |", "|---|---|---|"]
for n, v in sorted(enums.items()):
    md.append(f'| `{n}` | {", ".join("`"+x+"`" for x in v)} | implementado |')
for n, v in sorted(enums_prop.items()):
    md.append(f'| `{n}` | {", ".join("`"+x+"`" for x in v)} | propuesto |')
md.append("")
open(SAL + "SPLG-modelo-de-datos.md", "w", encoding="utf-8").write("\n".join(md))

# ------------------------------------------------------------- 8. LEEME.md
leeme = f"""# Modelo de datos de SPLG — qué es cada archivo

Todo lo que hay en esta carpeta lo genera `generar-modelo-datos.py`, que está en
la raíz del repo y lee la base en ejecución (contenedor `{CONTENEDOR}`). No se
edita nada a mano: si cambia la base, se vuelve a correr.

```bash
python3 generar-modelo-datos.py
```

## Los archivos

| Archivo | Qué es | Para qué sirve |
|---|---|---|
| `SPLG-base-de-datos.sql` | Volcado de `pg_dump`, esquema completo | Recrear la base tal cual está |
| `SPLG-base-de-datos-lucidchart.sql` | Sólo lo implementado, en SQL portable | Diagramar el estado actual |
| `SPLG-base-de-datos-propuesta.sql` | Sólo los agregados de la cátedra | Boceto de la migración que falta |
| `SPLG-base-de-datos-completa-lucidchart.sql` | Actual + propuesta, en SQL portable | **El que se importa en Lucidchart** |
| `SPLG-modelo-fisico.png` / `.svg` | Entidad-relación con tablas y columnas | La lámina técnica |
| `SPLG-modelo-conceptual.png` / `.svg` | Entidades del negocio y cardinalidades | La lámina para la defensa |
| `SPLG-modelo-de-datos.md` | Diccionario de datos y sustento escrito | El texto del informe |

En los dos diagramas, lo que ya está implementado va en blanco con borde oscuro
y lo propuesto en celeste con el estereotipo `<<propuesto>>`. Las relaciones que
existen en el dominio pero que la base no declara como clave foránea van con
línea punteada y la etiqueta «sin FK»; en el modelo físico, la columna que las
sostiene lleva la marca `<<ref>>` en lugar de `<<FK>>`.

`SPLG-base-de-datos-propuesta.sql` es PostgreSQL válido: agrega tipos, columnas
y tablas sobre el esquema que ya está, sin tocar los datos existentes.

## Importar en Lucidchart

1. Entrar a Lucidchart y abrir un documento en blanco.
2. En el panel izquierdo, **Import Data** (o *Archivo · Importar datos*).
3. Elegir **Entity Relationship (ERD)**.
4. Elegir el origen **PostgreSQL**.
5. Pegar el contenido de `SPLG-base-de-datos-completa-lucidchart.sql`
   (o subir el archivo, según lo que ofrezca la versión).
6. **Import**. Lucidchart arma una tabla por cada `CREATE TABLE` y una línea por
   cada `FOREIGN KEY`.

Notas para que la importación salga limpia:

- Usar el archivo `-lucidchart.sql`, no `SPLG-base-de-datos.sql`: el volcado de
  `pg_dump` trae `CREATE TYPE`, `CREATE EXTENSION postgis`, índices y funciones
  que el importador no entiende.
- En los archivos portables los tipos enumerados se escriben `varchar(32)` y las
  columnas geográficas de PostGIS `varchar(255)`. La lista de valores de cada
  enumerado está en `SPLG-modelo-de-datos.md`.
- Lucidchart dibuja todas las relaciones iguales: la distinción entre
  implementado, propuesto y «sin FK» sólo se ve en los diagramas de esta carpeta
  y está escrita en el `.md`.
- Si se quiere el estado actual sin los agregados, importar
  `SPLG-base-de-datos-lucidchart.sql`.

## Qué pegarle a Gemini

Para que revise el modelo, el archivo que conviene pasarle es
**`SPLG-modelo-de-datos.md`**: es el único que trae, en un solo texto, el
diccionario de datos, las relaciones que faltan declarar y los agregados
pedidos, cada uno con el motivo por el que está.

Si además se quiere que revise el DDL, sumar
**`SPLG-base-de-datos-completa-lucidchart.sql`**, que es el modelo entero en
menos de {os.path.getsize(SAL + 'SPLG-base-de-datos-completa-lucidchart.sql') // 1024 + 1} KB.
No conviene pegar `SPLG-base-de-datos.sql`: son {os.path.getsize(SAL + 'SPLG-base-de-datos.sql') // 1024} KB
en su mayoría de índices y funciones de PostGIS que no aportan al análisis del
modelo.

Un pedido que funciona bien:

> Adjunto el modelo de datos de un sistema de pedidos y logística de garrafas de
> gas. Revisá normalización, integridad referencial, cardinalidades y nombres.
> Señalá redundancias y relaciones que falten. Tené en cuenta que la sección
> «Modelo propuesto» todavía no está implementada.
"""
open(SAL + "LEEME.md", "w", encoding="utf-8").write(leeme)

# ------------------------------------------------------------------ render
entorno = dict(os.environ, PLANTUML_LIMIT_SIZE="32768")
for n in ("SPLG-modelo-fisico", "SPLG-modelo-conceptual"):
    for fmt in ("png", "svg"):
        r = subprocess.run(["plantuml", "-t"+fmt, "-charset", "UTF-8", SAL+n+".puml"],
                           capture_output=True, text=True, env=entorno)
        if r.returncode: print("  ✗", n, fmt, r.stderr.strip()[:200])
    if os.path.exists(SAL+n+".png"):
        print(f"  ✓ {n} ({os.path.getsize(SAL+n+'.png')//1024} KB)")

for a in avisos: print("  ·", a)
print(f"implementado · tablas: {len(tablas)} · columnas: {sum(len(v) for v in columnas.values())} · "
      f"claves foráneas: {len(fks)} · sin declarar: {len(sin_fk)} · enumerados: {len(enums)}")
print(f"propuesto    · tablas: {len(tablas_prop)} · columnas: {sum(len(v) for v in cols_prop.values())} · "
      f"claves foráneas: {sum(1 for d in completo.values() for f in d['fks'] if f['prop'])} · "
      f"enumerados: {len(enums_prop)}")
print(f"completo     · tablas: {len(completo)} · relaciones: {n_fk_completo}")
