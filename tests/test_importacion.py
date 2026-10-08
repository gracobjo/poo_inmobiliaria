"""Tests del importador de datos hacia el dominio."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.importacion import ImportadorDatos
from src.modelos.casa import Casa
from src.servicios.app_inmobiliaria import AppInmobiliaria
from src.utils.constantes import EstadoCasa


class TestImportacion(unittest.TestCase):
    """Carga desde dict, list, CSV, TXT, JSON y tabla."""

    def setUp(self) -> None:
        Casa.total_casas = 0
        Casa.impuesto_aitp = 0.10
        self.importador = ImportadorDatos()
        self.raiz = Path(__file__).resolve().parents[1]
        self.ejemplos = self.raiz / "data" / "ejemplos"

    def test_desde_dict(self) -> None:
        casa = self.importador.cargar_casas(
            {
                "direccion": "Calle Dict 1",
                "codigo_postal": "28013",
                "metros_cuadrados": 50,
                "precio": 100000,
                "habitaciones": 2,
                "localidad": "Madrid",
            }
        )[0]
        self.assertEqual(casa.localidad, "Madrid")
        self.assertEqual(casa.estado, EstadoCasa.DISPONIBLE)

    def test_desde_lista_con_alias(self) -> None:
        casas = self.importador.cargar_casas(
            [
                {
                    "address": "Street 1",
                    "cp": "08001",
                    "m2": 60,
                    "price": 200000,
                    "rooms": 2,
                    "city": "Barcelona",
                }
            ]
        )
        self.assertEqual(len(casas), 1)
        self.assertEqual(casas[0].codigo_postal, "08001")
        self.assertEqual(casas[0].precio_m2, 200000 / 60)

    def test_desde_tabla(self) -> None:
        tabla = [
            ["direccion", "codigo_postal", "metros_cuadrados", "precio", "habitaciones"],
            ["Calle Tabla", "41001", 70, 180000, 3],
        ]
        casas = self.importador.cargar_casas(tabla)
        self.assertEqual(casas[0].direccion, "Calle Tabla")

    def test_desde_csv_ejemplo(self) -> None:
        resultado = self.importador.importar_casas(self.ejemplos / "casas.csv")
        self.assertEqual(resultado.ok, 3)
        self.assertEqual(resultado.errores, [])

    def test_csv_diez_tipos(self) -> None:
        from src.utils.constantes import TipoVivienda

        resultado = self.importador.importar_casas(self.ejemplos / "casas_10_tipos.csv")
        self.assertEqual(resultado.errores, [])
        self.assertGreaterEqual(resultado.ok, 10)
        tipos = {casa.tipo_vivienda for casa in resultado.exitosos}
        self.assertIn(TipoVivienda.CHALET, tipos)
        self.assertIn(TipoVivienda.LOCAL, tipos)
        self.assertIn(TipoVivienda.ATICO, tipos)
        self.assertEqual(len(tipos), resultado.ok)

    def test_desde_txt_pipe(self) -> None:
        casas = self.importador.cargar_casas(self.ejemplos / "casas.txt")
        self.assertEqual(len(casas), 2)
        self.assertEqual(casas[0].localidad, "Sevilla")

    def test_desde_json(self) -> None:
        casas = self.importador.cargar_casas(self.ejemplos / "casas.json")
        self.assertEqual(len(casas), 2)
        self.assertEqual(casas[0].direccion, "Calle JSON 1")

    def test_fila_invalida_no_strict(self) -> None:
        resultado = self.importador.importar_casas(
            [
                {
                    "direccion": "Ok",
                    "codigo_postal": "28001",
                    "metros_cuadrados": 40,
                    "precio": 120000,
                    "habitaciones": 1,
                },
                {
                    "direccion": "Mal CP",
                    "codigo_postal": "99999",
                    "metros_cuadrados": 40,
                    "precio": 120000,
                    "habitaciones": 1,
                },
            ]
        )
        self.assertEqual(resultado.ok, 1)
        self.assertEqual(len(resultado.errores), 1)

    def test_app_persiste_importacion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "test.db"
            app = AppInmobiliaria(db)
            iniciales = len(app.gestion.propiedades)
            resultado = app.importar_casas(self.ejemplos / "casas.csv")
            self.assertEqual(resultado.ok, 3)
            self.assertEqual(len(app.gestion.propiedades), iniciales + 3)
            app.cerrar()


if __name__ == "__main__":
    unittest.main()
