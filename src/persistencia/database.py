"""Conexión y esquema SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    """Gestiona la conexión SQLite y la creación del esquema."""

    def __init__(self, ruta: str | Path) -> None:
        """Abre (o crea) la base de datos en ``ruta``."""
        self.ruta: Path = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection = sqlite3.connect(self.ruta)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._crear_esquema()

    @property
    def conexion(self) -> sqlite3.Connection:
        """Conexión activa a SQLite."""
        return self._conn

    def _crear_esquema(self) -> None:
        """Crea las tablas si no existen."""
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS casas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                direccion TEXT NOT NULL,
                codigo_postal TEXT NOT NULL,
                localidad TEXT NOT NULL DEFAULT '',
                metros_cuadrados REAL NOT NULL,
                precio REAL NOT NULL,
                habitaciones INTEGER NOT NULL,
                estado TEXT NOT NULL,
                historial TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dni TEXT NOT NULL UNIQUE,
                telefono TEXT NOT NULL,
                ingresos REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS contratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                casa_id INTEGER NOT NULL UNIQUE,
                cliente_id INTEGER NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT NOT NULL,
                renta REAL NOT NULL,
                fianza REAL NOT NULL,
                FOREIGN KEY (casa_id) REFERENCES casas(id) ON DELETE CASCADE,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            );

            CREATE TABLE IF NOT EXISTS solicitudes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                casa_id INTEGER NOT NULL,
                cliente_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                mensaje TEXT NOT NULL DEFAULT '',
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'PENDIENTE',
                FOREIGN KEY (casa_id) REFERENCES casas(id) ON DELETE CASCADE,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            );
            """
        )
        self._conn.commit()

    def cerrar(self) -> None:
        """Cierra la conexión."""
        self._conn.close()
