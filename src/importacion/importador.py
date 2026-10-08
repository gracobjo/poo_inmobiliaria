"""Importador de alto nivel hacia objetos del dominio."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from src.importacion.fuentes import FuenteDatos, extraer_registros
from src.importacion.mapeo import registro_a_casa, registro_a_inquilino
from src.modelos.casa import Casa
from src.modelos.inquilino import Inquilino

TipoEntidad = Literal["casa", "inquilino"]


@dataclass
class ResultadoImportacion:
    """Resultado de una importación masiva."""

    exitosos: list[Any] = field(default_factory=list)
    errores: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.exitosos) + len(self.errores)

    @property
    def ok(self) -> int:
        return len(self.exitosos)

    def resumen(self) -> str:
        lineas = [
            f"Importados correctamente: {self.ok}/{self.total}",
        ]
        if self.errores:
            lineas.append("Errores:")
            lineas.extend(f"  - {e}" for e in self.errores[:50])
            if len(self.errores) > 50:
                lineas.append(f"  … y {len(self.errores) - 50} más")
        return "\n".join(lineas)


class ImportadorDatos:
    """Carga CSV/TXT/JSON/Excel/dict/list/DataFrame y construye modelos POO.

    Ejemplo::

        imp = ImportadorDatos()
        casas = imp.cargar_casas("data/ejemplos/casas.csv")
        resultado = imp.importar_casas([{"direccion": "...", ...}])
    """

    def cargar_registros(
        self,
        fuente: FuenteDatos,
        *,
        delimitador: str | None = None,
    ) -> list[dict[str, Any]]:
        """Devuelve registros crudos normalizados como lista de dicts."""
        return extraer_registros(fuente, delimitador=delimitador)

    def cargar_casas(
        self,
        fuente: FuenteDatos,
        *,
        delimitador: str | None = None,
        strict: bool = False,
    ) -> list[Casa]:
        """Carga y convierte a ``Casa``.

        Args:
            fuente: Archivo o estructura de datos.
            delimitador: Delimitador CSV/TXT opcional.
            strict: Si es ``True``, el primer error aborta la carga.
        """
        resultado = self.importar_casas(fuente, delimitador=delimitador, strict=strict)
        if strict and resultado.errores:
            raise ValueError(resultado.errores[0])
        return list(resultado.exitosos)

    def cargar_inquilinos(
        self,
        fuente: FuenteDatos,
        *,
        delimitador: str | None = None,
        strict: bool = False,
    ) -> list[Inquilino]:
        """Carga y convierte a ``Inquilino``."""
        resultado = self.importar_inquilinos(
            fuente, delimitador=delimitador, strict=strict
        )
        if strict and resultado.errores:
            raise ValueError(resultado.errores[0])
        return list(resultado.exitosos)

    def importar_casas(
        self,
        fuente: FuenteDatos,
        *,
        delimitador: str | None = None,
        strict: bool = False,
    ) -> ResultadoImportacion:
        """Importa casas devolviendo éxitos y errores por fila."""
        return self._importar(
            fuente,
            entidad="casa",
            delimitador=delimitador,
            strict=strict,
        )

    def importar_inquilinos(
        self,
        fuente: FuenteDatos,
        *,
        delimitador: str | None = None,
        strict: bool = False,
    ) -> ResultadoImportacion:
        """Importa inquilinos devolviendo éxitos y errores por fila."""
        return self._importar(
            fuente,
            entidad="inquilino",
            delimitador=delimitador,
            strict=strict,
        )

    def _importar(
        self,
        fuente: FuenteDatos,
        *,
        entidad: TipoEntidad,
        delimitador: str | None,
        strict: bool,
    ) -> ResultadoImportacion:
        registros = extraer_registros(fuente, delimitador=delimitador)
        resultado = ResultadoImportacion()
        convertidor = registro_a_casa if entidad == "casa" else registro_a_inquilino

        for indice, registro in enumerate(registros, start=1):
            try:
                resultado.exitosos.append(convertidor(registro))
            except (ValueError, TypeError, KeyError) as error:
                mensaje = f"Fila {indice}: {error}"
                if strict:
                    raise ValueError(mensaje) from error
                resultado.errores.append(mensaje)
        return resultado
