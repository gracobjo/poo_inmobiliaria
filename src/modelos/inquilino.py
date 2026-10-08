"""Modelo de inquilino del Sistema Inmobiliario POO."""

from __future__ import annotations

import re

from src.utils.validadores import ValidadoresInmobiliarios


class Inquilino:
    """Representa a un potencial o actual inquilino.

    El DNI se mantiene encapsulado (atributo privado) y solo se expone
    mediante una property de solo lectura. La capacidad de alquilar se
    evalúa con la regla del 35 %: la renta mensual no puede superar
    ese porcentaje de los ingresos mensuales netos.

    Attributes:
        nombre: Nombre completo del inquilino.
        telefono: Teléfono de contacto.
        ingresos: Ingresos mensuales netos en euros.
    """

    _PATRON_DNI: re.Pattern[str] = re.compile(r"^\d{8}[A-Z]$")
    _RATIO_MAXIMO_RENTA: float = 0.35

    def __init__(
        self,
        nombre: str,
        dni: str,
        telefono: str,
        ingresos: float,
    ) -> None:
        """Inicializa un inquilino validando sus datos.

        Args:
            nombre: Nombre completo (no vacío).
            dni: Documento nacional de identidad (8 dígitos + letra).
            telefono: Teléfono de contacto (no vacío).
            ingresos: Ingresos mensuales netos (> 0).

        Raises:
            ValueError: Si algún dato no supera la validación.
        """
        if not ValidadoresInmobiliarios.es_string_no_vacio(nombre):
            raise ValueError("El nombre del inquilino no puede estar vacío.")
        if not ValidadoresInmobiliarios.es_string_no_vacio(telefono):
            raise ValueError("El teléfono del inquilino no puede estar vacío.")
        if not ValidadoresInmobiliarios.es_positivo(ingresos):
            raise ValueError("Los ingresos deben ser un número positivo.")

        dni_normalizado: str = dni.strip().upper() if isinstance(dni, str) else ""
        if self._PATRON_DNI.fullmatch(dni_normalizado) is None:
            raise ValueError("El DNI debe tener formato 8 dígitos + letra (ej. 12345678Z).")

        self.nombre: str = nombre.strip()
        self._dni: str = dni_normalizado
        self.telefono: str = telefono.strip()
        self._ingresos: float = float(ingresos)

    @property
    def dni(self) -> str:
        """DNI del inquilino (solo lectura)."""
        return self._dni

    @property
    def ingresos(self) -> float:
        """Ingresos mensuales netos en euros."""
        return self._ingresos

    @ingresos.setter
    def ingresos(self, valor: float) -> None:
        """Actualiza los ingresos mensuales.

        Args:
            valor: Nuevo importe (> 0).

        Raises:
            ValueError: Si el valor no es positivo.
        """
        if not ValidadoresInmobiliarios.es_positivo(valor):
            raise ValueError("Los ingresos deben ser un número positivo.")
        self._ingresos = float(valor)

    def puede_alquilar(self, renta_mensual: float) -> bool:
        """Evalúa si el inquilino puede asumir una renta (regla del 35 %).

        Args:
            renta_mensual: Renta mensual solicitada en euros.

        Returns:
            ``True`` si ``renta_mensual <= ingresos * 0.35``.

        Raises:
            ValueError: Si ``renta_mensual`` no es un número positivo.
        """
        if not ValidadoresInmobiliarios.es_positivo(renta_mensual):
            raise ValueError("La renta mensual debe ser un número positivo.")
        return float(renta_mensual) <= self._ingresos * self._RATIO_MAXIMO_RENTA

    def __repr__(self) -> str:
        return (
            f"Inquilino(nombre={self.nombre!r}, dni={self._dni!r}, "
            f"telefono={self.telefono!r}, ingresos={self._ingresos!r})"
        )

    def __str__(self) -> str:
        return f"{self.nombre} ({self._dni})"
