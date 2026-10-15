"""Modelos de dominio del Sistema Inmobiliario POO."""

from src.modelos.casa import Casa
from src.modelos.contrato import Contrato, ResolucionContrato
from src.modelos.inquilino import Inquilino

__all__ = [
    "Casa",
    "Contrato",
    "Inquilino",
    "ResolucionContrato",
]
