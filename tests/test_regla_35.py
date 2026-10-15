"""Tests de la regla del 35 % acumulada entre contratos."""

from __future__ import annotations

import unittest
from datetime import date

from src.modelos.casa import Casa
from src.modelos.inquilino import Inquilino


class TestRegla35Acumulada(unittest.TestCase):
    """La renta total de un inquilino no puede superar el 35 % de ingresos."""

    def setUp(self) -> None:
        Casa.total_casas = 0
        # Ingresos 2000 → tope 700 €/mes
        self.inquilino = Inquilino("prueba1", "12345678Z", "111111111", 2_000)

    def test_tope_renta(self) -> None:
        self.assertAlmostEqual(self.inquilino.tope_renta, 700.0)

    def test_primera_renta_dentro_del_tope(self) -> None:
        self.assertTrue(self.inquilino.puede_alquilar(600))

    def test_segunda_renta_acumulada_rechazada(self) -> None:
        # 600 ya comprometidos + 900 nuevos = 1500 > 700
        self.assertFalse(
            self.inquilino.puede_alquilar(900, renta_ya_comprometida=600)
        )

    def test_casa_rechaza_alquiler_acumulado(self) -> None:
        casa = Casa("Calle Sol 1", "28001", 50, 120_000, 2, localidad="Madrid")
        with self.assertRaises(ValueError) as ctx:
            casa.alquilar(
                self.inquilino,
                renta=400,
                fianza=800,
                fecha_inicio=date(2026, 3, 1),
                renta_ya_comprometida=600,
            )
        self.assertIn("35 %", str(ctx.exception))
        self.assertEqual(casa.estado.name, "DISPONIBLE")

    def test_casa_acepta_si_cabe_en_margen(self) -> None:
        casa = Casa("Calle Luna 2", "28002", 40, 100_000, 1, localidad="Madrid")
        contrato = casa.alquilar(
            self.inquilino,
            renta=100,
            fianza=200,
            fecha_inicio=date(2026, 3, 1),
            renta_ya_comprometida=600,
        )
        self.assertEqual(contrato.renta, 100)
        self.assertEqual(casa.estado.name, "ALQUILADA")


if __name__ == "__main__":
    unittest.main()
