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
    """

    VENTA = auto()
    ALQUILER = auto()
    REFORMA = auto()
    DECORACION = auto()


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
