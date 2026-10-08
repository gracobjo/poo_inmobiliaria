"""Capa de persistencia SQLite del Sistema Inmobiliario POO."""

from src.persistencia.database import Database
from src.persistencia.repositorio import RepositorioInmobiliario

__all__ = ["Database", "RepositorioInmobiliario"]
