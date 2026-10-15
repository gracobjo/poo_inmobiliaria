"""Modelo de reserva temporal de una vivienda."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from src.modelos.inquilino import Inquilino
from src.utils.validadores import ValidadoresInmobiliarios


@dataclass(frozen=True)
class Reserva:
    """Reserva de una vivienda a favor de un cliente.

    Attributes:
        cliente: Persona para la que se bloquea la vivienda.
        fecha: Momento en que se registró la reserva.
    """

    cliente: Inquilino
    fecha: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.cliente, Inquilino):
            raise TypeError("El cliente de la reserva debe ser un Inquilino.")
        if isinstance(self.fecha, date) and not isinstance(self.fecha, datetime):
            object.__setattr__(
                self,
                "fecha",
                datetime(self.fecha.year, self.fecha.month, self.fecha.day),
            )
        if not isinstance(self.fecha, datetime):
            raise TypeError("La fecha de reserva debe ser datetime.")
        if not ValidadoresInmobiliarios.es_fecha_valida(self.fecha):
            raise ValueError("La fecha de reserva no es válida.")
