"""Tests de reservas con cliente, fecha e informe."""

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from src.modelos.casa import Casa
from src.modelos.inquilino import Inquilino
from src.servicios.app_inmobiliaria import AppInmobiliaria
from src.servicios.gestion_inmobiliaria import GestionInmobiliaria
from src.utils.constantes import EstadoCasa


class TestReserva(unittest.TestCase):
    """Reserva enlaza cliente/fecha y aparece en el informe."""

    def setUp(self) -> None:
        Casa.total_casas = 0
        self.cliente = Inquilino("prueba1", "12345678Z", "111111111", 2_000)
        self.casa = Casa("Av. América 40", "28002", 145, 410_000, 4, localidad="Madrid")

    def test_informe_incluye_cliente_y_fecha(self) -> None:
        momento = datetime(2026, 10, 15, 9, 20)
        self.casa.reservar(self.cliente, fecha=momento)
        gestion = GestionInmobiliaria()
        gestion.agregar_propiedad(self.casa)
        informe = gestion.generar_informe_cartera()
        self.assertIn("RESERVADA", informe)
        self.assertIn("prueba1", informe)
        self.assertIn("12345678Z", informe)
        self.assertIn("15/10/2026 09:20", informe)

    def test_persistencia_reserva(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            app = AppInmobiliaria(ruta_db=Path(tmp) / "t.db")
            casa = next(c for c in app.gestion.propiedades if c.estado == EstadoCasa.DISPONIBLE)
            casa_id = casa.id
            assert casa_id is not None
            momento = datetime(2026, 10, 15, 10, 5)
            casa.reservar(self.cliente, fecha=momento)
            app.sincronizar(casa)

            app.cargar()
            recargada = app.obtener_casa(casa_id)
            self.assertIsNotNone(recargada)
            assert recargada is not None
            self.assertEqual(recargada.estado, EstadoCasa.RESERVADA)
            self.assertIsNotNone(recargada.reserva)
            assert recargada.reserva is not None
            self.assertEqual(recargada.reserva.cliente.dni, "12345678Z")
            self.assertEqual(recargada.reserva.fecha, momento)
            app.cerrar()


if __name__ == "__main__":
    unittest.main()
