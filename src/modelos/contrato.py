"""Modelo de contrato de alquiler del Sistema Inmobiliario POO."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from src.utils.validadores import ValidadoresInmobiliarios

if TYPE_CHECKING:
    from src.modelos.inquilino import Inquilino


class Contrato:
    """Contrato de alquiler vinculado a un inquilino.

    Gestiona el periodo de vigencia, la renta mensual y la fianza.
    El total pagado se calcula a partir de los meses transcurridos
    desde el inicio hasta una fecha de referencia (por defecto hoy),
    sin superar la fecha de fin del contrato.

    Attributes:
        inquilino: Inquilino titular del contrato.
        fecha_inicio: Fecha de comienzo del alquiler.
        fecha_fin: Fecha de finalización del alquiler.
        renta: Renta mensual en euros.
        fianza: Importe de la fianza en euros.
    """

    def __init__(
        self,
        inquilino: Inquilino,
        fecha_inicio: date,
        fecha_fin: date,
        renta: float,
        fianza: float,
    ) -> None:
        """Crea un contrato validando fechas e importes.

        Args:
            inquilino: Titular del contrato.
            fecha_inicio: Inicio del periodo de alquiler.
            fecha_fin: Fin del periodo (debe ser posterior al inicio).
            renta: Renta mensual (> 0).
            fianza: Fianza depositada (>= 0).

        Raises:
            ValueError: Si las fechas o los importes no son válidos.
            TypeError: Si ``inquilino`` no es una instancia de ``Inquilino``.
        """
        # Import diferido para evitar ciclos en tiempo de ejecución.
        from src.modelos.inquilino import Inquilino as InquilinoCls

        if not isinstance(inquilino, InquilinoCls):
            raise TypeError("El inquilino debe ser una instancia de Inquilino.")
        if not ValidadoresInmobiliarios.es_fecha_valida(fecha_inicio):
            raise ValueError("La fecha de inicio no es válida.")
        if not ValidadoresInmobiliarios.es_fecha_valida(fecha_fin):
            raise ValueError("La fecha de fin no es válida.")

        inicio: date = fecha_inicio.date() if hasattr(fecha_inicio, "date") else fecha_inicio
        fin: date = fecha_fin.date() if hasattr(fecha_fin, "date") else fecha_fin

        if fin <= inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio.")
        if not ValidadoresInmobiliarios.es_positivo(renta):
            raise ValueError("La renta debe ser un número positivo.")
        if not isinstance(fianza, (int, float)) or isinstance(fianza, bool) or fianza < 0:
            raise ValueError("La fianza debe ser un número mayor o igual que cero.")

        self._inquilino: Inquilino = inquilino
        self._fecha_inicio: date = inicio
        self._fecha_fin: date = fin
        self._renta: float = float(renta)
        self._fianza: float = float(fianza)

    @property
    def inquilino(self) -> Inquilino:
        """Inquilino titular del contrato."""
        return self._inquilino

    @property
    def fecha_inicio(self) -> date:
        """Fecha de inicio del contrato."""
        return self._fecha_inicio

    @property
    def fecha_fin(self) -> date:
        """Fecha de finalización del contrato."""
        return self._fecha_fin

    @property
    def renta(self) -> float:
        """Renta mensual en euros."""
        return self._renta

    @property
    def fianza(self) -> float:
        """Importe de la fianza en euros."""
        return self._fianza

    def calcular_total_pagado(self, hasta: date | None = None) -> float:
        """Calcula el importe abonado en rentas hasta una fecha.

        Suma la fianza más ``renta * meses_completos`` transcurridos
        entre el inicio y ``hasta`` (acotado a ``fecha_fin``).

        Args:
            hasta: Fecha de corte. Si es ``None``, se usa ``date.today()``.

        Returns:
            Total pagado en euros (fianza + rentas de meses completos).

        Raises:
            ValueError: Si ``hasta`` no es una fecha válida.
        """
        fecha_corte: date = date.today() if hasta is None else hasta
        if not ValidadoresInmobiliarios.es_fecha_valida(fecha_corte):
            raise ValueError("La fecha de corte no es válida.")

        if hasattr(fecha_corte, "date") and not isinstance(fecha_corte, date):
            fecha_corte = fecha_corte.date()

        if fecha_corte < self._fecha_inicio:
            return 0.0

        limite: date = min(fecha_corte, self._fecha_fin)
        meses: int = (limite.year - self._fecha_inicio.year) * 12 + (
            limite.month - self._fecha_inicio.month
        )
        if limite.day < self._fecha_inicio.day:
            meses -= 1
        meses = max(meses, 0)

        return self._fianza + (self._renta * meses)

    def esta_vigente(self, en_fecha: date | None = None) -> bool:
        """Indica si el contrato está vigente en una fecha.

        Args:
            en_fecha: Fecha a comprobar. Si es ``None``, se usa hoy.

        Returns:
            ``True`` si ``fecha_inicio <= en_fecha <= fecha_fin``.

        Raises:
            ValueError: Si ``en_fecha`` no es una fecha válida.
        """
        referencia: date = date.today() if en_fecha is None else en_fecha
        if not ValidadoresInmobiliarios.es_fecha_valida(referencia):
            raise ValueError("La fecha de referencia no es válida.")

        if hasattr(referencia, "date") and not isinstance(referencia, date):
            referencia = referencia.date()

        return self._fecha_inicio <= referencia <= self._fecha_fin

    def __repr__(self) -> str:
        return (
            f"Contrato(inquilino={self._inquilino!r}, "
            f"fecha_inicio={self._fecha_inicio!r}, fecha_fin={self._fecha_fin!r}, "
            f"renta={self._renta!r}, fianza={self._fianza!r})"
        )

    def __str__(self) -> str:
        estado: str = "vigente" if self.esta_vigente() else "no vigente"
        return (
            f"Contrato de {self._inquilino} "
            f"({self._fecha_inicio} → {self._fecha_fin}) — {estado}"
        )
