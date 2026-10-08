"""Validadores reutilizables para datos del dominio inmobiliario.

Proporciona comprobaciones estáticas de números, textos, códigos postales
españoles y fechas, pensadas para usarse desde modelos y casos de uso.
"""

from __future__ import annotations

import re
from datetime import date, datetime


class ValidadoresInmobiliarios:
    """Colección de validaciones estáticas del dominio inmobiliario.

    Todos los métodos son estáticos: no mantienen estado y pueden
    invocarse directamente sobre la clase.
    """

    _PATRON_CP_ESPANA: re.Pattern[str] = re.compile(r"^(?:0[1-9]|[1-4]\d|5[0-2])\d{3}$")

    @staticmethod
    def es_positivo(valor: int | float) -> bool:
        """Indica si ``valor`` es un número estricamente mayor que cero.

        Args:
            valor: Número entero o real a evaluar.

        Returns:
            ``True`` si ``valor > 0``; ``False`` en caso contrario
            (incluye cero, negativos y tipos no numéricos).
        """
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            return False
        return valor > 0

    @staticmethod
    def es_string_no_vacio(texto: str) -> bool:
        """Indica si ``texto`` es una cadena con contenido significativo.

        Se consideran inválidos ``None``, tipos distintos de ``str`` y
        cadenas vacías o formadas solo por espacios.

        Args:
            texto: Cadena a evaluar.

        Returns:
            ``True`` si, tras ``strip()``, la cadena no está vacía.
        """
        if not isinstance(texto, str):
            return False
        return texto.strip() != ""

    @staticmethod
    def es_cp_valido(codigo_postal: str) -> bool:
        """Valida un código postal español (formato INE).

        Acepta exactamente 5 dígitos correspondientes a las provincias
        españolas (01000–52999).

        Args:
            codigo_postal: Código postal como cadena.

        Returns:
            ``True`` si el formato y el rango provincial son válidos.
        """
        if not isinstance(codigo_postal, str):
            return False
        return ValidadoresInmobiliarios._PATRON_CP_ESPANA.fullmatch(codigo_postal.strip()) is not None

    @staticmethod
    def es_fecha_valida(fecha: date | datetime | str, formato: str = "%Y-%m-%d") -> bool:
        """Indica si ``fecha`` representa una fecha calendario válida.

        Acepta instancias de :class:`datetime.date` / :class:`datetime.datetime`
        o cadenas parseables con el ``formato`` indicado (por defecto ISO).

        Args:
            fecha: Valor a validar.
            formato: Patrón ``strptime`` cuando ``fecha`` es ``str``.

        Returns:
            ``True`` si la fecha es válida; ``False`` si el tipo no es
            admitido o la cadena no se puede interpretar.
        """
        if isinstance(fecha, datetime):
            return True
        if isinstance(fecha, date):
            return True
        if isinstance(fecha, str):
            if not ValidadoresInmobiliarios.es_string_no_vacio(fecha):
                return False
            try:
                datetime.strptime(fecha.strip(), formato)
            except ValueError:
                return False
            return True
        return False
