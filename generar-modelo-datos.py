#!/usr/bin/env python3
"""Genera el modelo de datos de SPLG leyendo la base que corre en Docker.

    python3 generar-modelo-datos.py

Sale, en diagramas/base-de-datos/:

  SPLG-base-de-datos.sql                  el esquema tal cual lo devuelve pg_dump
  SPLG-base-de-datos-portable.sql       el esquema actual en SQL portable
  SPLG-base-de-datos-propuesta.sql        solo los agregados pedidos por la catedra
  SPLG-base-de-datos-completa-portable.sql  actual + propuesta, portable, para importar
  fisico/SPLG-fisico-NN-<contexto>.puml/.png/.svg    entidad-relación con tablas y columnas,
                                          una lámina por contexto de negocio
  conceptual/SPLG-der-NN-<área>.puml/...  entidad-relación conceptual con el vocabulario del
                                          modelo conceptual (general y una por área)
  SPLG-der-mermaid.md                     el físico en Mermaid, el que se pega en el Documento 3
  SPLG-modelo-de-datos.md                 el diccionario de datos en texto
  LEEME.md                                como usar cada archivo

Se lee de la base y no de las entidades de TypeORM porque la base es la que manda:
incluye lo que agregaron las migraciones y los indices que no estan en el codigo.

Lo implementado sale de la base. Lo que la catedra pidio agregar vive en la
constante PROPUESTO y se dibuja aparte, con estereotipo <<propuesto>>, para que
en la defensa se distinga de un vistazo lo que ya corre de lo que falta.
"""
import subprocess, os, re, sys, collections, glob, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modelo_conceptual as MC

D = os.path.dirname(os.path.abspath(__file__)) + "/"
SAL = D + "diagramas/base-de-datos/"
os.makedirs(SAL, exist_ok=True)

BACK = os.path.abspath(D + "../splg-app-backend") + "/"
CONTENEDOR = os.environ.get("SPLG_BD_CONTENEDOR", "splg-bd")
env = {}
for l in open(BACK + ".env", encoding="utf-8"):
    m = re.match(r'\s*([A-Z_]+)\s*=\s*(.*)', l)
    if m: env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
USR, BD = env.get("DB_USERNAME", "postgres"), env.get("DB_NAME", "postgres")
# Otra base del mismo contenedor, por ejemplo una copia con un módulo que la doc
# todavía trata como planificado.
BD = os.environ.get("SPLG_BD_NOMBRE", BD)

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
# Un índice único sin condición equivale a una restricción UNIQUE aunque la base no la
# declare como tal (admin.user_id tiene `UQ_admin_user`, un índice). Los parciales
# (`WHERE released_at IS NULL`) no cuentan: solo valen para un subconjunto de filas.
for t, cols in psql(f"""
  select i.indrelid::regclass::text,
         string_agg(a.attname, ',' order by array_position(i.indkey::int2[], a.attnum))
  from pg_index i join pg_attribute a on a.attrelid=i.indrelid and a.attnum = any(i.indkey)
  where i.indisunique and not i.indisprimary and i.indpred is null
    and i.indrelid::regclass::text not in {SALTAR}
  group by i.indexrelid, i.indrelid;"""):
    grupo = cols.split(",")
    t = t.strip('"')
    if grupo not in unicos.get(t, []):
        unicos.setdefault(t, []).append(grupo)
unicos_simples = {t: {g[0] for g in v if len(g) == 1} for t, v in unicos.items()}

fks = []
for t, c, dt, dc, borrado in psql(f"""
  select tc.table_name, kcu.column_name, ccu.table_name, ccu.column_name, rc.delete_rule
  from information_schema.table_constraints tc
  join information_schema.key_column_usage kcu on kcu.constraint_name=tc.constraint_name
  join information_schema.constraint_column_usage ccu on ccu.constraint_name=tc.constraint_name
  join information_schema.referential_constraints rc on rc.constraint_name=tc.constraint_name
  where tc.constraint_type='FOREIGN KEY' and tc.table_schema='public'
    and tc.table_name not in {SALTAR} and ccu.table_name not in {SALTAR}
  order by 1,2;"""):
    fks.append({"tabla": t, "col": c, "destino": dt, "destcol": dc, "borrado": borrado})

enums = {n: v.split(",") for n, v in psql("""
  select t.typname, string_agg(e.enumlabel, ',' order by e.enumsortorder)
  from pg_type t join pg_enum e on e.enumtypid=t.oid
  join pg_namespace n on n.oid=t.typnamespace and n.nspname='public'
  group by t.typname;""")}

# ---------------------------------------------------------- CHECK e indices
# Se piden aparte de information_schema porque una CHECK con OR (como la de
# coverage_zone) no sale completa de information_schema.check_constraints.
checks = collections.defaultdict(list)
for t, nom, defi in psql("""
  select conrelid::regclass::text, conname, pg_get_constraintdef(oid)
  from pg_constraint
  where contype='c' and connamespace='public'::regnamespace
  order by 1, 2;"""):
    checks[t.strip('"')].append((nom, defi))

indices = collections.defaultdict(list)
for t, nom, defi in psql("""
  select tablename, indexname, indexdef
  from pg_indexes
  where schemaname='public'
  order by tablename, indexname;"""):
    # Los indices de PK ya se ven en la columna marcada <<PK>>; no aportan de nuevo.
    if nom.upper().startswith('PK_'): continue
    indices[t].append((nom, defi))

# --------------------------------------------- descripciones desde el código
# El diccionario completo (B-4) pide una descripcion por columna. Se toma del
# comentario que antecede a cada @Column/@PrimaryGeneratedColumn/@Create..
# /@Update../@DeleteDateColumn en la entidad de TypeORM. Si una columna no
# tiene comentario en el código, queda sin descripcion: no se inventa una.
def leer_descripciones_entidades():
    desc = collections.defaultdict(dict)
    decoradores_columna = ('@Column(', '@PrimaryGeneratedColumn(', '@CreateDateColumn(',
                          '@UpdateDateColumn(', '@DeleteDateColumn(')
    for ruta in glob.glob(BACK + "src/**/*.entity.ts", recursive=True):
        src = open(ruta, encoding="utf-8").read()
        m = re.search(r"@Entity\(\s*['\"]([a-zA-Z_]+)['\"]", src)
        if not m: continue
        tabla = m.group(1)
        cm = re.search(r'export\s+class\s+\w+[^{]*\{', src)
        inicio_clase = cm.end() if cm else 0
        props = list(re.finditer(r'^ {2}(\w+)[!?]?\s*:', src, re.M))
        for i, pm in enumerate(props):
            previo = props[i - 1].end() if i else 0
            inicio = max(previo, inicio_clase)
            if pm.start() < inicio: continue     # propiedad de una interfaz anterior a la clase
            segmento = src[inicio:pm.start()]
            if not any(d in segmento for d in decoradores_columna):
                continue
            nm = re.search(r"name:\s*['\"](\w+)['\"]", segmento)
            columna = nm.group(1) if nm else pm.group(1)
            antes = segmento.split('@', 1)[0]
            com = re.search(r'/\*\*(.*?)\*/', antes, re.S)
            if com:
                texto = re.sub(r'\s*\*\s?', ' ', com.group(1)).strip()
            else:
                lns = [l.strip()[2:].strip() for l in antes.strip().splitlines()
                       if l.strip().startswith('//')]
                texto = ' '.join(lns).strip()
            texto = re.sub(r'\s+', ' ', texto)
            if texto:
                desc[tabla][columna] = texto
    return desc

descripciones = leer_descripciones_entidades()

# ------------------------------------------------- relaciones que existen sin FK
# Columnas que apuntan a otra tabla y se usan como referencia en el codigo, pero
# que nunca se declararon como FOREIGN KEY: la base no las valida ni las
# propaga al borrar. El destino de cada una se leyo de la entidad de TypeORM
# correspondiente (los comentarios del backend dicen a que apunta cada columna).
# Las 13 relaciones sin clave foránea se declararon el 25/09/2026
# (migración DeclararRelacionesSinClaveForanea). Hoy no queda ninguna.
SIN_FK = []

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

# Implementado el 25/09/2026 (migración ModeloPropuesto): se conserva como
# registro de dónde salió cada tabla y como especificación contra la que se
# verificó el esquema. Sus etiquetas de negocio alimentan el modelo conceptual.
PROPUESTO_IMPLEMENTADO = [
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
         {"nombre": "alerted_at", "tipo": "timestamptz", "nulo": True,
          "desc": "Cuándo se avisó que vence (CU-142); vacío, sin aviso."},
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
       "desc": "Kilómetros, pedidos y horas en ruta por vehículo y día. Solo se agrega.",
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
    "nota": "Hoy el pedido guarda solo su estado actual y algunas marcas de tiempo sueltas (`acceptedAt`, `onTheWayAt`, `deliveredAt`): no queda quién hizo cada cambio ni por qué. Las marcas de tiempo se conservan porque los listados las leen sin unir tablas.",
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
    "nota": "Una zona usa recargo fijo o porcentual, nunca los dos: `surcharge` guarda el valor y `surcharge_type` dice cómo leerlo. La vigencia solo tiene fin; el comienzo programado quedó como decisión pendiente en CU-150.",
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
    "nota": "El lote no reemplaza al pedido: cada pedido sigue su ciclo de entrega. El lote solo decide a quién se asignan juntos y en qué orden. Si no se acepta, se deshace y los pedidos vuelven al despacho individual.",
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
          "concepto": "monto del depósito", "desc": "Importe comprometido."},
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
          "desc": "Respuesta, solo para la oferta de retiro."},
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
    "nota": "El registro es de solo escritura: no hay modificación ni baja para ningún rol. Las referencias al autor y a la distribuidora quedan vacías si esos registros se borran, pero el asiento no se pierde. Necesita índices por fecha, por autor y por distribuidora (CU-152, rendimiento).",
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
      {"nombre": "audit_action_type", "concepto": "Tipo de acción de auditoría",
       "desc": "Catálogo fijo de las acciones que se auditan: 1 Alta, 2 Modificación, 3 Baja lógica, "
               "4 Reactivación, 5 Baja física. Lo siembra la migración; la API solo lo lee.",
       "columnas": [
         {"nombre": "action_type_id", "tipo": "smallint", "nulo": False,
          "desc": "Identificador fijo de la acción."},
         {"nombre": "name", "tipo": "varchar(40)", "nulo": False, "concepto": "nombre",
          "desc": "Nombre de la acción, único."},
       ],
       "pk": ["action_type_id"], "unicos": [["name"]]},
      {"nombre": "audit", "concepto": "Auditoría",
       "desc": "Una fila por registro de una entidad de negocio que se dio de alta, se modificó, "
               "se dio de baja o se reactivó. De solo escritura: un disparador rechaza todo UPDATE y "
               "DELETE, salvo el que la base hace al vaciar el usuario o la distribuidora.",
       "columnas": [
         _id("audit_id"),
         {"nombre": "action_type_id", "tipo": "smallint", "nulo": False,
          "desc": "Qué se hizo con el registro.",
          "ref": ("audit_action_type", "action_type_id", "RESTRICT")},
         _ref("user_id", "user", "user_id", "SET NULL",
              "Quién lo hizo; vacío si fue el sistema (tarea programada, siembra, notificación sin usuario).",
              nulo=True),
         _ref("distributor_id", "distributor", "distributor_id", "SET NULL",
              "Distribuidora del registro, para acotar la consulta; vacía en lo que es de la persona o global "
              "(usuario, cliente, rol), que solo ve el Administrador General.", nulo=True),
         {"nombre": "entity", "tipo": "varchar(60)", "nulo": False, "concepto": "entidad afectada",
          "desc": "Nombre de la entidad de dominio (Order, Car...), no la ruta."},
         {"nombre": "record_id", "tipo": "varchar(64)", "nulo": False, "concepto": "",
          "desc": "Identificador del registro afectado; en una clave compuesta, las partes separadas por «:»."},
         {"nombre": "ip", "tipo": "varchar(45)", "nulo": True, "concepto": "",
          "desc": "Dirección de red de la petición que originó el cambio."},
         {"nombre": "created_at", "tipo": "timestamptz", "nulo": False, "default": "now()",
          "concepto": "fecha y hora", "desc": "Cuándo."},
       ],
       "pk": ["audit_id"], "unicos": []},
      {"nombre": "audit_detail", "concepto": "Detalle de auditoría",
       "desc": "Un campo que cambió en una auditoría, con su valor anterior y el nuevo, en texto. "
               "Los campos sensibles se guardan como [oculto].",
       "columnas": [
         _id("audit_detail_id"),
         _ref("audit_id", "audit", "audit_id", "RESTRICT", "Auditoría a la que pertenece."),
         {"nombre": "field", "tipo": "varchar(80)", "nulo": False, "concepto": "campo",
          "desc": "Nombre de la propiedad de la entidad que cambió."},
         {"nombre": "old_value", "tipo": "text", "nulo": True, "concepto": "valor anterior",
          "desc": "Valor antes del cambio; vacío en una alta."},
         {"nombre": "new_value", "tipo": "text", "nulo": True, "concepto": "valor nuevo",
          "desc": "Valor después del cambio; vacío en una baja física."},
       ],
       "pk": ["audit_detail_id"], "unicos": []},
    ],
  },
]

