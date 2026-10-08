"""Modelo de vivienda del Sistema Inmobiliario POO."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from src.modelos.contrato import Contrato
from src.modelos.inquilino import Inquilino
from src.utils.constantes import EstadoCasa, TipoOperacion
from src.utils.validadores import ValidadoresInmobiliarios


class Casa:
    """Vivienda del inventario inmobiliario con encapsulamiento completo.

    Combina atributos de instancia (dirección, precio, estado, etc.) con
    atributos de clase compartidos (contador global, AITP e IVA de reforma).
    Las operaciones de negocio cambian el estado y, cuando corresponde,
    actualizan el precio o generan un contrato de alquiler.

    Attributes de clase:
        total_casas: Contador de instancias creadas.
        impuesto_aitp: Tipo impositivo AITP aplicado en compras (0–1).
        iva_reforma: IVA aplicado a reformas (0–1).
    """

    total_casas: int = 0
    impuesto_aitp: float = 0.10
    iva_reforma: float = 0.21

    def __init__(
        self,
        direccion: str,
        codigo_postal: str,
        metros_cuadrados: float,
        precio: float,
        habitaciones: int,
        estado: EstadoCasa = EstadoCasa.DISPONIBLE,
        localidad: str = "",
        id: int | None = None,
    ) -> None:
        """Crea una vivienda e incrementa el contador global.

        Args:
            direccion: Dirección postal (no vacía).
            codigo_postal: Código postal español válido.
            metros_cuadrados: Superficie útil (> 0).
            precio: Precio de venta o valor de referencia (> 0).
            habitaciones: Número de habitaciones (>= 1).
            estado: Estado inicial (por defecto ``DISPONIBLE``).
            localidad: Municipio o localidad (opcional).
            id: Identificador de persistencia (SQLite), opcional.

        Raises:
            ValueError: Si algún dato no supera la validación.
            TypeError: Si ``estado`` no es un ``EstadoCasa``.
        """
        if not ValidadoresInmobiliarios.es_string_no_vacio(direccion):
            raise ValueError("La dirección no puede estar vacía.")
        if not ValidadoresInmobiliarios.es_cp_valido(codigo_postal):
            raise ValueError("El código postal no es válido.")
        if not ValidadoresInmobiliarios.es_positivo(metros_cuadrados):
            raise ValueError("Los metros cuadrados deben ser un número positivo.")
        if not ValidadoresInmobiliarios.es_positivo(precio):
            raise ValueError("El precio debe ser un número positivo.")
        if not isinstance(habitaciones, int) or isinstance(habitaciones, bool) or habitaciones < 1:
            raise ValueError("El número de habitaciones debe ser un entero >= 1.")
        if not isinstance(estado, EstadoCasa):
            raise TypeError("El estado debe ser un valor de EstadoCasa.")
        if not isinstance(localidad, str):
            raise TypeError("La localidad debe ser una cadena.")
        if id is not None and (not isinstance(id, int) or isinstance(id, bool) or id < 1):
            raise ValueError("El id de persistencia debe ser un entero >= 1.")

        self._id: int | None = id
        self._direccion: str = direccion.strip()
        self._codigo_postal: str = codigo_postal.strip()
        self._metros_cuadrados: float = float(metros_cuadrados)
        self._precio: float = float(precio)
        self._habitaciones: int = habitaciones
        self._estado: EstadoCasa = estado
        self._localidad: str = localidad.strip()
        self._contrato: Contrato | None = None
        self._historial_operaciones: list[TipoOperacion] = []

        Casa.total_casas += 1

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def id(self) -> int | None:
        """Identificador de persistencia en SQLite, si existe."""
        return self._id

    @id.setter
    def id(self, valor: int | None) -> None:
        """Asigna el id tras insertar en base de datos."""
        if valor is not None and (not isinstance(valor, int) or isinstance(valor, bool) or valor < 1):
            raise ValueError("El id de persistencia debe ser un entero >= 1.")
        self._id = valor

    @property
    def direccion(self) -> str:
        """Dirección de la vivienda."""
        return self._direccion

    @property
    def codigo_postal(self) -> str:
        """Código postal de la vivienda."""
        return self._codigo_postal

    @property
    def localidad(self) -> str:
        """Municipio o localidad de la vivienda."""
        return self._localidad

    @property
    def metros_cuadrados(self) -> float:
        """Superficie útil en metros cuadrados."""
        return self._metros_cuadrados

    @property
    def precio(self) -> float:
        """Precio de referencia en euros."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """Actualiza el precio de la vivienda.

        Args:
            valor: Nuevo precio (> 0).

        Raises:
            ValueError: Si el valor no es positivo.
        """
        if not ValidadoresInmobiliarios.es_positivo(valor):
            raise ValueError("El precio debe ser un número positivo.")
        self._precio = float(valor)

    @property
    def habitaciones(self) -> int:
        """Número de habitaciones."""
        return self._habitaciones

    @property
    def estado(self) -> EstadoCasa:
        """Estado comercial/físico actual."""
        return self._estado

    @property
    def contrato(self) -> Contrato | None:
        """Contrato de alquiler asociado, si existe."""
        return self._contrato

    @property
    def historial_operaciones(self) -> list[TipoOperacion]:
        """Copia del historial de operaciones realizadas."""
        return list(self._historial_operaciones)

    @property
    def precio_m2(self) -> float:
        """Precio por metro cuadrado de esta vivienda."""
        return Casa.calcular_precio_m2(self._precio, self._metros_cuadrados)

    # ------------------------------------------------------------------
    # Métodos de instancia
    # ------------------------------------------------------------------

    def reservar(self) -> None:
        """Marca la vivienda como reservada.

        Raises:
            ValueError: Si la vivienda no está disponible.
        """
        if self._estado != EstadoCasa.DISPONIBLE:
            raise ValueError(
                f"No se puede reservar una vivienda en estado {self._estado.name}."
            )
        self._estado = EstadoCasa.RESERVADA

    def liberar(self) -> None:
        """Libera la vivienda (reserva o alquiler) y la deja disponible.

        Raises:
            ValueError: Si el estado no es ``RESERVADA`` ni ``ALQUILADA``.
        """
        if self._estado not in (EstadoCasa.RESERVADA, EstadoCasa.ALQUILADA):
            raise ValueError(
                f"No se puede liberar una vivienda en estado {self._estado.name}."
            )
        self._contrato = None
        self._estado = EstadoCasa.DISPONIBLE

    def calcular_rentabilidad(self, renta_mensual: float) -> float:
        """Calcula la rentabilidad bruta anual en porcentaje.

        Fórmula: ``(renta_mensual * 12 / precio) * 100``.

        Args:
            renta_mensual: Renta mensual estimada o de contrato (> 0).

        Returns:
            Rentabilidad bruta anual expresada en tanto por ciento.

        Raises:
            ValueError: Si ``renta_mensual`` no es positiva.
        """
        if not ValidadoresInmobiliarios.es_positivo(renta_mensual):
            raise ValueError("La renta mensual debe ser un número positivo.")
        return (float(renta_mensual) * 12 / self._precio) * 100

    def comprar(self) -> float:
        """Ejecuta la compra de la vivienda aplicando el impuesto AITP.

        Returns:
            Precio final con AITP incluido.

        Raises:
            ValueError: Si la vivienda no está disponible para venta.
        """
        if self._estado not in (EstadoCasa.DISPONIBLE, EstadoCasa.RESERVADA):
            raise ValueError(
                f"No se puede comprar una vivienda en estado {self._estado.name}."
            )

        precio_final: float = self._precio * (1 + Casa.impuesto_aitp)
        self._estado = EstadoCasa.VENDIDA
        self._contrato = None
        self._historial_operaciones.append(TipoOperacion.VENTA)
        return precio_final

    def alquilar(
        self,
        inquilino: Inquilino,
        renta: float,
        fianza: float,
        fecha_inicio: date | None = None,
        meses: int = 12,
    ) -> Contrato:
        """Alquila la vivienda a un inquilino generando un contrato.

        Args:
            inquilino: Solicitante del alquiler.
            renta: Renta mensual (> 0).
            fianza: Fianza (>= 0).
            fecha_inicio: Inicio del contrato (por defecto hoy).
            meses: Duración en meses (>= 1).

        Returns:
            Contrato de alquiler creado.

        Raises:
            ValueError: Si el estado no permite alquilar, el inquilino
                no supera la regla del 35 % o los parámetros son inválidos.
            TypeError: Si ``inquilino`` no es un ``Inquilino``.
        """
        if not isinstance(inquilino, Inquilino):
            raise TypeError("El inquilino debe ser una instancia de Inquilino.")
        if self._estado != EstadoCasa.DISPONIBLE:
            raise ValueError(
                f"No se puede alquilar una vivienda en estado {self._estado.name}."
            )
        if not isinstance(meses, int) or isinstance(meses, bool) or meses < 1:
            raise ValueError("La duración del contrato debe ser un entero >= 1.")
        if not inquilino.puede_alquilar(renta):
            raise ValueError(
                "El inquilino no puede alquilar: la renta supera el 35 % de sus ingresos."
            )

        inicio: date = fecha_inicio if fecha_inicio is not None else date.today()
        if not ValidadoresInmobiliarios.es_fecha_valida(inicio):
            raise ValueError("La fecha de inicio del alquiler no es válida.")

        # Aproximación de fin: inicio + meses (mismo día del mes cuando sea posible).
        mes_fin: int = inicio.month - 1 + meses
        anio_fin: int = inicio.year + mes_fin // 12
        mes_fin = mes_fin % 12 + 1
        dia_fin: int = min(inicio.day, _dias_en_mes(anio_fin, mes_fin))
        fin: date = date(anio_fin, mes_fin, dia_fin)
        if fin <= inicio:
            fin = inicio + timedelta(days=30 * meses)

        contrato: Contrato = Contrato(
            inquilino=inquilino,
            fecha_inicio=inicio,
            fecha_fin=fin,
            renta=renta,
            fianza=fianza,
        )
        self._contrato = contrato
        self._estado = EstadoCasa.ALQUILADA
        self._historial_operaciones.append(TipoOperacion.ALQUILER)
        return contrato

    def decorar(self, coste: float) -> float:
        """Registra un servicio de decoración sobre la vivienda.

        Args:
            coste: Coste base del servicio (> 0).

        Returns:
            Coste total del servicio (sin IVA de reforma).

        Raises:
            ValueError: Si el coste no es positivo o la vivienda está vendida.
        """
        if self._estado == EstadoCasa.VENDIDA:
            raise ValueError("No se puede decorar una vivienda ya vendida.")
        if not ValidadoresInmobiliarios.es_positivo(coste):
            raise ValueError("El coste de decoración debe ser un número positivo.")

        coste_total: float = float(coste)
        self._precio += coste_total
        self._historial_operaciones.append(TipoOperacion.DECORACION)
        return coste_total

    def reformar(self, coste: float) -> float:
        """Ejecuta una reforma aplicando el IVA configurado en la clase.

        Args:
            coste: Coste base de la reforma (> 0).

        Returns:
            Coste total con IVA incluido.

        Raises:
            ValueError: Si el coste no es positivo o la vivienda está
                vendida o ya en reforma.
        """
        if self._estado in (EstadoCasa.VENDIDA, EstadoCasa.EN_REFORMA):
            raise ValueError(
                f"No se puede reformar una vivienda en estado {self._estado.name}."
            )
        if not ValidadoresInmobiliarios.es_positivo(coste):
            raise ValueError("El coste de reforma debe ser un número positivo.")

        coste_total: float = float(coste) * (1 + Casa.iva_reforma)
        self._precio += coste_total
        self._estado = EstadoCasa.EN_REFORMA
        self._contrato = None
        self._historial_operaciones.append(TipoOperacion.REFORMA)
        return coste_total

    def finalizar_reforma(self) -> None:
        """Marca la reforma como terminada y deja la casa disponible.

        Raises:
            ValueError: Si la vivienda no está en reforma.
        """
        if self._estado != EstadoCasa.EN_REFORMA:
            raise ValueError("La vivienda no está en reforma.")
        self._estado = EstadoCasa.DISPONIBLE

    def restaurar_historial(self, operaciones: list[TipoOperacion]) -> None:
        """Restaura el historial desde persistencia (uso interno/repositorio)."""
        self._historial_operaciones = list(operaciones)

    def asociar_contrato(self, contrato: Contrato | None) -> None:
        """Asocia o limpia el contrato cargado desde persistencia."""
        self._contrato = contrato

    # ------------------------------------------------------------------
    # Métodos de clase
    # ------------------------------------------------------------------

    @classmethod
    def desde_diccionario(cls, datos: dict[str, Any]) -> Casa:
        """Construye una ``Casa`` a partir de un diccionario de datos.

        Claves esperadas: ``direccion``, ``codigo_postal``, ``metros_cuadrados``,
        ``precio``, ``habitaciones``. Opcional: ``estado`` (nombre del enum
        o instancia de ``EstadoCasa``) y ``localidad``.

        Args:
            datos: Diccionario con los atributos de la vivienda.

        Returns:
            Nueva instancia de ``Casa``.

        Raises:
            ValueError: Si faltan claves obligatorias o el estado es inválido.
            TypeError: Si ``datos`` no es un diccionario.
        """
        if not isinstance(datos, dict):
            raise TypeError("Los datos deben proporcionarse como diccionario.")

        obligatorias: tuple[str, ...] = (
            "direccion",
            "codigo_postal",
            "metros_cuadrados",
            "precio",
            "habitaciones",
        )
        faltantes: list[str] = [clave for clave in obligatorias if clave not in datos]
        if faltantes:
            raise ValueError(f"Faltan claves obligatorias: {', '.join(faltantes)}.")

        estado_raw: Any = datos.get("estado", EstadoCasa.DISPONIBLE)
        if isinstance(estado_raw, EstadoCasa):
            estado: EstadoCasa = estado_raw
        elif isinstance(estado_raw, str):
            try:
                estado = EstadoCasa[estado_raw.strip().upper()]
            except KeyError as exc:
                raise ValueError(f"Estado desconocido: {estado_raw!r}.") from exc
        else:
            raise ValueError("El estado debe ser un EstadoCasa o su nombre.")

        return cls(
            direccion=datos["direccion"],
            codigo_postal=datos["codigo_postal"],
            metros_cuadrados=datos["metros_cuadrados"],
            precio=datos["precio"],
            habitaciones=datos["habitaciones"],
            estado=estado,
            localidad=str(datos.get("localidad", "")),
            id=datos.get("id"),
        )

    @classmethod
    def cambiar_impuesto_aitp(cls, nuevo_impuesto: float) -> None:
        """Actualiza el tipo impositivo AITP de la clase.

        Args:
            nuevo_impuesto: Nuevo tipo en rango [0, 1] (p. ej. 0.10 = 10 %).

        Raises:
            ValueError: Si el valor está fuera de [0, 1].
        """
        if (
            not isinstance(nuevo_impuesto, (int, float))
            or isinstance(nuevo_impuesto, bool)
            or not 0 <= float(nuevo_impuesto) <= 1
        ):
            raise ValueError("El impuesto AITP debe estar en el intervalo [0, 1].")
        cls.impuesto_aitp = float(nuevo_impuesto)

    # ------------------------------------------------------------------
    # Métodos estáticos
    # ------------------------------------------------------------------

    @staticmethod
    def calcular_precio_m2(precio: float, metros_cuadrados: float) -> float:
        """Calcula el precio por metro cuadrado.

        Args:
            precio: Precio total en euros (> 0).
            metros_cuadrados: Superficie en m² (> 0).

        Returns:
            Precio €/m².

        Raises:
            ValueError: Si alguno de los valores no es positivo.
        """
        if not ValidadoresInmobiliarios.es_positivo(precio):
            raise ValueError("El precio debe ser un número positivo.")
        if not ValidadoresInmobiliarios.es_positivo(metros_cuadrados):
            raise ValueError("Los metros cuadrados deben ser un número positivo.")
        return float(precio) / float(metros_cuadrados)

    @staticmethod
    def comparar_inversion(casa_a: Casa, casa_b: Casa) -> Casa:
        """Compara dos viviendas y devuelve la de menor precio por m².

        Args:
            casa_a: Primera vivienda.
            casa_b: Segunda vivienda.

        Returns:
            La vivienda con mejor ratio precio/m² (menor €/m²).
            En empate, se devuelve ``casa_a``.

        Raises:
            TypeError: Si alguno de los argumentos no es una ``Casa``.
        """
        if not isinstance(casa_a, Casa) or not isinstance(casa_b, Casa):
            raise TypeError("Ambos argumentos deben ser instancias de Casa.")

        if casa_a.precio_m2 <= casa_b.precio_m2:
            return casa_a
        return casa_b

    def __repr__(self) -> str:
        return (
            f"Casa(direccion={self._direccion!r}, codigo_postal={self._codigo_postal!r}, "
            f"localidad={self._localidad!r}, metros_cuadrados={self._metros_cuadrados!r}, "
            f"precio={self._precio!r}, habitaciones={self._habitaciones!r}, "
            f"estado={self._estado!r})"
        )

    def __str__(self) -> str:
        localidad_txt: str = f", {self._localidad}" if self._localidad else ""
        return (
            f"{self._direccion} ({self._codigo_postal}{localidad_txt}) — "
            f"{self._metros_cuadrados:.0f} m², {self._habitaciones} hab., "
            f"{self._precio:,.2f} € [{self._estado.name}]"
        )


def _dias_en_mes(anio: int, mes: int) -> int:
    """Devuelve el número de días del mes indicado."""
    if mes == 12:
        siguiente: date = date(anio + 1, 1, 1)
    else:
        siguiente = date(anio, mes + 1, 1)
    return (siguiente - timedelta(days=1)).day
