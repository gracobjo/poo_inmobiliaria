"""Tests unitarios de la clase ``Contrato``."""

from __future__ import annotations

import unittest
from datetime import date

from src.modelos.contrato import Contrato
from src.modelos.inquilino import Inquilino


class TestContrato(unittest.TestCase):
    """Casos de prueba para creación, total pagado y vigencia."""

    def setUp(self) -> None:
        """Prepara un inquilino y fechas de contrato de referencia."""
        self.inquilino = Inquilino(
            nombre="Luis Perez",
            dni="87654321X",
            telefono="600333444",
            ingresos=2_500,
        )
        self.inicio = date(2026, 1, 1)
        self.fin = date(2026, 12, 31)
        self.contrato = Contrato(
            inquilino=self.inquilino,
            fecha_inicio=self.inicio,
            fecha_fin=self.fin,
            renta=700,
            fianza=1_400,
        )

    def test_creacion_exitosa(self) -> None:
        """Un contrato válido guarda inquilino, fechas e importes."""
        self.assertIs(self.contrato.inquilino, self.inquilino)
        self.assertEqual(self.contrato.fecha_inicio, self.inicio)
        self.assertEqual(self.contrato.fecha_fin, self.fin)
        self.assertEqual(self.contrato.renta, 700)
        self.assertEqual(self.contrato.fianza, 1_400)

    def test_creacion_fechas_invalidas(self) -> None:
        """Fin anterior o igual al inicio provoca ``ValueError``."""
        with self.assertRaises(ValueError):
            Contrato(self.inquilino, self.fin, self.inicio, 700, 1_400)
        with self.assertRaises(ValueError):
            Contrato(self.inquilino, self.inicio, self.inicio, 700, 1_400)

    def test_creacion_importes_invalidos(self) -> None:
        """Renta no positiva o fianza negativa provocan ``ValueError``."""
        with self.assertRaises(ValueError):
            Contrato(self.inquilino, self.inicio, self.fin, 0, 1_400)
        with self.assertRaises(ValueError):
            Contrato(self.inquilino, self.inicio, self.fin, 700, -1)

    def test_creacion_inquilino_invalido(self) -> None:
        """Un inquilino que no es ``Inquilino`` provoca ``TypeError``."""
        with self.assertRaises(TypeError):
            Contrato("no-inquilino", self.inicio, self.fin, 700, 1_400)  # type: ignore[arg-type]

    def test_calcular_total_pagado(self) -> None:
        """Total = fianza + renta × meses completos hasta la fecha de corte."""
        # Antes del inicio: 0
        self.assertEqual(self.contrato.calcular_total_pagado(date(2025, 12, 1)), 0.0)

        # Exactamente 3 meses después del inicio: fianza + 3 * renta
        total_3m = self.contrato.calcular_total_pagado(date(2026, 4, 1))
        self.assertAlmostEqual(total_3m, 1_400 + 700 * 3)

        # Tras el fin: se acota a fecha_fin (12 meses exactos el 31/12)
        total_fin = self.contrato.calcular_total_pagado(date(2027, 6, 1))
        self.assertAlmostEqual(total_fin, 1_400 + 700 * 11)

    def test_esta_vigente(self) -> None:
        """La vigencia cubre el intervalo cerrado [inicio, fin]."""
        self.assertFalse(self.contrato.esta_vigente(date(2025, 12, 31)))
        self.assertTrue(self.contrato.esta_vigente(self.inicio))
        self.assertTrue(self.contrato.esta_vigente(date(2026, 6, 15)))
        self.assertTrue(self.contrato.esta_vigente(self.fin))
        self.assertFalse(self.contrato.esta_vigente(date(2027, 1, 1)))


if __name__ == "__main__":
    unittest.main()
