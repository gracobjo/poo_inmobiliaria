"""Servicio de aplicación con persistencia SQLite."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from src.modelos.casa import Casa
from src.modelos.contrato import Contrato
from src.modelos.inquilino import Inquilino
from src.persistencia.database import Database
from src.persistencia.repositorio import RepositorioInmobiliario
from src.servicios.gestion_inmobiliaria import GestionInmobiliaria
from src.utils.constantes import EstadoCasa


class AppInmobiliaria:
    """Fachada para la UI: dominio + SQLite + semillas iniciales."""

    def __init__(self, ruta_db: str | Path | None = None) -> None:
        raiz = Path(__file__).resolve().parents[2]
        self.ruta_db: Path = Path(ruta_db) if ruta_db else raiz / "data" / "inmobiliaria.db"
        self._database = Database(self.ruta_db)
        self._repo = RepositorioInmobiliario(self._database)
        self.gestion = GestionInmobiliaria()
        self.cargar()
        if self._repo.contar_casas() == 0:
            self._sembrar_datos()

    def cargar(self) -> None:
        """Recarga la cartera desde SQLite."""
        Casa.total_casas = 0
        # Vacía la lista privada y vuelve a poblar.
        self.gestion = GestionInmobiliaria()
        for casa in self._repo.listar_casas():
            self.gestion.agregar_propiedad(casa)
        Casa.total_casas = len(self.gestion.propiedades)

    def guardar_casa(self, casa: Casa) -> Casa:
        """Persiste una vivienda y la mantiene en la cartera en memoria."""
        self._repo.guardar_casa(casa)
        if casa not in self.gestion.propiedades:
            # Puede ser nueva: si no está, agregarla.
            try:
                self.gestion.agregar_propiedad(casa)
            except ValueError:
                pass
        else:
            # Actualizar referencia: re-cargar para consistencia simple.
            pass
        self.cargar()
        return casa

    def agregar_casa(self, casa: Casa) -> Casa:
        """Añade una vivienda nueva a memoria y SQLite."""
        self.gestion.agregar_propiedad(casa)
        return self._repo.guardar_casa(casa)

    def sincronizar(self, casa: Casa) -> None:
        """Guarda el estado actual de una vivienda ya existente."""
        self._repo.guardar_casa(casa)
        self.cargar()

    def obtener_casa(self, casa_id: int) -> Casa | None:
        """Busca una casa por id en la cartera cargada."""
        for casa in self.gestion.propiedades:
            if casa.id == casa_id:
                return casa
        return None

    def crear_solicitud(
        self,
        casa_id: int,
        cliente: Inquilino,
        tipo: str,
        mensaje: str = "",
    ) -> int:
        """Registra una solicitud de cliente."""
        if self.obtener_casa(casa_id) is None:
            raise ValueError("La vivienda indicada no existe.")
        self._repo.guardar_cliente(cliente)
        return self._repo.crear_solicitud(casa_id, cliente, tipo, mensaje)

    def listar_solicitudes(self, solo_pendientes: bool = False) -> list[dict]:
        """Lista solicitudes persistidas."""
        return self._repo.listar_solicitudes(solo_pendientes=solo_pendientes)

    def atender_solicitud(self, solicitud_id: int) -> None:
        """Marca una solicitud como atendida."""
        self._repo.actualizar_estado_solicitud(solicitud_id, "ATENDIDA")

    def cerrar(self) -> None:
        """Cierra la base de datos."""
        self._database.cerrar()

    def _sembrar_datos(self) -> None:
        """Inserta un inventario de ejemplo la primera vez."""
        semillas = [
            Casa("Calle Mayor 12", "28013", 85, 250_000, 3, localidad="Madrid"),
            Casa("Av. Diagonal 200", "08018", 70, 310_000, 2, localidad="Barcelona"),
            Casa("Plaza Nueva 5", "41001", 95, 180_000, 4, localidad="Sevilla"),
            Casa("Calle Larios 8", "29015", 60, 195_000, 2, localidad="Málaga"),
        ]
        for casa in semillas:
            self.agregar_casa(casa)

        # Ejemplo de alquiler vigente en Sevilla para demo agente.
        sevilla = next(c for c in self.gestion.propiedades if c.localidad == "Sevilla")
        inquilino = Inquilino("Laura García", "12345678Z", "600111222", 2_800)
        sevilla.alquilar(
            inquilino,
            renta=900,
            fianza=1_800,
            fecha_inicio=date(2026, 1, 1),
            meses=12,
        )
        self.sincronizar(sevilla)
