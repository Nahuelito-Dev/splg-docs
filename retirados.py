# -*- coding: utf-8 -*-
"""Casos de uso retirados del catálogo: la única fuente de la tabla de retirados y del verificador.

Un caso retirado no es un proceso de negocio elemental (Larman): la documentación conserva su número reservado y
dice a dónde pasó lo que describía. Sus códigos no se reutilizan."""
RETIRADOS = [
    ("CU-003", "Registrar un Chofer (Gestión de Usuarios)", "15/10/2026",
     "Duplicaba CU-031: era la misma operación vista desde el subsistema de usuarios.", "CU-031 Registrar un Chofer (Gestión de la Flota)"),
    ("CU-021", "Recibir Notificaciones en Tiempo Real", "14/10/2026",
     "Es un requisito del sistema: el cliente recibe sin consultar cada cambio de su pedido y la posición del chofer.", "Documento 1, NFR-02 (Rendimiento)"),
    ("CU-084", "Verificar la Existencia de un Usuario (pre-registro)", "15/10/2026",
     "Es una validación del formulario de registro, no un proceso con valor propio para el actor.", "CU-002 Registrarse como Cliente"),
    ("CU-090", "Sembrar los Roles Iniciales", "15/10/2026",
     "Es una preparación del entorno al desplegar el sistema, no un objetivo de un usuario.", "Documento 3, despliegue (arranque del sistema)"),
    ("CU-091", "Validar Vigencia del Token de Sesión", "14/10/2026",
     "Es un mecanismo de autenticación que se ejecuta en cada solicitud, no un caso de uso.", "Documento 1, NFR-01 (Seguridad)"),
    ("CU-093", "Validar o Invalidar Cliente", "26/09/2026",
     "Los clientes se registran y compran sin aprobación previa: la marca no condicionaba ningún pedido y solo sumaba trabajo al administrador.", "Sin reemplazo (los choferes siguen validándose en CU-032)"),
    ("CU-098", "Registrar el Token de Notificaciones del Dispositivo", "15/10/2026",
     "Es un mecanismo del canal de avisos: la aplicación lo hace sola al iniciar sesión, sin que el usuario lo pida.", "Documento 1, NFR-02 (Rendimiento) y Documento 3, diseño de notificaciones"),
    ("CU-099", "Consultar los Tokens de un Usuario", "15/10/2026",
     "Es una herramienta de diagnóstico técnico del canal de avisos, no un proceso de negocio.", "CU-100 Enviar una Notificación de Prueba y Documento 3"),
    ("CU-103", "Dar de Baja una Franja Horaria", "16/10/2026",
     "Duplicaba CU-343: ambos desactivan la franja (baja lógica), uno con el verbo «dar de baja» y el otro con «desactivar».", "CU-343 Desactivar una Franja Horaria"),
    ("CU-153", "Registrar Toda Operación de Escritura", "15/10/2026",
     "Es un requisito transversal: el sistema deja constancia de cada escritura sin que ningún actor lo pida.", "Documento 1, NFR-10 (Trazabilidad y auditoría); la consulta sigue en CU-152"),
]
CODIGOS = [r[0] for r in RETIRADOS]