def _col(nombre, tipo, desc, nulo=False, default=None, ref=None):
    c = {"nombre": nombre, "tipo": tipo, "nulo": nulo, "desc": desc}
    if default is not None: c["default"] = default
    if ref: c["ref"] = ref
    return c

def _cant(nombre, desc, default="0"):
    return _col(nombre, "integer", desc, default=default)

def _ts(nombre, desc, nulo=True):
    return _col(nombre, "timestamptz", desc, nulo=nulo)

def _usr(nombre, desc, nulo=False):
    return _ref(nombre, "user", "user_id", "RESTRICT", desc, nulo=nulo)

def _gas(desc="Tipo de garrafa."):
    return _ref("gas_cylinder_id", "gas_cylinder", "gas_cylinder_id", "RESTRICT", desc)

# Lo que todavía no está en la base: los cambios de modelo que necesitan los casos de uso
# planificados (Documento 0, plan de construcción). Cada agregado se aplica en la
# iteración que lo necesita, con su propia migración; mientras tanto se dibuja aparte.
# `enum_valores` agrega valores a un tipo enumerado que ya existe.
PROPUESTO = [
  {
    "clave": "express-recargo-y-tipo-de-vehiculo",
    "casos": "CU-147 a CU-149 (C-17)",
    "nota": "La compra express guarda el recargo para poder explicar el total después, igual que el pedido guarda la zona que lo originó. El tipo de vehículo es hoy texto libre (`type_car`: «Moto», «Auto»…) y la express depende de reconocer una moto: se agrega una columna enumerada y se rellena desde `type_car`.",
    "titulo": "Recargo express y tipo de vehículo",
    "pedido": "Explicar el total de un pedido express y reconocer la moto sin depender de un texto libre.",
    "enums": {"vehicle_type_enum": ["motorcycle", "car", "van"]},
    "columnas": {
      "order": [
        {"nombre": "express_surcharge_amount", "tipo": "numeric(12,2)", "nulo": False,
         "default": "0", "desc": "Recargo de la modalidad express incluido en el total; cero en el reparto común."},
      ],
      "car": [
        {"nombre": "vehicle_type", "tipo": "vehicle_type_enum", "nulo": True,
         "desc": "Tipo de vehículo normalizado, rellenado desde `type_car`; vacío hasta el relleno."},
      ],
    },
    "tablas": [],
  },
  {
    "clave": "recupero-baja-y-oferta-de-retiro",
    "casos": "CU-108 (C-15)",
    "nota": "El ciclo del envase no tiene un estado de baja: se agrega una baja lógica en vez de un valor de estado, para no tocar la máquina de estados que ya usan el despacho y la devolución. El aviso de recupero necesita saber a qué entrega se ató la oferta de retiro.",
    "titulo": "Baja del envase y oferta de retiro",
    "pedido": "Poder dar un envase de baja y atar la oferta de retiro a la entrega programada.",
    "enums": {},
    "columnas": {
      "cylinder": [
        {"nombre": "decommissioned_at", "tipo": "timestamptz", "nulo": True,
         "desc": "Cuándo se dio de baja el envase; vacío mientras está en circulación."},
      ],
      "cylinder_recovery_notice": [
        _ref("order_id", "order", "order_id", "SET NULL",
             "Pedido de la entrega a la que se ató la oferta de retiro.", nulo=True),
      ],
    },
    "tablas": [],
  },
  {
    "clave": "configuracion-despacho-y-tareas",
    "casos": "CU-171 y CU-173 (C-07)",
    "nota": "Los parámetros del despacho y la frecuencia de las tareas programadas usan la misma tabla de configuración por distribuidora que los módulos inteligentes: solo hace falta ampliar el tipo enumerado de procesos configurables.",
    "titulo": "Configuración del despacho y de las tareas programadas",
    "pedido": "Que el administrador configure el despacho y la frecuencia de las tareas de su distribuidora.",
    "enums": {},
    "enum_valores": {"configurable_process_enum": ["dispatch", "scheduled_tasks"]},
    "columnas": {},
    "tablas": [],
  },
  {
    "clave": "caja-rendicion-cuentas-corrientes",
    "casos": "CU-225 a CU-245 (C-20)",
    "nota": "Cinco libros de solo agregar (`cash_movement`, `customer_account_entry`, `commission_entry`, y las rendiciones y liquidaciones que los alimentan) sostienen el dinero de la distribuidora. Los libros se corrigen con contraasiento y rechazan todo `UPDATE` y todo `DELETE` por un disparador, igual que `audit_log`. El saldo de `cash_box` y de `customer_account` es una copia del libro que solo cambia por el punto único de escritura, y una conciliación nocturna compara las dos. Hay dos índices únicos parciales que este modelo no puede dibujar: una sesión abierta por caja (`WHERE status = 'open'`) y una cuenta vigente por cliente y distribuidora (`WHERE \"deletedAt\" IS NULL`). El turno del camión (`truck_load_id`) y la carga de combustible (`fuel_load_id`) se agregan a la rendición y a sus gastos cuando se integren los módulos de stock y de flota ampliada; hoy esas tablas no existen. Las comisiones cuelgan del empleado (`employee`, del módulo de personal, que ya está construido), de modo que un chofer cobra comisión como empleado.",
    "titulo": "Caja, rendición del chofer, cuentas corrientes y comisiones",
    "pedido": "Llevar el dinero de la distribuidora —cajas con arqueo, rendición diaria del chofer, venta a crédito y comisiones por entrega— con un libro auditable en vez de saldos sueltos.",
    "enums": {
      "cash_box_kind_enum": ["cash", "bank", "wallet"],
      "cash_session_status_enum": ["open", "closed"],
      "cash_direction_enum": ["income", "expense"],
      "cash_system_code_enum": ["driver_settlement", "customer_payment", "purchase", "fuel", "traffic_fine",
                                "commission_payment", "cash_difference", "box_transfer"],
      "cash_method_enum": ["cash", "transfer", "card", "mercadopago", "check"],
      "cash_reference_type_enum": ["manual", "driver_settlement", "customer_payment", "purchase_receipt",
                                   "fuel_load", "traffic_fine", "driver_liquidation", "box_transfer", "reversal"],
      "driver_settlement_status_enum": ["open", "submitted", "approved"],
      "settlement_difference_resolution_enum": ["none", "charged_to_driver", "absorbed"],
      "tax_condition_enum": ["registered", "monotax", "exempt", "final_consumer"],
      "customer_account_status_enum": ["active", "blocked", "closed"],
      "customer_entry_type_enum": ["sale_charge", "payment", "credit_note", "debit_note", "reversal"],
      "commission_basis_enum": ["per_unit", "per_order", "percent_of_total"],
      "commission_entry_type_enum": ["delivery_commission", "settlement_shortage", "traffic_fine",
                                     "adjustment", "legacy_balance", "carry_forward"],
      "driver_liquidation_status_enum": ["draft", "approved", "paid", "closed", "voided"],
    },
    "enum_valores": {"order_paymentmethod_enum": ["account"], "order_paymenttype_enum": ["account"]},
    "columnas": {},
    "tablas": [
      {"nombre": "cash_box", "concepto": "Caja",
       "desc": "Cuenta de fondos de la distribuidora: efectivo, banco o billetera. Su saldo solo cambia por el libro.",
       "columnas": [
         _id("cash_box_id"), _dist(),
         {"nombre": "name", "tipo": "varchar(80)", "nulo": False, "desc": "Nombre de la caja."},
         {"nombre": "kind", "tipo": "cash_box_kind_enum", "nulo": False, "desc": "Efectivo, banco o billetera."},
         {"nombre": "balance", "tipo": "numeric(14,2)", "nulo": False, "default": "0",
          "desc": "Saldo; una restricción impide que una caja de efectivo quede en negativo."},
         {"nombre": "requires_session", "tipo": "boolean", "nulo": False, "default": "false",
          "desc": "Si exige una sesión abierta para registrar movimientos."},
         {"nombre": "is_active", "tipo": "boolean", "nulo": False, "default": "true", "desc": "Si la caja está activa."},
         {"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Alta."},
         {"nombre": "updatedAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Última modificación."},
         {"nombre": "deletedAt", "tipo": "timestamptz", "nulo": True, "desc": "Baja lógica."},
       ],
       "pk": ["cash_box_id"], "unicos": []},
      {"nombre": "cash_session", "concepto": "Sesión de caja",
       "desc": "Período entre una apertura y un cierre con arqueo de una caja.",
       "columnas": [
         _id("session_id"), _dist(),
         _ref("cash_box_id", "cash_box", "cash_box_id", "CASCADE", "Caja que se abre."),
         {"nombre": "status", "tipo": "cash_session_status_enum", "nulo": False, "default": "'open'",
          "desc": "Abierta o cerrada."},
         {"nombre": "opened_at", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Apertura."},
         _ref("opened_by_user_id", "user", "user_id", "RESTRICT", "Administrador que la abrió."),
         {"nombre": "opening_amount", "tipo": "numeric(12,2)", "nulo": False, "default": "0",
          "desc": "Monto con que se abrió."},
         {"nombre": "closed_at", "tipo": "timestamptz", "nulo": True, "desc": "Cierre."},
         _ref("closed_by_user_id", "user", "user_id", "RESTRICT", "Administrador que la cerró.", nulo=True),
         {"nombre": "expected_amount", "tipo": "numeric(12,2)", "nulo": True,
          "desc": "Monto que debía haber: el inicial más los movimientos de la sesión."},
         {"nombre": "counted_amount", "tipo": "numeric(12,2)", "nulo": True, "desc": "Monto contado en el arqueo."},
         {"nombre": "difference", "tipo": "numeric(12,2)", "nulo": True,
          "desc": "Contado menos esperado; negativa es faltante."},
         {"nombre": "notes", "tipo": "text", "nulo": True, "desc": "Observaciones del arqueo."},
       ],
       "pk": ["session_id"], "unicos": []},
      {"nombre": "cash_category", "concepto": "Categoría de caja",
       "desc": "Categoría de ingreso o de gasto; las de sistema se siembran y no se modifican.",
       "columnas": [
         _id("category_id"), _dist(),
         {"nombre": "name", "tipo": "varchar(80)", "nulo": False, "desc": "Nombre de la categoría."},
         {"nombre": "direction", "tipo": "cash_direction_enum", "nulo": False, "desc": "Ingreso o egreso."},
         {"nombre": "system_code", "tipo": "cash_system_code_enum", "nulo": True,
          "desc": "Código con que los procesos automáticos la buscan; vacío en las propias."},
         {"nombre": "is_active", "tipo": "boolean", "nulo": False, "default": "true", "desc": "Si se ofrece para movimientos nuevos."},
         {"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Alta."},
         {"nombre": "updatedAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Última modificación."},
       ],
       "pk": ["category_id"], "unicos": [["distributor_id", "system_code"]]},
      {"nombre": "cash_movement", "concepto": "Movimiento de caja",
       "desc": "Asiento del libro de una caja; de solo agregar, se corrige con un contraasiento.",
       "columnas": [
         _id("movement_id"), _dist(),
         _ref("cash_box_id", "cash_box", "cash_box_id", "CASCADE", "Caja del asiento."),
         _ref("session_id", "cash_session", "session_id", "SET NULL", "Sesión en que se asentó.", nulo=True),
         {"nombre": "direction", "tipo": "cash_direction_enum", "nulo": False, "desc": "Ingreso o egreso."},
         {"nombre": "amount", "tipo": "numeric(12,2)", "nulo": False, "desc": "Importe, siempre mayor que cero."},
         _ref("category_id", "cash_category", "category_id", "RESTRICT", "Categoría del movimiento."),
         {"nombre": "method", "tipo": "cash_method_enum", "nulo": False, "desc": "Medio, informativo."},
         {"nombre": "occurred_at", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Cuándo ocurrió."},
         {"nombre": "description", "tipo": "varchar(255)", "nulo": True, "desc": "Descripción libre."},
         {"nombre": "reference_type", "tipo": "cash_reference_type_enum", "nulo": False, "default": "'manual'",
          "desc": "Qué lo originó: carga manual, rendición, pago, liquidación, transferencia o anulación."},
         {"nombre": "reference_id", "tipo": "uuid", "nulo": True, "desc": "Identificador de lo que lo originó."},
         _ref("reverses_movement_id", "cash_movement", "movement_id", "RESTRICT",
              "Movimiento al que anula; único: un movimiento se anula una sola vez.", nulo=True),
         _ref("created_by_user_id", "user", "user_id", "RESTRICT", "Quien lo asentó."),
         {"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Alta."},
       ],
       "pk": ["movement_id"], "unicos": [["reverses_movement_id"]]},
      {"nombre": "driver_settlement", "concepto": "Rendición del chofer",
       "desc": "Rendición diaria del efectivo que cobró un chofer.",
       "columnas": [
         _id("settlement_id"), _dist(),
         _ref("delivery_id", "delivery", "delivery_id", "RESTRICT", "Chofer que rinde."),
         {"nombre": "number", "tipo": "integer", "nulo": False, "desc": "Número correlativo por distribuidora."},
         {"nombre": "business_date", "tipo": "date", "nulo": False, "desc": "Día argentino que se rinde."},
         {"nombre": "status", "tipo": "driver_settlement_status_enum", "nulo": False, "default": "'open'",
          "desc": "Abierta, presentada o aprobada."},
         {"nombre": "expected_cash", "tipo": "numeric(12,2)", "nulo": False, "default": "0",
          "desc": "Efectivo que debería entregar."},
         {"nombre": "declared_cash", "tipo": "numeric(12,2)", "nulo": True, "desc": "Efectivo que declara entregar."},
         {"nombre": "driver_expenses", "tipo": "numeric(12,2)", "nulo": False, "default": "0",
          "desc": "Gastos pagados con la cobranza."},
         {"nombre": "difference", "tipo": "numeric(12,2)", "nulo": True,
          "desc": "Declarado más gastos menos esperado; negativa es faltante."},
         {"nombre": "difference_resolution", "tipo": "settlement_difference_resolution_enum", "nulo": True,
          "desc": "Cómo se resolvió la diferencia."},
         _ref("destination_cash_box_id", "cash_box", "cash_box_id", "SET NULL", "Caja donde entró el efectivo.", nulo=True),
         _ref("cash_movement_id", "cash_movement", "movement_id", "SET NULL", "Ingreso a caja de la aprobación.", nulo=True),
         {"nombre": "submitted_at", "tipo": "timestamptz", "nulo": True, "desc": "Cuándo se presentó."},
         _ref("submitted_by_user_id", "user", "user_id", "RESTRICT", "Quien la presentó.", nulo=True),
         {"nombre": "approved_at", "tipo": "timestamptz", "nulo": True, "desc": "Cuándo se aprobó."},
         _ref("approved_by_user_id", "user", "user_id", "RESTRICT", "Administrador que la aprobó.", nulo=True),
         {"nombre": "alerted_at", "tipo": "timestamptz", "nulo": True, "desc": "Cuándo se avisó que seguía sin cerrar."},
         {"nombre": "notes", "tipo": "text", "nulo": True, "desc": "Observaciones."},
         {"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Alta."},
       ],
       "pk": ["settlement_id"], "unicos": []},
      {"nombre": "driver_settlement_order", "concepto": "Pedido rendido",
       "desc": "Pedido en efectivo incluido en una rendición; un pedido se rinde una sola vez.",
       "columnas": [
         _id("settlement_order_id"),
         _ref("settlement_id", "driver_settlement", "settlement_id", "CASCADE", "Rendición que lo incluye."),
         _ref("order_id", "order", "order_id", "RESTRICT", "Pedido rendido; único."),
         {"nombre": "amount", "tipo": "numeric(12,2)", "nulo": False, "desc": "Importe cobrado."},
         {"nombre": "payment_method", "tipo": "order_paymentmethod_enum", "nulo": False,
          "desc": "Medio de pago del pedido al rendirlo."},
       ],
       "pk": ["settlement_order_id"], "unicos": [["order_id"]]},
      {"nombre": "driver_settlement_expense", "concepto": "Gasto de rendición",
       "desc": "Gasto que el chofer pagó con la cobranza.",
       "columnas": [
         _id("expense_id"),
         _ref("settlement_id", "driver_settlement", "settlement_id", "CASCADE", "Rendición que lo declara."),
         _ref("category_id", "cash_category", "category_id", "RESTRICT", "Categoría del gasto."),
         {"nombre": "amount", "tipo": "numeric(12,2)", "nulo": False, "desc": "Importe pagado."},
         {"nombre": "description", "tipo": "varchar(255)", "nulo": True, "desc": "Descripción libre."},
       ],
       "pk": ["expense_id"], "unicos": []},
      {"nombre": "customer_account", "concepto": "Cuenta corriente",
       "desc": "Cuenta corriente de un cliente en una distribuidora: crédito, plazo y saldo.",
       "columnas": [
         _id("account_id"), _dist(),
         _ref("customer_user_id", "user", "user_id", "RESTRICT", "Cliente titular."),
         {"nombre": "business_name", "tipo": "varchar(120)", "nulo": False, "desc": "Razón social."},
         {"nombre": "tax_id", "tipo": "varchar(11)", "nulo": True, "desc": "CUIT."},
         {"nombre": "tax_condition", "tipo": "tax_condition_enum", "nulo": False, "desc": "Condición fiscal."},
         {"nombre": "credit_limit", "tipo": "numeric(12,2)", "nulo": False, "default": "0", "desc": "Límite de crédito."},
         {"nombre": "payment_terms_days", "tipo": "integer", "nulo": False, "default": "30", "desc": "Plazo de pago en días."},
         {"nombre": "status", "tipo": "customer_account_status_enum", "nulo": False, "default": "'active'",
          "desc": "Activa, bloqueada o cerrada."},
         {"nombre": "balance", "tipo": "numeric(14,2)", "nulo": False, "default": "0", "desc": "Saldo; positivo es deuda del cliente."},
         {"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Alta."},
         {"nombre": "updatedAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Última modificación."},
         {"nombre": "deletedAt", "tipo": "timestamptz", "nulo": True, "desc": "Baja lógica."},
       ],
       "pk": ["account_id"], "unicos": []},
      {"nombre": "customer_account_entry", "concepto": "Asiento de cuenta corriente",
       "desc": "Asiento del libro de una cuenta corriente: cargo, pago, nota de crédito o de débito.",
       "columnas": [
         _id("entry_id"), _dist(),
         _ref("account_id", "customer_account", "account_id", "CASCADE", "Cuenta del asiento."),
         {"nombre": "type", "tipo": "customer_entry_type_enum", "nulo": False, "desc": "Cargo, pago, nota o anulación."},
         {"nombre": "amount", "tipo": "numeric(12,2)", "nulo": False, "desc": "Importe; el signo lo da el tipo."},
         _ref("order_id", "order", "order_id", "SET NULL", "Pedido que originó el cargo.", nulo=True),
         {"nombre": "due_date", "tipo": "date", "nulo": True, "desc": "Vencimiento del cargo."},
         {"nombre": "payment_method", "tipo": "cash_method_enum", "nulo": True, "desc": "Medio del pago."},
         _ref("cash_movement_id", "cash_movement", "movement_id", "SET NULL", "Ingreso a caja del pago.", nulo=True),
         _ref("collected_by_delivery_id", "delivery", "delivery_id", "SET NULL", "Chofer que cobró en la calle.", nulo=True),
         _ref("settlement_id", "driver_settlement", "settlement_id", "SET NULL", "Rendición en que entró lo cobrado.", nulo=True),
         _ref("reverses_entry_id", "customer_account_entry", "entry_id", "RESTRICT",
              "Asiento al que anula; único.", nulo=True),
         {"nombre": "description", "tipo": "varchar(255)", "nulo": True, "desc": "Descripción o motivo."},
         {"nombre": "occurred_at", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Cuándo ocurrió."},
         _ref("created_by_user_id", "user", "user_id", "RESTRICT", "Quien lo asentó.", nulo=True),
         {"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Alta."},
       ],
       "pk": ["entry_id"], "unicos": [["reverses_entry_id"]]},
      {"nombre": "customer_account_allocation", "concepto": "Imputación de cuenta corriente",
       "desc": "Aplicación de un pago o una nota de crédito a un cargo; alimenta la antigüedad de la deuda.",
       "columnas": [
         _id("allocation_id"),
         _ref("debit_entry_id", "customer_account_entry", "entry_id", "CASCADE", "Cargo que se cancela."),
         _ref("credit_entry_id", "customer_account_entry", "entry_id", "CASCADE", "Pago o nota que lo cancela."),
         {"nombre": "amount", "tipo": "numeric(12,2)", "nulo": False, "desc": "Importe aplicado."},
       ],
       "pk": ["allocation_id"], "unicos": []},
      {"nombre": "commission_rule", "concepto": "Regla de comisión",
       "desc": "Cuánto gana un chofer por entrega, con su alcance y su vigencia.",
       "columnas": [
         _id("rule_id"), _dist(),
         _ref("employee_id", "employee", "employee_id", "CASCADE", "Empleado de la regla; vacío vale para todos los choferes.", nulo=True),
         _ref("gas_cylinder_id", "gas_cylinder", "gas_cylinder_id", "CASCADE", "Producto de la regla; vacío vale para todos.", nulo=True),
         {"nombre": "basis", "tipo": "commission_basis_enum", "nulo": False, "desc": "Por unidad, por pedido o porcentaje del total."},
         {"nombre": "value", "tipo": "numeric(10,4)", "nulo": False, "desc": "Monto o porcentaje, según la base."},
         {"nombre": "valid_from", "tipo": "date", "nulo": False, "desc": "Inicio de la vigencia."},
         {"nombre": "valid_to", "tipo": "date", "nulo": True, "desc": "Fin de la vigencia."},
         {"nombre": "is_active", "tipo": "boolean", "nulo": False, "default": "true", "desc": "Si la regla está activa."},
         {"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Alta."},
         {"nombre": "updatedAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Última modificación."},
       ],
       "pk": ["rule_id"], "unicos": []},
      {"nombre": "commission_entry", "concepto": "Asiento de comisión",
       "desc": "Asiento del libro de comisiones de un chofer: comisión, deducción o saldo heredado.",
       "columnas": [
         _id("entry_id"), _dist(),
         _ref("employee_id", "employee", "employee_id", "RESTRICT", "Empleado del asiento."),
         {"nombre": "type", "tipo": "commission_entry_type_enum", "nulo": False, "desc": "Comisión, faltante, multa, ajuste, saldo heredado o arrastre."},
         {"nombre": "amount", "tipo": "numeric(12,2)", "nulo": False, "desc": "Importe con signo; las deducciones son negativas."},
         _ref("order_id", "order", "order_id", "SET NULL", "Pedido que devengó la comisión.", nulo=True),
         _ref("rule_id", "commission_rule", "rule_id", "SET NULL", "Regla aplicada.", nulo=True),
         {"nombre": "rule_snapshot", "tipo": "jsonb", "nulo": True, "desc": "Copia de la regla con que se calculó."},
         _ref("settlement_id", "driver_settlement", "settlement_id", "SET NULL", "Rendición que originó un faltante.", nulo=True),
         _ref("liquidation_id", "driver_liquidation", "liquidation_id", "SET NULL", "Liquidación que lo incluye; vacío si está libre.", nulo=True),
         {"nombre": "description", "tipo": "varchar(255)", "nulo": True, "desc": "Descripción o motivo."},
         {"nombre": "occurred_at", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Cuándo ocurrió."},
         _ref("created_by_user_id", "user", "user_id", "RESTRICT", "Quien lo asentó; vacío si fue el sistema.", nulo=True),
         {"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Alta."},
       ],
       "pk": ["entry_id"], "unicos": []},
      {"nombre": "driver_liquidation", "concepto": "Liquidación de comisiones",
       "desc": "Liquidación de las comisiones y las deducciones de un chofer en un período.",
       "columnas": [
         _id("liquidation_id"), _dist(),
         {"nombre": "number", "tipo": "integer", "nulo": False, "desc": "Número correlativo por distribuidora."},
         _ref("employee_id", "employee", "employee_id", "RESTRICT", "Empleado liquidado."),
         {"nombre": "period_from", "tipo": "date", "nulo": False, "desc": "Inicio del período."},
         {"nombre": "period_to", "tipo": "date", "nulo": False, "desc": "Fin del período."},
         {"nombre": "gross", "tipo": "numeric(12,2)", "nulo": False, "desc": "Suma de las comisiones."},
         {"nombre": "deductions", "tipo": "numeric(12,2)", "nulo": False, "desc": "Suma de las deducciones."},
         {"nombre": "net", "tipo": "numeric(12,2)", "nulo": False, "desc": "Neto a pagar."},
         {"nombre": "status", "tipo": "driver_liquidation_status_enum", "nulo": False, "default": "'draft'",
          "desc": "Borrador, aprobada, pagada, cerrada sin pago o anulada."},
         {"nombre": "approved_at", "tipo": "timestamptz", "nulo": True, "desc": "Cuándo se aprobó."},
         _ref("approved_by_user_id", "user", "user_id", "RESTRICT", "Administrador que la aprobó.", nulo=True),
         {"nombre": "paid_at", "tipo": "timestamptz", "nulo": True, "desc": "Cuándo se pagó."},
         _ref("cash_movement_id", "cash_movement", "movement_id", "SET NULL", "Egreso de caja del pago.", nulo=True),
         {"nombre": "createdAt", "tipo": "timestamptz", "nulo": False, "default": "now()", "desc": "Alta."},
       ],
       "pk": ["liquidation_id"], "unicos": []},
    ],
  },
]

# Los módulos de gestión de la distribuidora traen su modelo planificado en un archivo propio.
import propuesto_personal
PROPUESTO += propuesto_personal.AGREGADOS
# Flota ampliada (iteración C-18): combustible, multas, siniestros y neumáticos, en su propio archivo.
import propuesto_flota
PROPUESTO += propuesto_flota.AGREGADOS

# Lo que la base ya tiene deja de ser propuesto (configuración del despacho y las tareas, personal, flota
# ampliada, caja y rendición): sus tablas salen de la base y estos agregados quedan como registro y como fuente de
# las etiquetas de negocio. La columna `car.vehicle_type` no se construyó: la moto se reconoce por `car.type_car`.
_REALIZADOS = {"configuracion-despacho-y-tareas", "caja-rendicion-cuentas-corrientes", "personal-y-legajos",
               "flota-gastos", "flota-neumaticos"}
PROPUESTO_IMPLEMENTADO += [_a for _a in PROPUESTO if _a["clave"] in _REALIZADOS]
PROPUESTO = [_a for _a in PROPUESTO
             if _a["clave"] not in _REALIZADOS | {"express-recargo-y-tipo-de-vehiculo"}]

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
  "customer": ("Cliente", [("ubicación", "location")]),
  "delivery": ("Chofer", [("calificación", "calification"), ("habilitado", "isEnabled"),
                          ("disponible", "isAvailable"),
                          ("posición", "location"), ("saldo", "balance")]),
  "car": ("Vehículo", [("patente", "car_patent"), ("tipo", "type_car"),
                       ("capacidad", "car_capacity")]),
  "vehicle_assignment": ("Asignación de vehículo", [("asignado el", "assigned_at"),
                                                    ("liberado el", "released_at"),
                                                    ("nota", "note")]),
  "user_address": ("Dirección de entrega", [("calle", "street"), ("ciudad", "city"),
                                            ("predeterminada", "isDefault")]),
  "coverage_zone": ("Zona de cobertura", [("nombre", "name"), ("área", "area"),
                                          ("recargo", "surcharge_value"),
                                          ("tipo de recargo", "surcharge_type"),
                                          ("etiqueta", "label"), ("color", "color"),
                                          ("prioridad", "priority"),
                                          ("vigente desde", "valid_from"),
                                          ("vigente hasta", "valid_until")]),
  "time_slot": ("Franja horaria", [("nombre", "name"), ("desde", "startTime"),
                                   ("hasta", "endTime"), ("cupo", "capacity")]),
  "gas_cylinder": ("Tipo de garrafa", [("tipo", "type"), ("peso en kg", "weight"),
                                       ("precio", "price"), ("stock", "stock"),
                                       ("costo promedio", "average_unit_cost")]),
  "gas_cylinder_promotion": ("Promoción", [("desde cantidad", "quantity"),
                                           ("descuento", "discount_percentage")]),
  "cylinder": ("Envase", [("número de serie", "serial"), ("estado", "state"),
                          ("monto del depósito", "deposit")]),
  "cylinder_movement": ("Movimiento de envase", [("desde", "from_state"), ("hacia", "to_state"),
                                                 ("fecha", "createdAt")]),
  "order": ("Pedido", [("estado", "status"), ("total", "totalAmount"),
                       ("método de pago", "paymentMethod"), ("fecha agendada", "scheduled_date"),
                       ("modalidad de entrega", "delivery_mode"),
                       ("recargo de zona", "zone_surcharge_amount"),
                       ("subtotal de ítems", "subtotal_items"),
                       ("nombre de quien recibe", "receiver_name"),
                       ("documento de quien recibe", "receiver_document"),
                       ("vínculo de quien recibe", "receiver_relationship")]),
  "order_item": ("Ítem del pedido", [("cantidad", "quantity"), ("precio unitario", "unitPrice"),
                                     ("subtotal", "subtotal")]),
  "order_dispatch_offer": ("Oferta de despacho", [("estado", "status"), ("vence", "expiresAt")]),
  "payment": ("Pago", [("importe", "amount"), ("pasarela", "gateway"), ("estado", "status")]),
  "payment_refund": ("Reintegro de pago", [("tipo", "kind"), ("importe", "amount"), ("estado", "status"),
                                            ("intentos", "attempts"), ("reintegrado el", "refunded_at"),
                                            ("referencia en la pasarela", "gateway_refund_id"),
                                            ("mensaje de error", "error_message"),
                                            ("devuelto antes del intento", "refunded_baseline")]),
  "driver_settlement_collection": ("Cobro de rendición", [("importe", "amount")]),
  "maintenance_task_attachment": ("Adjunto de tarea de mantenimiento",
    [("nombre original", "original_name"), ("tipo de archivo", "mime_type"),
     ("tamaño", "size_bytes"), ("subido el", "uploaded_at")]),
  "attachment": ("Adjunto", [("nombre original", "original_name"), ("tipo de archivo", "mime_type"),
                             ("etiqueta", "label"), ("fecha de carga", "uploaded_at")]),
  "job_position": ("Puesto de trabajo", [("nombre", "name"), ("categoría", "category"),
                                         ("activo", "is_active")]),
  "employee": ("Empleado", [("legajo", "file_number"), ("nombre", "first_name"), ("apellido", "last_name"),
                            ("documento", "document_number"), ("CUIL", "cuil"),
                            ("fecha de nacimiento", "birth_date"), ("domicilio", "address_line"),
                            ("teléfono", "phone"), ("contacto de emergencia", "emergency_contact_name"),
                            ("fecha de ingreso", "hire_date"), ("fecha de egreso", "termination_date"),
                            ("motivo de egreso", "termination_reason"),
                            ("modalidad de contratación", "employment_type"), ("estado", "status")]),
  "document_sequence": ("Secuencia de documentos", [("tipo de documento", "doc_type"),
                                                    ("último número", "last_number")]),
  "storage_orphan": ("Archivo pendiente de borrado", [("clave", "storage_key"), ("intentos", "attempts"),
                                                       ("estado", "status")]),
  "warehouse": ("Depósito", [("nombre", "name"), ("código", "code"), ("tipo", "kind"),
                             ("dirección", "address"), ("predeterminado", "is_default"),
                             ("activo", "is_active")]),
  "stock_location": ("Ubicación de stock", [("tipo", "kind")]),
  "stock_balance": ("Saldo de stock", [("condición", "condition"), ("cantidad", "quantity")]),
  "stock_movement": ("Movimiento de stock", [("cantidad", "quantity"),
                                             ("condición de origen", "from_condition"),
                                             ("condición de destino", "to_condition"),
                                             ("motivo", "reason"),
                                             ("documento de origen", "reference_type"),
                                             ("observación", "notes"), ("fecha", "occurred_at")]),
  "stock_threshold": ("Umbral de stock", [("mínimo de llenas", "min_full"),
                                          ("avisado el", "alerted_at")]),
  "stock_adjustment": ("Ajuste de stock", [("número", "number"), ("motivo", "reason"),
                                           ("nota", "notes"), ("fecha", "createdAt")]),
  "stock_adjustment_item": ("Renglón de ajuste de stock", [("condición", "condition"),
                                                            ("diferencia", "quantity_delta")]),
  "truck_load": ("Carga del camión", [("número", "number"), ("día", "business_date"), ("estado", "status"),
                                      ("abierta el", "opened_at"), ("salió el", "departed_at"),
                                      ("regresó el", "returned_at"), ("cerrada el", "closed_at"),
                                      ("nota de diferencia", "difference_note"),
                                      ("motivo de cancelación", "cancel_reason"), ("notas", "notes")]),
  "truck_load_item": ("Renglón de carga", [("llenas cargadas", "loaded_full"),
                                           ("llenas repuestas", "reloaded_full"),
                                           ("vacías cargadas", "loaded_empty"),
                                           ("llenas declaradas al regreso", "declared_return_full"),
                                           ("vacías declaradas al regreso", "declared_return_empty"),
                                           ("llenas entregadas", "delivered_full"),
                                           ("vacías recolectadas", "collected_empty"),
                                           ("/llenas esperadas", "expected_full"),
                                           ("/vacías esperadas", "expected_empty"),
                                           ("diferencia de llenas", "difference_full"),
                                           ("diferencia de vacías", "difference_empty")]),
  "supplier": ("Proveedor", [("razón social", "business_name"), ("CUIT", "cuit"), ("tipo", "kind"),
                             ("contacto", "contact_name"), ("teléfono", "phone"), ("correo", "email"),
                             ("dirección", "address"), ("plazo de pago", "payment_terms_days"),
                             ("activo", "is_active")]),
  "purchase_order": ("Orden de compra", [("número", "number"), ("estado", "status"),
                                         ("emitida el", "issued_at"), ("fecha esperada", "expected_date"),
                                         ("total", "total_amount"),
                                         ("motivo de cancelación", "cancel_reason"),
                                         ("motivo de cierre", "close_reason"), ("notas", "notes")]),
  "purchase_order_item": ("Renglón de orden de compra", [("cantidad", "quantity"),
                                                         ("costo unitario", "unit_cost"),
                                                         ("vacíos a canjear", "empties_to_exchange"),
                                                         ("cantidad recibida", "received_quantity")]),
  "purchase_receipt": ("Recepción de compra", [("número", "number"),
                                               ("tipo de comprobante", "supplier_document_type"),
                                               ("número de comprobante", "supplier_document_number"),
                                               ("recibida el", "received_at"), ("total", "total_amount"),
                                               ("estado de pago", "payment_status"), ("estado", "status"),
                                               ("motivo de anulación", "void_reason"),
                                               ("anulada el", "voided_at"), ("notas", "notes")]),
  "purchase_receipt_item": ("Renglón de recepción de compra",
                            [("llenas recibidas", "quantity_full"), ("vacías entregadas", "quantity_empty_out"),
                             ("costo unitario", "unit_cost"), ("costo promedio previo", "previous_average_cost"),
                             ("existencia previa", "previous_on_hand")]),
  "stock_reconciliation_alert": ("Aviso de conciliación de stock",
                                 [("firma de las diferencias", "signature"),
                                  ("avisada el", "alerted_at")]),
  "claims": ("Reclamo", [("motivo", "reason"), ("estado", "status")]),
  "incident": ("Incidencia", [("tipo", "type"), ("estado", "status")]),
  "rating": ("Calificación", [("puntaje", "stars"), ("comentario", "comment")]),
}

# Las tablas y columnas que venían de la propuesta traen su etiqueta de negocio.
for _ag in PROPUESTO_IMPLEMENTADO:
    for _tb in _ag["tablas"]:
        CONCEPTO.setdefault(_tb["nombre"], (_tb["concepto"], []))
        _nom, _atts = CONCEPTO[_tb["nombre"]]
        CONCEPTO[_tb["nombre"]] = (_nom, _atts + [(c["concepto"], c["nombre"])
                                                  for c in _tb["columnas"] if c.get("concepto")])
    for _t, _cs in _ag["columnas"].items():
        _nom, _atts = CONCEPTO[_t]
        CONCEPTO[_t] = (_nom, _atts + [(c["concepto"], c["nombre"]) for c in _cs if c.get("concepto")])

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

# Si otro módulo ya llevó a la base una tabla o un tipo que el modelo propuesto traía (los adjuntos
# genéricos, por ejemplo), deja de ser propuesto: se toma de la base.
for _ag in PROPUESTO:
    _ag["tablas"] = [tb for tb in _ag["tablas"] if tb["nombre"] not in columnas]
    _ag["enums"] = {n: v for n, v in _ag["enums"].items() if n not in enums}
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
    if tipo.endswith("[]"): return "varchar(255)"
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
open(SAL + "SPLG-base-de-datos-portable.sql", "w", encoding="utf-8").write("\n".join(sql))

# ------------------------------------------------------ 3. solo lo propuesto
prop = ["-- Modelo propuesto — SPLG",
        "-- Los cambios de modelo de los casos de uso planificados, sobre el esquema que hoy está en la base.",
        "-- PostgreSQL. Se ejecuta en este orden: tipos, columnas nuevas, tablas nuevas,",
        "-- claves foráneas. Generado por generar-modelo-datos.py.", ""]
prop.append("-- ---------- tipos enumerados nuevos ----------")
for ag in PROPUESTO:
    for n, v in ag["enums"].items():
        prop.append(f'CREATE TYPE "{n}" AS ENUM (' + ", ".join(f"'{x}'" for x in v) + ");")
prop.append("")
prop.append("-- ---------- valores nuevos de tipos enumerados existentes ----------")
for ag in PROPUESTO:
    for n, v in ag.get("enum_valores", {}).items():
        for x in v:
            prop.append(f'ALTER TYPE "{n}" ADD VALUE IF NOT EXISTS \'{x}\';')
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
comp = ["-- Modelo completo de SPLG: lo implementado más lo planificado",
        f"-- {len(completo)} tablas y {n_fk_completo} relaciones.",
        f"-- Hoy en la base hay {len(tablas)} tablas y {len(fks)} claves foráneas declaradas;",
        f"-- este archivo suma {len(tablas_prop)} tablas planificadas y "
        f"{sum(len(v) for v in cols_prop.values())} columnas nuevas en tablas que ya existen."]
if sin_fk:
    comp += [f"-- Declara además las {len(sin_fk)} relaciones que hoy existen en el dominio pero no están declaradas",
             "-- como FOREIGN KEY (ver «Relaciones no declaradas» en SPLG-modelo-de-datos.md)."]
comp += ["-- SQL portable: sin tipos enumerados ni tipos de PostGIS, sin defaults ni índices.",
         "-- Las tablas van en orden de dependencia. Generado por generar-modelo-datos.py.", ""]
for t in orden_dependencias(completo):
    d = completo[t]
    comp.append(("-- tabla propuesta\n" if d["prop"] else "") + crear_tabla(t, d))
open(SAL + "SPLG-base-de-datos-completa-portable.sql", "w", encoding="utf-8").write("\n".join(comp))

# ------------------------------------------------------------ estilo comun
AZUL, TINTA = "#1F5E8C", "#2C4257"
RUTA_ESTILO = "../../estilo-vp.iuml"
CAB = f"""!include {RUTA_ESTILO}
skinparam entity<<ajena>> {{
  BackgroundColor #F1F1F1
  BorderColor #8A97A3
  FontColor #55616C
}}
skinparam class<<propuesto>> {{
  BorderColor {AZUL}
  BackgroundColor #FFF6D9
}}
skinparam entity<<propuesto>> {{
  BorderColor {AZUL}
  BackgroundColor #FFF6D9
}}
"""
def leyenda(marca_ref):
    """La misma leyenda en los dos diagramas; solo el físico marca las columnas
    con «ref», porque el conceptual no muestra columnas. Las filas de lo
    propuesto y de las relaciones sin clave foránea salen solo si hay alguna."""
    filas = ["|<#FFFFFF> **implementado** | tabla o atributo que ya existe en la base |"]
    if PROPUESTO:
        filas.append("|<#FFF6D9> **propuesto** | cambio planificado, todavía sin aplicar a la base |")
    if SIN_FK:
        filas.append(f"|<#FFFFFF> **línea punteada{' · «ref»' if marca_ref else ''}** | la relación existe "
                     "en el dominio pero la base no la declara como clave foránea |")
    return "legend bottom\n" + "\n".join(filas) + "\nendlegend"

def marca(c, d):
    """PK, FK, referencia sin declarar o nada, para el modelo físico."""
    if c["nombre"] in d["pk"]: return "<<PK>>", f'**{c["nombre"]}**'
    f = next((x for x in d["fks"] if x["col"] == c["nombre"]), None)
    if f: return ("<<ref>>" if f["sinfk"] else "<<FK>>"), f'//{c["nombre"]}//'
    return "", c["nombre"]

# Contextos del negocio (MODELO-DE-DOMINIO.md): cada entidad pertenece a uno.
# Si aparece una tabla sin contexto, el script corta: el modelo tiene que decir
# dónde vive cada cosa.
CONTEXTOS = [
  ("Organización y acceso", ["distributor", "role", "user", "admin", "module_config", "audit_log",
                           "audit", "audit_detail", "audit_action_type"]),
  ("Clientes", ["customer", "user_address", "repurchase_invitation"]),
  ("Catálogo e inventario de envases", ["gas_cylinder", "gas_cylinder_promotion", "cylinder", "cylinder_movement",
                                        "cylinder_inspection", "cylinder_recovery_case",
                                        "cylinder_recovery_notice"]),
  ("Venta y pedidos", ["cart", "cart_item", "order", "order_item", "order_status_history",
                       "order_address_change", "coverage_zone", "time_slot"]),
  ("Pagos", ["payment", "payment_refund"]),
  ("Despacho y logística", ["order_dispatch_offer", "route_batch", "route_batch_stop",
                            "route_batch_offer"]),
  ("Flota y choferes", ["delivery", "car", "vehicle_assignment", "maintenance_plan", "maintenance_task",
                        "maintenance_task_attachment", "maintenance_window_proposal",
                        "vehicle_usage_log"]),
  ("Posventa", ["claims", "incident", "rating"]),
  (propuesto_personal.CONTEXTO[0], propuesto_personal.CONTEXTO[1] + ["attachment"]),
  ("Gastos de la flota", ["fuel_load", "traffic_fine", "vehicle_accident", "tire", "tire_event"]),
  ("Stock físico y carga del camión", ["warehouse", "stock_location", "stock_balance", "stock_movement",
                                      "stock_threshold", "stock_adjustment", "stock_adjustment_item",
                                      "truck_load", "truck_load_item"]),
  ("Compras", ["supplier", "purchase_order", "purchase_order_item", "purchase_receipt",
               "purchase_receipt_item"]),
  ("Tablas técnicas", sorted(MC.TABLAS_TECNICAS)),
  ("Caja y finanzas", ["cash_box", "cash_session", "cash_category", "cash_movement", "driver_settlement",
                       "driver_settlement_order", "driver_settlement_expense", "driver_settlement_collection",
                       "customer_account",
                       "customer_account_entry", "customer_account_allocation", "commission_rule",
                       "commission_entry", "driver_liquidation"]),
]
_en_contexto = [t for _, ts in CONTEXTOS for t in ts]
_sin = sorted(set(completo) - set(_en_contexto))
_sobra = sorted(set(_en_contexto) - set(completo))
if _sin or _sobra:
    sys.exit(f"CONTEXTOS: sin contexto {_sin} · inexistentes {_sobra}")


# ---------------------------------------------------------------- cardinalidades
# Una clave foránea es «muchos a uno»; si la columna es única es «uno a cero-o-uno»
# (user -> admin, customer, delivery). El lado del padre es obligatorio si la columna no
# admite nulos. Las columnas únicas incluyen los índices únicos (ver más arriba).
IZQ = {"uno": "||", "cero_uno": "|o", "muchos": "}o",
       # multiplicidades del modelo conceptual, para el DER conceptual
       "1": "||", "0..1": "|o", "0..*": "}o", "*": "}o", "1..*": "}|"}
DER = {"uno": "||", "cero_uno": "o|", "muchos": "o{",
       "1": "||", "0..1": "o|", "0..*": "o{", "*": "o{", "1..*": "|{"}

def _aprox(m):
    """La multiplicidad que pata de gallo sí puede dibujar."""
    if m in IZQ: return m
    lo = m.split("..")[0]
    return "1..*" if lo not in ("0", "") else "0..*"

def card_hijo(t, f):
    prop = {g[0] for g in completo[t]["unicos"] if len(g) == 1} if t in completo else set()
    return "cero_uno" if f["col"] in unicos_simples.get(t, set()) | prop else "muchos"

def card_padre(t, f):
    col = next((c for c in completo[t]["columnas"] if c["nombre"] == f["col"]), None)
    return "cero_uno" if (col and col["nulo"]) else "uno"

CONVENCIONES = ("Los nombres reflejan la base real: conviven camelCase "
                "(paymentMethod, createdAt, isActive) y snake_case (scheduled_date, "
                "delivery_mode) porque las columnas más antiguas se crearon así y las "
                "posteriores siguieron otra convención; la tabla claims está en plural y el "
                "resto en singular.")

# ----------------------------------------------------------- 5. modelo físico
# Una lámina por contexto de negocio, con las tablas del contexto completas y, como
# referencia, el nombre de las tablas de otros contextos a las que apuntan.
FIS = SAL + "fisico/"
os.makedirs(FIS, exist_ok=True)
for _viejo in glob.glob(FIS + "SPLG-fisico-*"): os.remove(_viejo)
for _viejo in glob.glob(SAL + "SPLG-modelo-fisico.*"): os.remove(_viejo)

def slug(txt):
    import unicodedata
    n = unicodedata.normalize("NFD", txt.lower())
    return re.sub(r'[^a-z0-9]+', '-', "".join(c for c in n if not unicodedata.combining(c))).strip("-")

fisicos = []
_orden_global = orden_dependencias(completo)

# Vista general: la base que existe hoy, entera, en una sola lámina. Para que se lea con
# 48 tablas, cada una muestra solo su clave primaria y sus claves foráneas (las columnas
# completas están en la lámina de su contexto y en el diccionario de datos), agrupadas
# por contexto de negocio. La FK a distributor no se dibuja: la tienen casi todas.
def _fisico_general():
    lin = ["@startuml", "title Modelo físico de la base de datos — vista general (tablas implementadas)",
           CAB, "hide circle", "left to right direction", "skinparam linetype ortho", "skinparam nodesep 40",
           "skinparam ranksep 60", "skinparam packageStyle rectangle", ""]
    implementadas = [t for t in _orden_global if t in actual]
    for ctx, ts in CONTEXTOS:
        propias = [t for t in implementadas if t in ts]
        if not propias: continue
        lin.append(f'package "{ctx}" {{')
        for t in propias:
            d = actual[t]
            lin.append(f'  entity "{t}" as e_{t} {{')
            for c in d["columnas"]:
                mk, nom = marca(c, d)
                if not mk or (mk != "<<PK>>" and c["nombre"] == "distributor_id"): continue
                lin.append(f'    {{field}} {nom} : {c["tipo"]}{"" if c["nulo"] else " *"} {mk}'.rstrip())
            lin.append("  }")
        lin.append("}")
    lin.append("")
    vistos = set()
    for t in implementadas:
        for f in actual[t]["fks"]:
            if f["destino"] == "distributor" and t != "distributor" or f["destino"] not in actual: continue
            if (t, f["col"]) in vistos: continue
            vistos.add((t, f["col"]))
            lin.append(f'e_{f["destino"]} {IZQ[card_padre(t, f)]}--{DER[card_hijo(t, f)]} e_{t}')
    n_dist = sum(1 for t in implementadas if any(f["destino"] == "distributor" for f in actual[t]["fks"]))
    lin += ["", "legend bottom right",
            f"  {len(implementadas)} tablas implementadas y {len(vistos)} relaciones dibujadas.",
            f"  Además, {n_dist} tablas tienen distributor_id (FK a distributor, multi-distribuidora): esa línea no se dibuja.",
            "  Cada tabla muestra solo su PK y sus FK; las columnas completas están en la lámina de su contexto",
            "  y en el diccionario de datos. * = obligatoria.",
            "endlegend", "@enduml"]
    return "\n".join(lin)

open(FIS + "SPLG-fisico-00-general.puml", "w", encoding="utf-8").write(_fisico_general())
fisicos.append("SPLG-fisico-00-general")
for k, (ctx, ts) in enumerate(CONTEXTOS, 1):
    propias = [t for t in _orden_global if t in ts]
    ajenas = []
    for t in propias:
        for f in completo[t]["fks"]:
            if f["destino"] not in ts and f["destino"] != "distributor" and f["destino"] not in ajenas:
                ajenas.append(f["destino"])
    lin = ["@startuml",
           f"title Modelo físico — {ctx}", CAB, "hide circle", "skinparam linetype polyline", ""]
    for t in propias:
        d = completo[t]
        lin.append(f'entity "{t}" as e_{t}' + (" <<propuesto>>" if d["prop"] else "") + " {")
        for c in d["columnas"]:
            mk, nom = marca(c, d)
            linea = f'{nom} : {c["tipo"]}{"" if c["nulo"] else " *"} {mk}'.rstrip()
            lin.append("  {field} " + (f"<color:{AZUL}>{linea} <<propuesto>></color>" if c["prop"] else linea))
        lin.append("}")
    for t in ajenas:
        lin.append(f'entity "{t}" as e_{t} #F1F1F1 {{')
        lin.append("}")
    lin.append("")
    vistos = set()
    for t in propias + ajenas:
        for f in completo[t]["fks"]:
            otros = set(propias) | set(ajenas)
            if f["destino"] not in otros or f["destino"] == "distributor" and "distributor" not in propias:
                continue
            if t in ajenas and f["destino"] not in propias: continue
            if (t, f["col"]) in vistos: continue
            vistos.add((t, f["col"]))
            est = f' #line:{AZUL[1:]};text:{AZUL[1:]}' if f["prop"] else ""
            lin.append(f'e_{f["destino"]} {IZQ[card_padre(t, f)]}--{DER[card_hijo(t, f)]} e_{t}{est} : {f["col"]}')
    lin += ["", "legend bottom",
            "|<#F1F1F1> **tabla de otro contexto** | solo se muestra su nombre; sus columnas están en su propio contexto |"]
    if "distributor" not in propias and any(f["destino"] == "distributor" for t in propias for f in completo[t]["fks"]):
        lin.append("|<#FFFFFF> **distributor_id** | la tabla pertenece a una distribuidora (FK a distributor); la línea no se dibuja |")
    if any(c["prop"] for t in propias for c in completo[t]["columnas"]):
        lin.append("|<#FFF6D9> **propuesto** | columna planificada, todavía sin aplicar a la base |")
    lin += ["endlegend",
            "note as N"] + ["  " + l for l in textwrap.wrap(CONVENCIONES, 110)] + ["end note", "@enduml"]
    nombre = f"SPLG-fisico-{k:02d}-{slug(ctx)}"
    open(FIS + nombre + ".puml", "w", encoding="utf-8").write("\n".join(lin))
    fisicos.append(nombre)

# ------------------------------------------------------- 6. modelo conceptual
# El DER conceptual usa el mismo vocabulario que el modelo conceptual (Doc 2, §1): una
# entidad por concepto que tiene tabla, con los atributos del concepto y las
# relaciones con el nombre y el sentido de lectura de la asociación. Cada atributo
# listado corresponde a una columna real; si no, el script corta.
def atributos_de(concepto):
    atrs = list(MC.CLASES[concepto][1])
    # las especializaciones de PropuestaConVigencia heredan `estado` y `vence`
    if any(concepto in h for p, h, _ in MC.GENERALIZACIONES if p == "PropuestaConVigencia"):
        atrs = [a for a in MC.CLASES["PropuestaConVigencia"][1] if a not in atrs] + atrs
    return atrs

def _columnas_de(tabla):
    """Columnas de una tabla: las de la base y las que agrega lo propuesto."""
    r = {c["nombre"] for c in columnas[tabla]} | {c["nombre"] for c in cols_prop.get(tabla, [])}
    for _tb in tablas_prop:
        if _tb["nombre"] == tabla:
            r |= {c["nombre"] for c in _tb["columnas"]}
    return r

_mal = []
for _c in MC.CLASES:
    _t = MC.TABLA[_c]
    if not _t: continue
    for _a in atributos_de(_c):
        _col = MC.ATRIBUTOS.get(_c, {}).get(_a) or MC.HEREDA_ATRIBUTOS.get(_a)
        if not _col or _col not in _columnas_de(_t):
            _mal.append(f"{_c}.{_a} -> {_t}.{_col}")
if _mal:
    sys.exit("El modelo conceptual tiene atributos sin columna en la base:\n  - " + "\n  - ".join(_mal))
_sin_concepto = sorted(set(completo) - set(MC.CONCEPTO_DE_TABLA) - set(MC.TABLAS_TECNICAS))
if _sin_concepto:
    sys.exit(f"Tablas sin concepto en modelo_conceptual.TABLA: {_sin_concepto}")

def nombre_concepto(t):
    return MC.CONCEPTO_DE_TABLA[t]

# relaciones del DER conceptual: (entidad izquierda, tarjeta izq., tarjeta der., entidad derecha, nombre)
def relaciones_conceptuales():
    sal, vistos = [], set()
    for t in _orden_global:
        for f in completo[t]["fks"]:
            a = MC.asociacion_de_fk(t, f["col"], f["destino"])
            if a is None: continue
            ct, cd = MC.CONCEPTO_DE_TABLA[t], MC.CONCEPTO_DE_TABLA[f["destino"]]
            hijo, padre = card_hijo(t, f), card_padre(t, f)
            if a[0] == "ESPECIALIZACION":
                izq, der, nom = ct, cd, "es un"
                ci, cdr = hijo, padre
                mi, md_ = izq, der
            elif t == "vehicle_assignment":
                # en el DER la clase de asociación es una entidad más
                izq, der, nom, ci, cdr, mi, md_ = cd, ct, "figura en", padre, hijo, cd, ct
            else:
                # El DER conceptual habla el idioma del modelo conceptual: los extremos son
                # los conceptos de la asociación (Cliente, Chofer; no la tabla `user` a la
                # que apunta la clave) y las cardinalidades son sus multiplicidades. Con las
                # de la base no se podía decir 1..*: una clave foránea no exige hijos.
                nom = a[5]
                izq, der, ci, cdr = a[0], a[4], a[1], a[3]
                mi, md_ = a[0], a[4]
            clave = (izq, der, nom)
            if clave in vistos: continue
            vistos.add(clave)
            sal.append((izq, ci, cdr, der, nom, mi, md_))
    # asociaciones con dueño polimórfico: no tienen clave foránea, pero el modelo las nombra
    for a, ma, t_, mb, b, n, _cat in MC.ASOCIACIONES:
        if (a, b, n) in MC.POLIMORFICAS:
            sal.append((a, ma, mb, b, n, a, b))
    return sal

REL_CONCEPTUALES = relaciones_conceptuales()

def entidad_conceptual(c, con_atributos):
    est = " <<propuesto>>" if c in MC.PLANIFICADOS else ""
    if not con_atributos:
        return [f'entity {c}{est}']
    marca = f" #FFF6D9;line:{AZUL[1:]}" if c in MC.PLANIFICADOS else ""
    return [f'entity {c}{est}{marca} {{', "  * identificador", "  --"] + ["  {field} " + a for a in atributos_de(c)] + ["}"]

def der_conceptual(titulo, foco, ref, general=False):
    foco = [c for c in foco if MC.TABLA.get(c)]
    ref = [c for c in ref if MC.TABLA.get(c) and c not in foco]
    if not general:
        # el otro extremo de una relación del área, aunque sea de otra vista, va como
        # referencia: si no, la relación no se dibujaba (pasaba con Cliente y Chofer)
        for izq, _ci, _cd, der, _n, _mi, _md in REL_CONCEPTUALES:
            for x, y in ((izq, der), (der, izq)):
                if x in foco and y not in foco and y not in ref and MC.TABLA.get(y):
                    ref.append(y)
    if ref and not general:
        # una entidad de referencia sin ninguna relación en la vista no aporta nada: se quita
        con_relacion = {x for izq, _ci, _cd, der, _n, _mi, _md in REL_CONCEPTUALES
                        for x in (izq, der) if izq in foco or der in foco}
        ref = [c for c in ref if c in con_relacion]
    lin = ["@startuml", f"title {titulo}", CAB, "hide circle", "skinparam nodesep 25",
           "skinparam ranksep 45", ""]
    for c in foco:
        lin += entidad_conceptual(c, not general)
    for c in ref:
        lin += [f'entity {c} #F1F1F1 {{', "}"]
    lin.append("")
    ents = set(foco) | set(ref)
    vistas_g = set()
    for izq, ci, cdr, der, nom, mi, md_ in REL_CONCEPTUALES:
        if general:
            # en la vista general cada relación con Usuario se dibuja con el perfil que la
            # origina (Cliente, Chofer); las que son del Usuario mismo van en su vista
            if izq == "Usuario" and mi != "Usuario": izq = mi
            if der == "Usuario" and md_ != "Usuario": der = md_
            if (izq == "Usuario" and nom != "es un" and der != "Rol" and der != "AsientoAuditoria") \
                    or (der == "Usuario" and nom != "es un" and izq != "Rol"):
                continue
            if (izq, der, nom) in vistas_g: continue
            vistas_g.add((izq, der, nom))
        if izq in ents and der in ents and (izq in foco or der in foco):
            # una multiplicidad acotada (0..2) no tiene símbolo propio en pata de
            # gallo: se dibuja como "muchos" y el número exacto va en el nombre
            exactas = [m for m in (ci, cdr) if m not in IZQ]
            ci_, cdr_ = (_aprox(ci), _aprox(cdr))
            txt = f" : {nom}{' [' + ' / '.join(exactas) + ']' if exactas else ''} >"
            lin.append(f'{izq} {IZQ[ci_]}--{DER[cdr_]} {der}{txt}')
    if general:
        lin += ["", "legend bottom right",
                "  Vista de conjunto: sin atributos (están en la vista de cada área). Las relaciones de Usuario",
                "  con los registros que solo dejan constancia de su autoría figuran en la vista de su área.",
                "endlegend"]
    if not general:
        leyenda = ["  * identificador: atributo que identifica a cada instancia.  /atributo: atributo derivado."]
        if ref:
            leyenda.append("  Las entidades en gris pertenecen a otra vista; se muestran solo como referencia.")
        lin += ["", "legend bottom right"] + leyenda + ["endlegend"]
    lin.append("@enduml")
    return "\n".join(lin)

CON = SAL + "conceptual/"
os.makedirs(CON, exist_ok=True)
for _viejo in glob.glob(CON + "SPLG-der-*"): os.remove(_viejo)
for _viejo in glob.glob(SAL + "SPLG-modelo-entidad-relacion.*"): os.remove(_viejo)
conceptuales = []
_pre = ""
_todo = [c for c in MC.CLASES]
_g = der_conceptual("Modelo entidad-relación conceptual — vista general", _todo, [], general=True)
nombre = "SPLG-der-00-general"
open(CON + nombre + ".puml", "w", encoding="utf-8").write(_g.replace("hide circle", "hide circle\n" + _pre, 1))
conceptuales.append(nombre)
for k, (ttl, _arch, foco, ref) in enumerate(MC.VISTAS, 1):
    nombre = f"SPLG-der-{k:02d}-{slug(ttl)}"
    txt = der_conceptual(f"Modelo entidad-relación conceptual — {ttl}", foco, ref)
    open(CON + nombre + ".puml", "w", encoding="utf-8").write(txt.replace("hide circle", "hide circle\n" + _pre, 1))
    conceptuales.append(nombre)

# --------------------------------------------------- 7. diccionario de datos
md = ["# Modelo de Datos — SPLG", "",
      f"{len(tablas)} tablas y {len(fks)} claves foráneas, leídas de la base en ejecución.", "",
      "| Sección | Qué contiene |", "|---|---|",
      "| [Diccionario de datos](#diccionario-de-datos) | Las tablas tal cual están hoy en la base, "
      "con tipo, obligatoriedad, clave, referencia, default, descripción, `CHECK` e índices |",
      "| [Relaciones no declaradas](#relaciones-no-declaradas) | Columnas que apuntan a otra tabla "
      "sin clave foránea |",
      "| [Modelo propuesto](#modelo-propuesto) | Lo que falta agregar, por pedido de la cátedra |",
      "| [Tipos enumerados](#tipos-enumerados) | Los valores admitidos por cada enumerado |", "",
      "## Diccionario de datos", ""]
_sin_doc = []
for t in tablas:
    nom = MC.CONCEPTO_DE_TABLA.get(t) or MC.TABLAS_TECNICAS.get(t, (None,))[0] or CONCEPTO.get(t, (t, []))[0]
    md += [f"### `{t}` — {nom}", "",
           "| Columna | Tipo | Obligatoria | Clave | Referencia | Default | Descripción |",
           "|---|---|:-:|:-:|---|---|---|"]
    for c in columnas[t]:
        ref = next((f'`{f["destino"]}.{f["destcol"]}`' for f in fks
                    if f["tabla"] == t and f["col"] == c["nombre"]), "")
        if not ref:
            ref = next((f'`{s["destino"]}.{s["destcol"]}` (sin FK)' for s in sin_fk
                        if s["tabla"] == t and s["col"] == c["nombre"]), "")
        clave = ("PK" if c["nombre"] in pk[t]
                 else "FK" if any(f["tabla"] == t and f["col"] == c["nombre"] for f in fks)
                 else "U" if c["nombre"] in unicos_simples.get(t, set()) else "")
        dflt = c["default"].strip() or ""
        desc = descripciones.get(t, {}).get(c["nombre"], "")
        if not desc:
            _sin_doc.append(f"{t}.{c['nombre']}")
            desc = "_(sin descripción documentada en el código)_"
        md.append(f'| `{c["nombre"]}` | {tipo_sql(c)} | {"sí" if not c["nulo"] else "no"} '
                  f'| {clave} | {ref} | {("`" + dflt + "`") if dflt else ""} | {desc} |')
    compuestos = [g for g in unicos.get(t, []) if len(g) > 1]
    if compuestos:
        md += ["", "Claves únicas compuestas: "
               + ", ".join("(" + ", ".join(f"`{c}`" for c in g) + ")" for g in compuestos) + "."]
    if checks.get(t):
        md += ["", "Restricciones `CHECK`:"]
        for nom_c, defi in checks[t]:
            md.append(f'- `{nom_c}`: `{defi}`')
    if indices.get(t):
        md += ["", "Índices (además de la clave primaria):"]
        for nom_i, defi in indices[t]:
            md.append(f'- `{nom_i}`: `{defi}`')
    md.append("")

md += ["> **Cobertura de las descripciones.** "
       f"{sum(len(v) for v in columnas.values()) - len(_sin_doc)} de "
       f"{sum(len(v) for v in columnas.values())} columnas tienen descripción tomada del "
       "comentario de la entidad de TypeORM que las define; las que no la tienen en el "
       "código figuran arriba como «sin descripción documentada en el código» en lugar de "
       "inventarse una.", ""]

if sin_fk:
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
else:
    md += ["## Relaciones no declaradas", "",
           "No hay ninguna: las 13 relaciones que en algún momento existieron sin `FOREIGN "
           "KEY` se declararon el 25/09/2026 (migración `DeclararRelacionesSinClaveForanea`). "
           f"Hoy las {len(fks)} relaciones del dominio están todas declaradas.", ""]

if not PROPUESTO:
    md += ["## Modelo propuesto", "",
           "No hay ningún agregado pendiente: los agregados que pidió la cátedra el 24/09/2026 "
           "ya están todos implementados (ver «Implementado el 25/09/2026» en "
           "`generar-modelo-datos.py`, constante `PROPUESTO_IMPLEMENTADO`), así que esta "
           "sección queda vacía en vez de mostrar un «0 agregados» que no dice nada.", ""]
for i, ag in enumerate(PROPUESTO, 1):
    md += [f"### {i}. {ag['titulo']}", "", f"**Casos de uso:** {ag['casos']}. **Qué resuelve:** {ag['pedido']}", "",
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
    if ag.get("enum_valores"):
        md.append("")
        for n, v in ag["enum_valores"].items():
            md.append(f'Valores nuevos del tipo enumerado `{n}`: {", ".join("`"+x+"`" for x in v)}.')
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
TABLA_CORR = "\n".join(f"| {c} | {c if t else '—'} | {('`'+t+'`') if t else '—'} |"
                       for c, t in MC.TABLA.items())
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
| `SPLG-base-de-datos-portable.sql` | Solo lo implementado, en SQL portable | Diagramar el estado actual |
| `SPLG-base-de-datos-propuesta.sql` | Solo lo planificado (los módulos de gestión) | Boceto de las migraciones que faltan |
| `SPLG-base-de-datos-completa-portable.sql` | Actual + planificado, en SQL portable | Ver todo el modelo en un solo SQL |
| `fisico/SPLG-fisico-NN-<contexto>.png` / `.svg` | Entidad-relación con tablas y columnas, una lámina por contexto de negocio | Las láminas técnicas |
| `conceptual/SPLG-der-NN-<área>.png` / `.svg` | Entidad-relación conceptual: una entidad por concepto del modelo conceptual, con sus atributos y las relaciones con su nombre | Las láminas para la defensa |
| `SPLG-der-mermaid.md` | El físico en Mermaid, por contexto | Lo que se pega en el Documento 3 §7.4.2 |
| `SPLG-modelo-de-datos.md` | Diccionario de datos y sustento escrito | El texto del informe |

En las láminas físicas, lo que ya está implementado va en blanco con borde oscuro y lo
propuesto —columnas planificadas que todavía no están en la base— en celeste, con el
marcador `<<propuesto>>`. Una tabla en gris es de otro contexto y solo se muestra su nombre.
Los nombres reflejan la base real: conviven camelCase (`paymentMethod`) y snake_case
(`scheduled_date`), y la tabla `claims` está en plural; unificarlos exigiría renombrar
columnas en una base en uso.

Las láminas conceptuales usan el vocabulario del modelo conceptual (Documento 2, §1) y no el
de las tablas: la entidad se llama como el concepto y lleva sus atributos. La relación con
`distributor` de cada tabla no se dibuja; sí las que el modelo conceptual nombra.

## Correspondencia entre el modelo conceptual y el modelo de datos

| Concepto | Entidad | Tabla |
|---|---|---|
{TABLA_CORR}

Los conceptos sin tabla son PropuestaConVigencia (abstracto), UbicacionGPS (la columna
`delivery.actual_location`) e ItemSugerido (JSON dentro de `repurchase_invitation`).
`material-de-trabajo/verificar-mc-der.py` comprueba esta correspondencia contra la base.

`SPLG-base-de-datos-propuesta.sql` es PostgreSQL válido: agrega tipos, columnas
y tablas sobre el esquema que ya está, sin tocar los datos existentes.

## Diagramas en draw.io

Los cuatro modelos (conceptual, DER, base de datos físico y clases de diseño) están en `drawio/`, generados por
`generar-drawio.py` a partir de `SPLG-modelo.json`, que escribe este script leyendo la base. Ver `drawio/LEEME.md`.

## Qué pegarle a Gemini

Para que revise el modelo, el archivo que conviene pasarle es
**`SPLG-modelo-de-datos.md`**: es el único que trae, en un solo texto, el
diccionario de datos, las relaciones que faltan declarar y los agregados
pedidos, cada uno con el motivo por el que está.

Si además se quiere que revise el DDL, sumar
**`SPLG-base-de-datos-completa-portable.sql`**, que es el modelo entero en
menos de {os.path.getsize(SAL + 'SPLG-base-de-datos-completa-portable.sql') // 1024 + 1} KB.
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

# --------------------------------------------- 9. DER en Mermaid, por contexto
# El Doc 3 (`3-Diseño.md` §7.4) embebe Mermaid, no PlantUML: este bloque arma
# el mismo contenido que el `.puml` físico, pero en `erDiagram`, partido por
# contexto de negocio para que cada lámina se pueda leer, con una lámina final
# de relaciones entre contextos. Se pega a mano en el Doc 3 (los `.md` son la
# fuente); lo que hay que evitar es tipearlo de nuevo si cambia la base.
def tipo_mermaid(tipo):
    """Mermaid erDiagram no acepta paréntesis ni comas en el tipo."""
    t = re.sub(r'\(.*\)', '', tipo)
    if t in enums: return "enum"
    return {"varchar": "varchar", "text": "text", "geometry": "geometry",
            "geography": "geography", "numeric": "decimal", "timestamptz": "timestamptz",
            "timestamp": "timestamp", "uuid": "uuid", "boolean": "boolean", "integer": "int",
            "jsonb": "jsonb", "date": "date", "double precision": "float"}.get(t, t)

def entidad_mermaid(t, modelo=None):
    d = (modelo or actual)[t]
    ln = [f"    {t.upper()} {{"]
    for c in d["columnas"]:
        marcas = []
        if c["nombre"] in d["pk"]: marcas.append("PK")
        elif any(f["col"] == c["nombre"] for f in d["fks"]): marcas.append("FK")
        if c["nombre"] in unicos_simples.get(t, set()) and c["nombre"] not in d["pk"]:
            marcas.append("UK")
        notas = [] if c["nulo"] is False else ["nullable"]
        marca_txt = ", ".join(marcas)
        com = ('"' + "; ".join(notas) + '"') if notas else ""
        ln.append(f'        {tipo_mermaid(c["tipo"])} {c["nombre"]}'
                  + (f" {marca_txt}" if marca_txt else "") + (f" {com}" if com else ""))
    ln.append("    }")
    return "\n".join(ln)

def relacion_mermaid(f, t, modelo=None):
    modelo = modelo or actual
    simples = unicos_simples.get(t, set()) | {g[0] for g in modelo[t]["unicos"] if len(g) == 1}
    hijo = "|o" if f["col"] in simples else "}o"
    col = next((c for c in modelo[t]["columnas"] if c["nombre"] == f["col"]), None)
    padre = "o|" if (col and col["nulo"]) else "||"
    return f'    {t.upper()} {hijo}--{padre} {f["destino"].upper()} : "{f["col"]}"'

_tabla_a_ctx = {t: ctx for ctx, ts in CONTEXTOS for t in ts}
der = ["# DER de SPLG, en Mermaid — generado", "",
       f"Generado por `generar-modelo-datos.py` desde la base en ejecución: "
       f"{len(tablas)} tablas, {len(fks)} relaciones. Se pega tal cual en "
       "`3-Diseño.md` §7.4.2 (los `.md` son la fuente; esto se corre de nuevo y se vuelve "
       "a pegar si la base cambia). Cada lámina es un `erDiagram` válido por separado "
       "(uno por contexto de negocio) más una lámina final con las relaciones que cruzan "
       "de un contexto a otro.", ""]
_vistas_globales = set()
for ctx, ts in CONTEXTOS:
    # un contexto sin ninguna tabla en la base (módulo planificado) se dibuja desde el modelo completo
    planificado = any(x not in actual for x in ts)
    modelo = completo if planificado else actual
    # Personal está a medias: legajos y puestos construidos, jornadas y licencias no
    marca_ctx = "" if not planificado else (" (planificado)" if not any(x in actual for x in ts)
                                            else " (en parte planificado)")
    der += [f"### {ctx}" + marca_ctx, "", "```mermaid", "erDiagram"]
    for t in [x for x in orden_dependencias(modelo) if x in ts]:
        for f in modelo[t]["fks"]:
            if _tabla_a_ctx.get(f["destino"]) == ctx:
                der.append(relacion_mermaid(f, t, modelo))
                _vistas_globales.add((t, f["col"]))
    der.append("")
    for t in [x for x in orden_dependencias(modelo) if x in ts]:
        der.append(entidad_mermaid(t, modelo))
    der += ["```", ""]

der += ["### Relaciones entre contextos", "",
        "Las que cruzan de un contexto a otro (ya sin repetir la entidad completa; "
        "sus columnas están en la lámina de su propio contexto). La relación con "
        "`distributor` se omite acá también por lo mismo que en el conceptual: "
        "prácticamente todo pertenece a una distribuidora.", "",
        "```mermaid", "erDiagram"]
for t in orden_dependencias(completo):
    for f in completo[t]["fks"]:
        if (t, f["col"]) in _vistas_globales: continue
        if f["destino"] == "distributor": continue
        der.append(relacion_mermaid(f, t, completo))
der += ["```", ""]
open(SAL + "SPLG-der-mermaid.md", "w", encoding="utf-8").write("\n".join(der))
print(f"  ✓ SPLG-der-mermaid.md  ({len(CONTEXTOS)} láminas por contexto + 1 de cruces)")

# ------------------------------------------------- fuente de los diagramas de draw.io
# generar-drawio.py no vuelve a leer la base: toma de acá el modelo físico (las tablas reales, con
# columnas, claves e índices) y el DER conceptual (conceptos, atributos y relaciones con su
# cardinalidad), el mismo que dibujan las láminas de PlantUML.
import json as _json
_modelo = {"dbd": {"contextos": [[c, [t for t in ts if t in actual]] for c, ts in CONTEXTOS
                                   if any(t in actual for t in ts)],
                   "tablas": {}},
           "der": {"entidades": {}, "relaciones": [], "vistas": []}}
for _t in tablas:
    _d = actual[_t]
    _cols = []
    for _c in _d["columnas"]:
        _f = next((f for f in _d["fks"] if f["col"] == _c["nombre"]), None)
        _cols.append({"nombre": _c["nombre"], "tipo": _c["tipo"], "nulo": _c["nulo"],
                      "pk": _c["nombre"] in _d["pk"],
                      "unico": any(g == [_c["nombre"]] for g in _d["unicos"]),
                      "fk": ({"destino": _f["destino"], "destcol": _f["destcol"], "borrado": _f["borrado"],
                              "card_padre": card_padre(_t, _f), "card_hijo": card_hijo(_t, _f)} if _f else None)})
    _modelo["dbd"]["tablas"][_t] = {
        "columnas": _cols, "pk": _d["pk"], "unicos": _d["unicos"],
        "indices": [[n, dfn] for n, dfn in indices.get(_t, [])]}
for _c in MC.CLASES:
    if MC.TABLA.get(_c):
        _modelo["der"]["entidades"][_c] = {"atributos": atributos_de(_c), "planificado": _c in MC.PLANIFICADOS,
                                           "contexto": MC.CLASES[_c][0]}
_modelo["der"]["relaciones"] = [{"izq": a, "card_izq": ci, "card_der": cd, "der": b, "nombre": n,
                                 "extremo_izq": mi, "extremo_der": md_}
                                for a, ci, cd, b, n, mi, md_ in REL_CONCEPTUALES]
_modelo["der"]["vistas"] = [[ttl, foco] for ttl, _arch, foco, _ref in MC.VISTAS]
open(SAL + "SPLG-modelo.json", "w", encoding="utf-8").write(_json.dumps(_modelo, ensure_ascii=False, indent=1))
print(f"  ✓ SPLG-modelo.json  ({len(_modelo['dbd']['tablas'])} tablas, {len(_modelo['der']['relaciones'])} relaciones conceptuales)")

# ------------------------------------------------------------------ render
entorno = dict(os.environ, PLANTUML_LIMIT_SIZE="32768")
for carpeta, nombres in ((FIS, fisicos), (CON, conceptuales)):
    for n in nombres:
        for fmt in ("png", "svg"):
            r = subprocess.run(["plantuml", "-t"+fmt, "-charset", "UTF-8", carpeta+n+".puml"],
                               capture_output=True, text=True, env=entorno)
            if r.returncode or "Error" in (r.stdout + r.stderr):
                print("  ✗", n, fmt, (r.stderr or r.stdout).strip()[:200])
        if os.path.exists(carpeta+n+".png"):
            print(f"  ✓ {n} ({os.path.getsize(carpeta+n+'.png')//1024} KB)")

for a in avisos: print("  ·", a)
print(f"implementado · tablas: {len(tablas)} · columnas: {sum(len(v) for v in columnas.values())} · "
      f"claves foráneas: {len(fks)} · sin declarar: {len(sin_fk)} · enumerados: {len(enums)}")
print(f"propuesto    · tablas: {len(tablas_prop)} · columnas: {sum(len(v) for v in cols_prop.values())} · "
      f"claves foráneas: {sum(1 for d in completo.values() for f in d['fks'] if f['prop'])} · "
      f"enumerados: {len(enums_prop)}")
print(f"completo     · tablas: {len(completo)} · relaciones: {n_fk_completo}")
