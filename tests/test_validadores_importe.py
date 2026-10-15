"""Tests del parseo de importes para filtros de precio."""

from __future__ import annotations

import unittest

from src.ui.app_grafica import AppGrafica
from src.utils.validadores import ValidadoresInmobiliarios


class TestParsearImporte(unittest.TestCase):
    """Comprueba formatos ES/EN y el atajo en miles del filtro de cliente."""

    def test_euros_completos(self) -> None:
        self.assertEqual(ValidadoresInmobiliarios.parsear_importe("250000"), 250_000.0)
        self.assertEqual(ValidadoresInmobiliarios.parsear_importe("250.000"), 250_000.0)
        self.assertEqual(ValidadoresInmobiliarios.parsear_importe("250,000"), 250_000.0)
        self.assertEqual(ValidadoresInmobiliarios.parsear_importe("250k"), 250_000.0)
        self.assertEqual(ValidadoresInmobiliarios.parsear_importe("250.000,50"), 250_000.5)

    def test_filtro_interpreta_miles_cortos(self) -> None:
        self.assertEqual(AppGrafica._parsear_filtro_precio("250"), 250_000.0)
        self.assertEqual(AppGrafica._parsear_filtro_precio("700"), 700_000.0)
        self.assertEqual(AppGrafica._parsear_filtro_precio("250.000"), 250_000.0)
        self.assertEqual(AppGrafica._parsear_filtro_precio("250000"), 250_000.0)
        self.assertIsNone(AppGrafica._parsear_filtro_precio("  "))


if __name__ == "__main__":
    unittest.main()
