"""Tests unitarios de la clase ``Casa``."""

from __future__ import annotations

import unittest
from datetime import date

from src.modelos.casa import Casa
from src.modelos.inquilino import Inquilino
from src.utils.constantes import EstadoCasa, TipoOperacion


class TestCasa(unittest.TestCase):
    """Casos de prueba para creación, operaciones y utilidades de ``Casa``."""

    def setUp(self) -> None:
        """Restaura atributos de clase y crea una vivienda base."""
        Casa.total_casas = 0
        Casa.impuesto_aitp = 0.10
        Casa.iva_reforma = 0.21
        self.casa = Casa(
            direccion="Calle Mayor 1",
            codigo_postal="28013",
            metros_cuadrados=80,
            precio=200_000,
            habitaciones=3,
            localidad="Madrid",
        )
        self.inquilino = Inquilino(
            nombre="Ana Lopez",
            dni="12345678Z",
            telefono="600111222",
            ingresos=3_000,
        )

    def test_creacion_exitosa(self) -> None:
        """Una casa válida se crea con estado disponible e incrementa el contador."""
        self.assertEqual(self.casa.direccion, "Calle Mayor 1")
        self.assertEqual(self.casa.codigo_postal, "28013")
        self.assertEqual(self.casa.localidad, "Madrid")
        self.assertEqual(self.casa.metros_cuadrados, 80)
        self.assertEqual(self.casa.precio, 200_000)
        self.assertEqual(self.casa.habitaciones, 3)
        self.assertEqual(self.casa.estado, EstadoCasa.DISPONIBLE)
        self.assertEqual(Casa.total_casas, 1)
        self.assertIsNone(self.casa.contrato)

    def test_validacion_precio_invalido(self) -> None:
        """Precio no positivo provoca ``ValueError``."""
        with self.assertRaises(ValueError):
            Casa("Calle X", "28013", 50, 0, 2)
        with self.assertRaises(ValueError):
            Casa("Calle X", "28013", 50, -10, 2)

    def test_validacion_cp_y_direccion(self) -> None:
        """CP inválido o dirección vacía provocan ``ValueError``."""
        with self.assertRaises(ValueError):
            Casa("Calle X", "99999", 50, 100_000, 2)
        with self.assertRaises(ValueError):
            Casa("   ", "28013", 50, 100_000, 2)

    def test_reservar(self) -> None:
        """Reservar pasa de DISPONIBLE a RESERVADA."""
        self.casa.reservar()
        self.assertEqual(self.casa.estado, EstadoCasa.RESERVADA)
        with self.assertRaises(ValueError):
            self.casa.reservar()

    def test_comprar(self) -> None:
        """Comprar aplica AITP, cambia estado y registra la operación."""
        precio_final = self.casa.comprar()
        self.assertAlmostEqual(precio_final, 220_000.0)
        self.assertEqual(self.casa.estado, EstadoCasa.VENDIDA)
        self.assertIn(TipoOperacion.VENTA, self.casa.historial_operaciones)
        with self.assertRaises(ValueError):
            self.casa.comprar()

    def test_comprar_desde_reservada(self) -> None:
        """Una vivienda reservada también puede comprarse."""
        self.casa.reservar()
        precio_final = self.casa.comprar()
        self.assertAlmostEqual(precio_final, 220_000.0)
        self.assertEqual(self.casa.estado, EstadoCasa.VENDIDA)

    def test_alquilar(self) -> None:
        """Alquilar crea contrato, cambia estado y valida la regla del 35 %."""
        contrato = self.casa.alquilar(
            inquilino=self.inquilino,
            renta=900,
            fianza=1_800,
            fecha_inicio=date(2026, 1, 1),
            meses=12,
        )
        self.assertEqual(self.casa.estado, EstadoCasa.ALQUILADA)
        self.assertIs(self.casa.contrato, contrato)
        self.assertEqual(contrato.renta, 900)
        self.assertIn(TipoOperacion.ALQUILER, self.casa.historial_operaciones)

        casa2 = Casa("Calle Sol 2", "28001", 60, 150_000, 2, localidad="Madrid")
        with self.assertRaises(ValueError):
            casa2.alquilar(self.inquilino, renta=2_000, fianza=2_000)

    def test_liberar(self) -> None:
        """Liberar deshace reserva o alquiler y deja la casa disponible."""
        self.casa.reservar()
        self.casa.liberar()
        self.assertEqual(self.casa.estado, EstadoCasa.DISPONIBLE)

        self.casa.alquilar(
            self.inquilino,
            renta=800,
            fianza=1_600,
            fecha_inicio=date(2026, 2, 1),
        )
        self.casa.liberar()
        self.assertEqual(self.casa.estado, EstadoCasa.DISPONIBLE)
        self.assertIsNone(self.casa.contrato)

        with self.assertRaises(ValueError):
            self.casa.liberar()

    def test_decorar(self) -> None:
        """Decorar incrementa el precio y registra la operación."""
        coste = self.casa.decorar(5_000)
        self.assertEqual(coste, 5_000)
        self.assertEqual(self.casa.precio, 205_000)
        self.assertIn(TipoOperacion.DECORACION, self.casa.historial_operaciones)

        self.casa.comprar()
        with self.assertRaises(ValueError):
            self.casa.decorar(1_000)

    def test_reformar_con_iva(self) -> None:
        """Reformar aplica IVA de clase, suma al precio y cambia estado."""
        coste_total = self.casa.reformar(10_000)
        self.assertAlmostEqual(coste_total, 12_100.0)
        self.assertAlmostEqual(self.casa.precio, 212_100.0)
        self.assertEqual(self.casa.estado, EstadoCasa.EN_REFORMA)
        self.assertIn(TipoOperacion.REFORMA, self.casa.historial_operaciones)

        with self.assertRaises(ValueError):
            self.casa.reformar(1_000)

    def test_rentabilidad(self) -> None:
        """La rentabilidad bruta anual se calcula como (renta*12/precio)*100."""
        # (1000 * 12 / 200000) * 100 = 6 %
        self.assertAlmostEqual(self.casa.calcular_rentabilidad(1_000), 6.0)
        with self.assertRaises(ValueError):
            self.casa.calcular_rentabilidad(0)

    def test_desde_diccionario(self) -> None:
        """``desde_diccionario`` construye una casa y acepta estado como str."""
        casa = Casa.desde_diccionario(
            {
                "direccion": "Av. Diagonal 100",
                "codigo_postal": "08008",
                "metros_cuadrados": 90,
                "precio": 350_000,
                "habitaciones": 4,
                "estado": "disponible",
                "localidad": "Barcelona",
            }
        )
        self.assertEqual(casa.localidad, "Barcelona")
        self.assertEqual(casa.estado, EstadoCasa.DISPONIBLE)
        self.assertEqual(casa.precio, 350_000)

        with self.assertRaises(ValueError):
            Casa.desde_diccionario({"direccion": "X"})

    def test_precio_m2(self) -> None:
        """``precio_m2`` y el estático ``calcular_precio_m2`` son coherentes."""
        self.assertAlmostEqual(self.casa.precio_m2, 2_500.0)
        self.assertAlmostEqual(Casa.calcular_precio_m2(100_000, 50), 2_000.0)
        with self.assertRaises(ValueError):
            Casa.calcular_precio_m2(100_000, 0)

    def test_historial_operaciones(self) -> None:
        """El historial acumula operaciones y se expone como copia."""
        self.casa.decorar(1_000)
        self.casa.reformar(2_000)
        historial = self.casa.historial_operaciones
        self.assertEqual(
            historial,
            [TipoOperacion.DECORACION, TipoOperacion.REFORMA],
        )
        historial.clear()
        self.assertEqual(len(self.casa.historial_operaciones), 2)


if __name__ == "__main__":
    unittest.main()
