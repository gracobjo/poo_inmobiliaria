"""Servicio de gestión de cartera inmobiliaria."""

from __future__ import annotations

from collections import Counter

from src.modelos.casa import Casa
from src.utils.constantes import EstadoCasa
from src.utils.validadores import ValidadoresInmobiliarios


class GestionInmobiliaria:
    """Gestiona una cartera privada de propiedades inmobiliarias.

    Centraliza altas, consultas filtradas, valoración agregada y
    generación de informes sobre el inventario.
    """

    def __init__(self) -> None:
        """Inicializa la cartera vacía."""
        self._propiedades: list[Casa] = []

    @property
    def propiedades(self) -> list[Casa]:
        """Copia de la lista de propiedades gestionadas."""
        return list(self._propiedades)

    def agregar_propiedad(self, propiedad: Casa) -> None:
        """Añade una vivienda a la cartera.

        Args:
            propiedad: Instancia de ``Casa`` a registrar.

        Raises:
            TypeError: Si ``propiedad`` no es una ``Casa``.
            ValueError: Si la vivienda ya está en la cartera.
        """
        if not isinstance(propiedad, Casa):
            raise TypeError("Solo se pueden agregar instancias de Casa.")
        if propiedad in self._propiedades:
            raise ValueError("La propiedad ya está registrada en la cartera.")
        self._propiedades.append(propiedad)

    def listar_disponibles(self) -> list[Casa]:
        """Devuelve las viviendas en estado ``DISPONIBLE``.

        Returns:
            Lista de propiedades disponibles (puede estar vacía).
        """
        return [casa for casa in self._propiedades if casa.estado == EstadoCasa.DISPONIBLE]

    def listar_por_localidad(self, localidad: str) -> list[Casa]:
        """Filtra propiedades por localidad (comparación sin mayúsculas).

        Args:
            localidad: Nombre del municipio o localidad (no vacío).

        Returns:
            Viviendas cuya ``localidad`` coincide con el criterio.

        Raises:
            ValueError: Si ``localidad`` está vacía.
        """
        if not ValidadoresInmobiliarios.es_string_no_vacio(localidad):
            raise ValueError("La localidad de búsqueda no puede estar vacía.")

        criterio: str = localidad.strip().casefold()
        return [
            casa
            for casa in self._propiedades
            if casa.localidad.casefold() == criterio
        ]

    def buscar_por_precio(
        self,
        precio_min: float = 0.0,
        precio_max: float | None = None,
    ) -> list[Casa]:
        """Busca viviendas cuyo precio está en el intervalo indicado.

        Args:
            precio_min: Precio mínimo inclusivo (>= 0).
            precio_max: Precio máximo inclusivo. Si es ``None``, sin techo.

        Returns:
            Lista de viviendas que cumplen el rango de precio.

        Raises:
            ValueError: Si los límites no son válidos o ``min > max``.
        """
        if not isinstance(precio_min, (int, float)) or isinstance(precio_min, bool) or precio_min < 0:
            raise ValueError("El precio mínimo debe ser un número >= 0.")
        if precio_max is not None:
            if not ValidadoresInmobiliarios.es_positivo(precio_max) and precio_max != 0:
                raise ValueError("El precio máximo debe ser un número >= 0.")
            if float(precio_min) > float(precio_max):
                raise ValueError("El precio mínimo no puede ser mayor que el máximo.")

        resultado: list[Casa] = []
        for casa in self._propiedades:
            if casa.precio < float(precio_min):
                continue
            if precio_max is not None and casa.precio > float(precio_max):
                continue
            resultado.append(casa)
        return resultado

    def calcular_valor_cartera(self) -> float:
        """Suma el precio de todas las propiedades de la cartera.

        Returns:
            Valor total en euros (0.0 si no hay propiedades).
        """
        return sum(casa.precio for casa in self._propiedades)

    def generar_informe_cartera(self) -> str:
        """Genera un informe textual resumen de la cartera.

        Incluye número de propiedades, valor total, desglose por estado
        y el listado breve de cada vivienda.

        Returns:
            Informe multilínea listo para imprimir o registrar.
        """
        lineas: list[str] = [
            "=== Informe de cartera inmobiliaria ===",
            f"Propiedades: {len(self._propiedades)}",
            f"Valor total: {self.calcular_valor_cartera():,.2f} €",
        ]

        conteo: Counter[str] = Counter(casa.estado.name for casa in self._propiedades)
        if conteo:
            lineas.append("Por estado:")
            for estado_nombre, cantidad in sorted(conteo.items()):
                lineas.append(f"  - {estado_nombre}: {cantidad}")
        else:
            lineas.append("Cartera vacía.")

        if self._propiedades:
            lineas.append("Detalle:")
            for indice, casa in enumerate(self._propiedades, start=1):
                lineas.append(f"  {indice}. {casa}")

        return "\n".join(lineas)
