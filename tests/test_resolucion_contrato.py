"""Tests de resolución formal de contratos de arrendamiento."""

from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from src.modelos.casa import Casa
from src.modelos.inquilino import Inquilino
from src.servicios.app_inmobiliaria import AppInmobiliaria
from src.utils.constantes import CausaResolucion, EstadoCasa, IniciativaResolucion


class TestResolucionContrato(unittest.TestCase):
    """Baja de contrato por iniciativa de arrendador/arrendatario."""

    def setUp(self) -> None:
        Casa.total_casas = 0
        self.inquilino = Inquilino("Ana Lopez", "12345678Z", "600111222", 3_000)
        self.casa = Casa(
            "Calle Mayor 1",
            "28013",
            80,
            200_000,
            3,
            localidad="Madrid",
        )
        self.casa.alquilar(
            self.inquilino,
            renta=900,
            fianza=1_800,
            fecha_inicio=date(2025, 1, 1),
            meses=24,
        )

    def test_arrendador_por_falta_de_pago(self) -> None:
        resolucion = self.casa.resolver_contrato(
            CausaResolucion.FALTA_PAGO_RENTA,
            IniciativaResolucion.ARRENDADOR,
            observaciones="Tres mensualidades impagadas",
            fecha=date(2026, 3, 15),
        )
        self.assertEqual(self.casa.estado, EstadoCasa.DISPONIBLE)
        self.assertIsNone(self.casa.contrato)
        self.assertEqual(resolucion.causa, CausaResolucion.FALTA_PAGO_RENTA)
        self.assertEqual(resolucion.iniciativa, IniciativaResolucion.ARRENDADOR)

    def test_arrendatario_no_puede_usar_causa_de_arrendador(self) -> None:
        with self.assertRaises(ValueError):
            self.casa.resolver_contrato(
                CausaResolucion.FALTA_PAGO_RENTA,
                IniciativaResolucion.ARRENDATARIO,
            )

    def test_desistimiento_requiere_seis_meses(self) -> None:
        casa = Casa("Calle Corta 2", "28001", 50, 150_000, 2, localidad="Madrid")
        casa.alquilar(
            self.inquilino,
            renta=800,
            fianza=1_600,
            fecha_inicio=date(2026, 8, 1),
            meses=12,
        )
        with self.assertRaises(ValueError) as ctx:
            casa.resolver_contrato(
                CausaResolucion.DESISTIMIENTO_INQUILINO,
                IniciativaResolucion.ARRENDATARIO,
                fecha=date(2026, 10, 15),  # < 6 meses
            )
        self.assertIn("6 meses", str(ctx.exception))

    def test_desistimiento_tras_seis_meses(self) -> None:
        resolucion = self.casa.resolver_contrato(
            CausaResolucion.DESISTIMIENTO_INQUILINO,
            IniciativaResolucion.ARRENDATARIO,
            fecha=date(2025, 8, 1),
        )
        self.assertEqual(resolucion.causa, CausaResolucion.DESISTIMIENTO_INQUILINO)
        self.assertEqual(self.casa.estado, EstadoCasa.DISPONIBLE)

    def test_mutuo_acuerdo_disponible_para_ambas_partes(self) -> None:
        resolucion = self.casa.resolver_contrato(
            CausaResolucion.MUTUO_ACUERDO,
            IniciativaResolucion.ARRENDADOR,
        )
        self.assertEqual(resolucion.causa, CausaResolucion.MUTUO_ACUERDO)

    def test_persistencia_resolucion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "test.db"
            app = AppInmobiliaria(ruta_db=ruta)
            # Semilla crea Sevilla alquilada; usamos una disponible.
            casa = next(c for c in app.gestion.propiedades if c.estado == EstadoCasa.DISPONIBLE)
            inquilino = Inquilino("Luis Perez", "87654321X", "600333444", 3_500)
            casa.alquilar(
                inquilino,
                renta=700,
                fianza=1_400,
                fecha_inicio=date(2025, 1, 1),
                meses=12,
            )
            app.sincronizar(casa)
            casa_id = casa.id
            assert casa_id is not None

            resolucion = app.resolver_contrato(
                casa_id,
                CausaResolucion.MUTUO_ACUERDO,
                IniciativaResolucion.ARRENDATARIO,
                observaciones="Fin anticipado de común acuerdo",
            )
            historial = app.listar_resoluciones(dni="87654321X")
            self.assertEqual(len(historial), 1)
            self.assertEqual(historial[0]["causa"], "MUTUO_ACUERDO")
            self.assertEqual(resolucion.observaciones, "Fin anticipado de común acuerdo")
            recargada = app.obtener_casa(casa_id)
            self.assertIsNotNone(recargada)
            assert recargada is not None
            self.assertEqual(recargada.estado, EstadoCasa.DISPONIBLE)
            self.assertIsNone(recargada.contrato)
            app.cerrar()


if __name__ == "__main__":
    unittest.main()
