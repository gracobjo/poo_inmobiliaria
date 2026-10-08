"""Demostración completa del Sistema Inmobiliario POO.

Recorre los conceptos principales de Programación Orientada a Objetos
aplicados al dominio inmobiliario: clases, encapsulamiento, properties,
métodos de instancia/clase/estáticos, atributos de clase, enumeraciones
y manejo de errores.
"""

from __future__ import annotations

import sys
from datetime import date

from src.modelos.casa import Casa
from src.modelos.contrato import Contrato
from src.modelos.inquilino import Inquilino
from src.servicios.gestion_inmobiliaria import GestionInmobiliaria
from src.utils.constantes import EstadoCasa, TipoOperacion


def _configurar_salida() -> None:
    """Fuerza UTF-8 en stdout/stderr cuando la consola lo permite."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _separador(titulo: str) -> None:
    """Imprime un encabezado de sección en consola."""
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def demostrar_creacion() -> tuple[Casa, Casa, Casa, Inquilino, GestionInmobiliaria]:
    """Crea objetos de dominio y registra propiedades en la cartera."""
    _separador("1. Creación de objetos (clases e instancias)")

    # Reinicio de atributos de clase para una demo reproducible.
    Casa.total_casas = 0
    Casa.impuesto_aitp = 0.10
    Casa.iva_reforma = 0.21

    casa_madrid = Casa(
        direccion="Calle Mayor 12",
        codigo_postal="28013",
        metros_cuadrados=85,
        precio=250_000,
        habitaciones=3,
        localidad="Madrid",
    )
    casa_barcelona = Casa.desde_diccionario(
        {
            "direccion": "Av. Diagonal 200",
            "codigo_postal": "08018",
            "metros_cuadrados": 70,
            "precio": 310_000,
            "habitaciones": 2,
            "localidad": "Barcelona",
            "estado": "DISPONIBLE",
        }
    )
    casa_sevilla = Casa(
        direccion="Plaza Nueva 5",
        codigo_postal="41001",
        metros_cuadrados=95,
        precio=180_000,
        habitaciones=4,
        localidad="Sevilla",
    )

    inquilino = Inquilino(
        nombre="Laura García",
        dni="12345678Z",
        telefono="600111222",
        ingresos=2_800,
    )

    gestion = GestionInmobiliaria()
    for casa in (casa_madrid, casa_barcelona, casa_sevilla):
        gestion.agregar_propiedad(casa)

    print(f"Casas creadas (atributo de clase total_casas): {Casa.total_casas}")
    print(f"Inquilino: {inquilino}")
    print(f"DNI encapsulado (property): {inquilino.dni}")
    print(f"Estados posibles: {[e.name for e in EstadoCasa]}")
    print(f"Tipos de operación: {[t.name for t in TipoOperacion]}")
    for casa in gestion.propiedades:
        print(f"  * {casa}")

    return casa_madrid, casa_barcelona, casa_sevilla, inquilino, gestion


def demostrar_venta(casa: Casa) -> None:
    """Demuestra reserva y compra con impuesto AITP (atributo de clase)."""
    _separador("2. Venta (métodos de instancia + atributo de clase AITP)")

    print(f"Impuesto AITP actual: {Casa.impuesto_aitp:.0%}")
    casa.reservar()
    print(f"Tras reservar -> estado: {casa.estado.name}")

    Casa.cambiar_impuesto_aitp(0.08)
    print(f"AITP actualizado con método de clase: {Casa.impuesto_aitp:.0%}")

    precio_final = casa.comprar()
    print(f"Precio base: {casa.precio:,.2f} €")
    print(f"Precio final con AITP: {precio_final:,.2f} €")
    print(f"Estado final: {casa.estado.name}")
    print(f"Historial: {[op.name for op in casa.historial_operaciones]}")


def demostrar_alquiler(casa: Casa, inquilino: Inquilino) -> Contrato:
    """Demuestra alquiler, regla del 35 % y vigencia del contrato."""
    _separador("3. Alquiler (colaboración entre objetos + encapsulamiento)")

    renta = 900.0
    print(f"¿Puede alquilar con renta {renta:.0f} €? -> {inquilino.puede_alquilar(renta)}")

    contrato = casa.alquilar(
        inquilino=inquilino,
        renta=renta,
        fianza=1_800,
        fecha_inicio=date(2026, 3, 1),
        meses=12,
    )
    print(f"Casa alquilada: {casa}")
    print(f"Contrato: {contrato}")
    print(f"¿Vigente el 2026-06-15? -> {contrato.esta_vigente(date(2026, 6, 15))}")
    print(
        f"Total pagado hasta 2026-09-01: "
        f"{contrato.calcular_total_pagado(date(2026, 9, 1)):,.2f} €"
    )
    return contrato


def demostrar_mejoras(casa: Casa) -> None:
    """Demuestra decoración y reforma con IVA (atributo de clase)."""
    _separador("4. Mejoras (decorar / reformar) y cambio de estado")

    print(f"Precio antes de mejoras: {casa.precio:,.2f} €")
    coste_decoracion = casa.decorar(4_500)
    print(f"Decoración: +{coste_decoracion:,.2f} € -> precio {casa.precio:,.2f} €")

    # Liberar alquiler para poder reformar con claridad en la demo.
    if casa.estado == EstadoCasa.ALQUILADA:
        casa.liberar()
        print(f"Alquiler liberado -> estado: {casa.estado.name}")

    print(f"IVA reforma (atributo de clase): {Casa.iva_reforma:.0%}")
    coste_reforma = casa.reformar(12_000)
    print(f"Reforma con IVA: {coste_reforma:,.2f} € -> precio {casa.precio:,.2f} €")
    print(f"Estado: {casa.estado.name}")
    casa.finalizar_reforma()
    print(f"Tras finalizar reforma -> estado: {casa.estado.name}")
    print(f"Historial: {[op.name for op in casa.historial_operaciones]}")


def demostrar_calculos(casa_a: Casa, casa_b: Casa) -> None:
    """Demuestra métodos estáticos, properties y rentabilidad."""
    _separador("5. Cálculos (estáticos, properties y rentabilidad)")

    print(f"Precio/m² de {casa_a.localidad}: {casa_a.precio_m2:,.2f} €/m²")
    print(f"Precio/m² de {casa_b.localidad}: {casa_b.precio_m2:,.2f} €/m²")
    print(
        "calcular_precio_m2(200000, 80) = "
        f"{Casa.calcular_precio_m2(200_000, 80):,.2f} €/m²"
    )

    mejor = Casa.comparar_inversion(casa_a, casa_b)
    print(f"Mejor inversión (€/m² más bajo): {mejor.direccion} ({mejor.localidad})")

    if casa_a.estado != EstadoCasa.VENDIDA:
        rentabilidad = casa_a.calcular_rentabilidad(850)
        print(f"Rentabilidad bruta anual estimada (850 €/mes): {rentabilidad:.2f} %")


def demostrar_informe(gestion: GestionInmobiliaria) -> None:
    """Demuestra consultas del servicio e informe de cartera."""
    _separador("6. Servicio GestionInmobiliaria e informe de cartera")

    disponibles = gestion.listar_disponibles()
    print(f"Disponibles: {len(disponibles)}")
    for casa in disponibles:
        print(f"  * {casa}")

    en_madrid = gestion.listar_por_localidad("Madrid")
    print(f"En Madrid: {len(en_madrid)}")

    rango = gestion.buscar_por_precio(150_000, 300_000)
    print(f"Entre 150.000 y 300.000 €: {len(rango)}")

    print(f"Valor de cartera: {gestion.calcular_valor_cartera():,.2f} €")
    print()
    print(gestion.generar_informe_cartera())


def demostrar_encapsulamiento() -> None:
    """Muestra validaciones y encapsulamiento con try/except."""
    _separador("7. Encapsulamiento y manejo de errores (try/except)")

    try:
        Casa(
            direccion="",
            codigo_postal="28013",
            metros_cuadrados=50,
            precio=100_000,
            habitaciones=2,
        )
    except ValueError as error:
        print(f"[OK] Dirección vacía rechazada: {error}")

    try:
        Casa(
            direccion="Calle Error",
            codigo_postal="99999",
            metros_cuadrados=50,
            precio=100_000,
            habitaciones=2,
        )
    except ValueError as error:
        print(f"[OK] CP inválido rechazado: {error}")

    try:
        inquilino = Inquilino("Pedro Ruiz", "11111111H", "600000000", 1_500)
        print(f"DNI solo lectura: {inquilino.dni}")
        inquilino.dni = "00000000T"  # type: ignore[misc]
    except AttributeError as error:
        print(f"[OK] DNI no modificable desde fuera: {error}")

    try:
        inquilino_ok = Inquilino("Marta Sol", "22222222J", "611222333", 1_600)
        casa = Casa("Calle Prueba 1", "28001", 40, 120_000, 1, localidad="Madrid")
        casa.alquilar(inquilino_ok, renta=900, fianza=900)
    except ValueError as error:
        print(f"[OK] Regla del 35 % aplicada: {error}")

    try:
        Casa.cambiar_impuesto_aitp(1.5)
    except ValueError as error:
        print(f"[OK] AITP fuera de rango rechazado: {error}")


def main() -> None:
    """Ejecuta la demostración completa del sistema."""
    _configurar_salida()
    print("Sistema Inmobiliario POO - Demostracion completa")
    print("Python 3.14+ - Clases, encapsulamiento y servicios")

    casa_madrid, casa_barcelona, casa_sevilla, inquilino, gestion = demostrar_creacion()
    demostrar_venta(casa_barcelona)
    demostrar_alquiler(casa_sevilla, inquilino)
    demostrar_mejoras(casa_sevilla)
    demostrar_calculos(casa_madrid, casa_sevilla)
    demostrar_informe(gestion)
    demostrar_encapsulamiento()

    _separador("Demo finalizada")
    print("Todos los conceptos POO del proyecto han sido ejercitados.")


if __name__ == "__main__":
    main()
