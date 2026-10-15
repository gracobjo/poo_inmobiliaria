"""Constantes enumeradas del Sistema Inmobiliario POO.

Define los estados posibles de una vivienda y los tipos de operación
comercial o de servicio que gestiona la inmobiliaria.
"""

from enum import Enum, auto


class EstadoCasa(Enum):
    """Estado comercial o físico de una vivienda en el inventario.

    Attributes:
        DISPONIBLE: Libre para venta o alquiler.
        RESERVADA: Bloqueada temporalmente para un cliente.
        VENDIDA: Transacción de venta cerrada.
        ALQUILADA: Cedida en régimen de alquiler vigente.
        EN_REFORMA: Fuera de comercialización por obras.
    """

    DISPONIBLE = auto()
    RESERVADA = auto()
    VENDIDA = auto()
    ALQUILADA = auto()
    EN_REFORMA = auto()


class TipoOperacion(Enum):
    """Tipo de operación o servicio inmobiliario.

    Attributes:
        VENTA: Transmisión de propiedad.
        ALQUILER: Cesión temporal de uso.
        REFORMA: Obra de mejora o rehabilitación.
        DECORACION: Servicio de interiorismo o ambientación.
        RESERVA: Bloqueo temporal a favor de un cliente.
        RESOLUCION: Baja formal de un contrato de arrendamiento.
    """

    VENTA = auto()
    ALQUILER = auto()
    REFORMA = auto()
    DECORACION = auto()
    RESERVA = auto()
    RESOLUCION = auto()


class IniciativaResolucion(Enum):
    """Quién solicita la resolución del contrato de arrendamiento."""

    ARRENDADOR = "ARRENDADOR"
    ARRENDATARIO = "ARRENDATARIO"
    AJENA = "AJENA"

    @property
    def etiqueta(self) -> str:
        return {
            IniciativaResolucion.ARRENDADOR: "Arrendador (gestor / propietario)",
            IniciativaResolucion.ARRENDATARIO: "Arrendatario (inquilino)",
            IniciativaResolucion.AJENA: "Causa ajena / mutuo acuerdo",
        }[self]


class CausaResolucion(Enum):
    """Causas de resolución del arrendamiento (inspiradas en la LAU).

    Cada valor guarda ``(iniciativa, descripción legible)``.
    """

    # Arrendador
    FALTA_PAGO_RENTA = (
        IniciativaResolucion.ARRENDADOR,
        "Falta de pago de la renta o cantidades debidas (comunidad, suministros…)",
    )
    FALTA_PAGO_FIANZA = (
        IniciativaResolucion.ARRENDADOR,
        "Falta de pago de la fianza o de su actualización obligatoria",
    )
    SUBARRIENDO_SIN_CONSENTIMIENTO = (
        IniciativaResolucion.ARRENDADOR,
        "Subarriendo o cesión sin consentimiento escrito del propietario",
    )
    DANOS_DOLOSOS = (
        IniciativaResolucion.ARRENDADOR,
        "Daños dolosos causados intencionadamente en la finca",
    )
    OBRAS_NO_CONSENTIDAS = (
        IniciativaResolucion.ARRENDADOR,
        "Obras no consentidas que alteren la vivienda o requieran permiso",
    )
    ACTIVIDADES_MOLESTAS = (
        IniciativaResolucion.ARRENDADOR,
        "Actividades molestas, insalubres, nocivas, peligrosas o ilícitas",
    )
    CAMBIO_DESTINO = (
        IniciativaResolucion.ARRENDADOR,
        "Cambio de destino: la vivienda deja de usarse como residencia permanente",
    )
    NECESIDAD_PROPIETARIO = (
        IniciativaResolucion.ARRENDADOR,
        "Necesidad de la vivienda para el propietario o familiares (1.er grado)",
    )
    # Arrendatario
    FALTA_REPARACIONES = (
        IniciativaResolucion.ARRENDATARIO,
        "No realización de reparaciones necesarias de habitabilidad",
    )
    PERTURBACION_USO = (
        IniciativaResolucion.ARRENDATARIO,
        "Perturbación del uso pacífico de la vivienda por el propietario",
    )
    DESISTIMIENTO_INQUILINO = (
        IniciativaResolucion.ARRENDATARIO,
        "Desistimiento del inquilino (art. 11 LAU, tras 6 meses de contrato)",
    )
    # Ajenas / mutuo
    PERDIDA_FINCA = (
        IniciativaResolucion.AJENA,
        "Pérdida de la finca arrendada por causa no imputable al propietario",
    )
    DECLARACION_RUINA = (
        IniciativaResolucion.AJENA,
        "Declaración firme de ruina de la vivienda",
    )
    MUTUO_ACUERDO = (
        IniciativaResolucion.AJENA,
        "Mutuo acuerdo entre propietario e inquilino",
    )

    @property
    def iniciativa(self) -> IniciativaResolucion:
        return self.value[0]

    @property
    def descripcion(self) -> str:
        return self.value[1]

    @classmethod
    def para_iniciativa(cls, iniciativa: IniciativaResolucion) -> list[CausaResolucion]:
        """Causas disponibles para una iniciativa (incluye las ajenas)."""
        propias = [c for c in cls if c.iniciativa == iniciativa]
        if iniciativa != IniciativaResolucion.AJENA:
            ajenas = [c for c in cls if c.iniciativa == IniciativaResolucion.AJENA]
            return propias + ajenas
        return propias


class TipoVivienda(Enum):
    """Tipología constructiva o de uso de un inmueble.

    Attributes:
        PISO: Vivienda en bloque plurifamiliar.
        ATICO: Última planta con posibles terrazas.
        ESTUDIO: Unidad diurna sin dormitorio separado.
        DUPLEX: Distribución en dos plantas.
        LOFT: Espacio diáfano tipo industrial.
        CHALET: Vivienda unifamiliar independiente.
        ADOSADO: Unifamiliar en hilera.
        PAREADO: Unifamiliar compartiendo medianera.
        CASA_RURAL: Vivienda en entorno rural.
        BUNGALOW: Unifamiliar de una planta.
        LOCAL: Local comercial.
        OFICINA: Uso terciario de oficinas.
    """

    PISO = auto()
    ATICO = auto()
    ESTUDIO = auto()
    DUPLEX = auto()
    LOFT = auto()
    CHALET = auto()
    ADOSADO = auto()
    PAREADO = auto()
    CASA_RURAL = auto()
    BUNGALOW = auto()
    LOCAL = auto()
    OFICINA = auto()
