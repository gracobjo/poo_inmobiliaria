"""Repositorio SQLite para cartera, clientes, contratos y solicitudes."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from src.modelos.casa import Casa
from src.modelos.contrato import Contrato
from src.modelos.inquilino import Inquilino
from src.persistencia.database import Database
from src.utils.constantes import EstadoCasa, TipoOperacion


class RepositorioInmobiliario:
    """Persistencia de entidades del dominio inmobiliario."""

    def __init__(self, database: Database) -> None:
        self._db = database

    # ------------------------------------------------------------------
    # Casas
    # ------------------------------------------------------------------

    def listar_casas(self) -> list[Casa]:
        """Carga todas las viviendas con contrato asociado si existe."""
        filas = self._db.conexion.execute(
            "SELECT * FROM casas ORDER BY id"
        ).fetchall()
        return [self._fila_a_casa(fila) for fila in filas]

    def guardar_casa(self, casa: Casa) -> Casa:
        """Inserta o actualiza una vivienda y su contrato."""
        historial = ",".join(op.name for op in casa.historial_operaciones)
        if casa.id is None:
            cursor = self._db.conexion.execute(
                """
                INSERT INTO casas (
                    direccion, codigo_postal, localidad, metros_cuadrados,
                    precio, habitaciones, estado, historial
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    casa.direccion,
                    casa.codigo_postal,
                    casa.localidad,
                    casa.metros_cuadrados,
                    casa.precio,
                    casa.habitaciones,
                    casa.estado.name,
                    historial,
                ),
            )
            casa.id = int(cursor.lastrowid)
        else:
            self._db.conexion.execute(
                """
                UPDATE casas SET
                    direccion = ?, codigo_postal = ?, localidad = ?,
                    metros_cuadrados = ?, precio = ?, habitaciones = ?,
                    estado = ?, historial = ?
                WHERE id = ?
                """,
                (
                    casa.direccion,
                    casa.codigo_postal,
                    casa.localidad,
                    casa.metros_cuadrados,
                    casa.precio,
                    casa.habitaciones,
                    casa.estado.name,
                    historial,
                    casa.id,
                ),
            )
        self._sincronizar_contrato(casa)
        self._db.conexion.commit()
        return casa

    def eliminar_casa(self, casa_id: int) -> None:
        """Elimina una vivienda por id."""
        self._db.conexion.execute("DELETE FROM casas WHERE id = ?", (casa_id,))
        self._db.conexion.commit()

    def _sincronizar_contrato(self, casa: Casa) -> None:
        if casa.id is None:
            return
        self._db.conexion.execute(
            "DELETE FROM contratos WHERE casa_id = ?", (casa.id,)
        )
        contrato = casa.contrato
        if contrato is None:
            return
        cliente_id = self.guardar_cliente(contrato.inquilino)
        self._db.conexion.execute(
            """
            INSERT INTO contratos (
                casa_id, cliente_id, fecha_inicio, fecha_fin, renta, fianza
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                casa.id,
                cliente_id,
                contrato.fecha_inicio.isoformat(),
                contrato.fecha_fin.isoformat(),
                contrato.renta,
                contrato.fianza,
            ),
        )

    def _fila_a_casa(self, fila: Any) -> Casa:
        estado = EstadoCasa[fila["estado"]]
        casa = Casa(
            direccion=fila["direccion"],
            codigo_postal=fila["codigo_postal"],
            metros_cuadrados=fila["metros_cuadrados"],
            precio=fila["precio"],
            habitaciones=fila["habitaciones"],
            estado=estado,
            localidad=fila["localidad"] or "",
            id=fila["id"],
        )
        # Evita inflar total_casas al recargar: se ajusta desde el servicio.
        historial_raw = (fila["historial"] or "").strip()
        if historial_raw:
            ops = [TipoOperacion[nombre] for nombre in historial_raw.split(",") if nombre]
            casa.restaurar_historial(ops)

        contrato_fila = self._db.conexion.execute(
            """
            SELECT c.*, cl.nombre, cl.dni, cl.telefono, cl.ingresos
            FROM contratos c
            JOIN clientes cl ON cl.id = c.cliente_id
            WHERE c.casa_id = ?
            """,
            (fila["id"],),
        ).fetchone()
        if contrato_fila is not None:
            inquilino = Inquilino(
                nombre=contrato_fila["nombre"],
                dni=contrato_fila["dni"],
                telefono=contrato_fila["telefono"],
                ingresos=contrato_fila["ingresos"],
            )
            contrato = Contrato(
                inquilino=inquilino,
                fecha_inicio=date.fromisoformat(contrato_fila["fecha_inicio"]),
                fecha_fin=date.fromisoformat(contrato_fila["fecha_fin"]),
                renta=contrato_fila["renta"],
                fianza=contrato_fila["fianza"],
            )
            casa.asociar_contrato(contrato)
        return casa

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------

    def guardar_cliente(self, cliente: Inquilino) -> int:
        """Inserta o actualiza un cliente por DNI. Devuelve su id."""
        existente = self._db.conexion.execute(
            "SELECT id FROM clientes WHERE dni = ?", (cliente.dni,)
        ).fetchone()
        if existente is None:
            cursor = self._db.conexion.execute(
                """
                INSERT INTO clientes (nombre, dni, telefono, ingresos)
                VALUES (?, ?, ?, ?)
                """,
                (cliente.nombre, cliente.dni, cliente.telefono, cliente.ingresos),
            )
            self._db.conexion.commit()
            return int(cursor.lastrowid)

        self._db.conexion.execute(
            """
            UPDATE clientes
            SET nombre = ?, telefono = ?, ingresos = ?
            WHERE id = ?
            """,
            (cliente.nombre, cliente.telefono, cliente.ingresos, existente["id"]),
        )
        self._db.conexion.commit()
        return int(existente["id"])

    def obtener_cliente_por_dni(self, dni: str) -> Inquilino | None:
        """Busca un cliente por DNI."""
        fila = self._db.conexion.execute(
            "SELECT * FROM clientes WHERE dni = ?", (dni.strip().upper(),)
        ).fetchone()
        if fila is None:
            return None
        return Inquilino(
            nombre=fila["nombre"],
            dni=fila["dni"],
            telefono=fila["telefono"],
            ingresos=fila["ingresos"],
        )

    # ------------------------------------------------------------------
    # Solicitudes
    # ------------------------------------------------------------------

    def crear_solicitud(
        self,
        casa_id: int,
        cliente: Inquilino,
        tipo: str,
        mensaje: str = "",
    ) -> int:
        """Registra una solicitud de cliente (visita, interés, etc.)."""
        cliente_id = self.guardar_cliente(cliente)
        cursor = self._db.conexion.execute(
            """
            INSERT INTO solicitudes (casa_id, cliente_id, tipo, mensaje, fecha, estado)
            VALUES (?, ?, ?, ?, ?, 'PENDIENTE')
            """,
            (
                casa_id,
                cliente_id,
                tipo.strip().upper(),
                mensaje.strip(),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        self._db.conexion.commit()
        return int(cursor.lastrowid)

    def listar_solicitudes(self, solo_pendientes: bool = False) -> list[dict[str, Any]]:
        """Lista solicitudes con datos de casa y cliente."""
        sql = """
            SELECT
                s.id, s.tipo, s.mensaje, s.fecha, s.estado,
                c.direccion, c.localidad, c.precio,
                cl.nombre, cl.dni, cl.telefono, cl.ingresos
            FROM solicitudes s
            JOIN casas c ON c.id = s.casa_id
            JOIN clientes cl ON cl.id = s.cliente_id
        """
        if solo_pendientes:
            sql += " WHERE s.estado = 'PENDIENTE'"
        sql += " ORDER BY s.id DESC"
        filas = self._db.conexion.execute(sql).fetchall()
        return [dict(fila) for fila in filas]

    def actualizar_estado_solicitud(self, solicitud_id: int, estado: str) -> None:
        """Cambia el estado de una solicitud."""
        self._db.conexion.execute(
            "UPDATE solicitudes SET estado = ? WHERE id = ?",
            (estado.strip().upper(), solicitud_id),
        )
        self._db.conexion.commit()

    def contar_casas(self) -> int:
        """Número de viviendas persistidas."""
        fila = self._db.conexion.execute("SELECT COUNT(*) AS n FROM casas").fetchone()
        return int(fila["n"])
