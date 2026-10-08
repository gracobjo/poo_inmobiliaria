"""Punto de entrada del Sistema Inmobiliario POO.

Por defecto lanza la interfaz gráfica dual Agente/Cliente con SQLite.
Usa ``--demo`` para ejecutar la demostración por consola.
"""

from __future__ import annotations

import argparse


def main() -> None:
    """Lanza la app gráfica o la demo de consola según argumentos."""
    parser = argparse.ArgumentParser(description="Sistema Inmobiliario POO")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Ejecuta la demostración completa por consola",
    )
    args = parser.parse_args()

    if args.demo:
        from ejemplos.demo_completa import main as ejecutar_demo

        ejecutar_demo()
        return

    from src.ui.app_grafica import ejecutar_app

    ejecutar_app()


if __name__ == "__main__":
    main()
