"""Normalización de claves y mapeo a modelos de dominio."""

from __future__ import annotations

from typing import Any

from src.modelos.casa import Casa
from src.modelos.inquilino import Inquilino


# alias (normalizado) -> campo canónico
_ALIAS_CASA: dict[str, str] = {
    "direccion": "direccion",
    "dirección": "direccion",
    "address": "direccion",
    "calle": "direccion",
    "dir": "direccion",
    "codigo_postal": "codigo_postal",
    "codigo postal": "codigo_postal",
    "código_postal": "codigo_postal",
    "código postal": "codigo_postal",
    "cp": "codigo_postal",
    "c.p.": "codigo_postal",
    "postal": "codigo_postal",
    "zip": "codigo_postal",
    "metros_cuadrados": "metros_cuadrados",
    "metros cuadrados": "metros_cuadrados",
    "m2": "metros_cuadrados",
    "m²": "metros_cuadrados",
    "superficie": "metros_cuadrados",
    "area": "metros_cuadrados",
    "precio": "precio",
    "price": "precio",
    "importe": "precio",
    "habitaciones": "habitaciones",
    "hab": "habitaciones",
    "rooms": "habitaciones",
    "dormitorios": "habitaciones",
    "localidad": "localidad",
    "ciudad": "localidad",
    "municipio": "localidad",
    "city": "localidad",
    "estado": "estado",
    "status": "estado",
    "tipo_vivienda": "tipo_vivienda",
    "tipo": "tipo_vivienda",
    "tipologia": "tipo_vivienda",
    "tipología": "tipo_vivienda",
    "type": "tipo_vivienda",
    "property_type": "tipo_vivienda",
    "id": "id",
}

_ALIAS_INQUILINO: dict[str, str] = {
    "nombre": "nombre",
    "name": "nombre",
    "dni": "dni",
    "nif": "dni",
    "documento": "dni",
    "telefono": "telefono",
    "teléfono": "telefono",
    "phone": "telefono",
    "tel": "telefono",
    "ingresos": "ingresos",
    "sueldo": "ingresos",
    "salary": "ingresos",
    "renta_ingresos": "ingresos",
}


def _normalizar_clave(clave: Any) -> str:
    texto = str(clave).strip().lower()
    texto = texto.replace("-", "_").replace(".", "")
    texto = " ".join(texto.split())
    return texto


def normalizar_registro(
    registro: dict[str, Any],
    alias: dict[str, str],
) -> dict[str, Any]:
    """Renombra claves de un registro según tabla de alias."""
    normalizado: dict[str, Any] = {}
    for clave, valor in registro.items():
        canonico = alias.get(_normalizar_clave(clave))
        if canonico is None:
            # conserva clave ya canónica si coincide
            clave_norm = _normalizar_clave(clave).replace(" ", "_")
            if clave_norm in alias.values():
                canonico = clave_norm
            else:
                continue
        if valor is None:
            continue
        if isinstance(valor, str):
            valor = valor.strip()
            if valor == "":
                continue
        normalizado[canonico] = valor
    return normalizado


def registro_a_casa(registro: dict[str, Any]) -> Casa:
    """Convierte un registro crudo en una instancia de ``Casa``."""
    datos = normalizar_registro(registro, _ALIAS_CASA)
    # Casa.desde_diccionario espera tipos coherentes; coerciona números.
    for campo in ("metros_cuadrados", "precio"):
        if campo in datos and isinstance(datos[campo], str):
            datos[campo] = float(datos[campo].replace(",", ".").replace(" ", ""))
    if "habitaciones" in datos and isinstance(datos["habitaciones"], str):
        datos["habitaciones"] = int(float(datos["habitaciones"].replace(",", ".")))
    if "id" in datos and datos["id"] is not None and not isinstance(datos["id"], int):
        try:
            datos["id"] = int(datos["id"])
        except (TypeError, ValueError):
            datos.pop("id", None)
    return Casa.desde_diccionario(datos)


def registro_a_inquilino(registro: dict[str, Any]) -> Inquilino:
    """Convierte un registro crudo en una instancia de ``Inquilino``."""
    datos = normalizar_registro(registro, _ALIAS_INQUILINO)
    obligatorias = ("nombre", "dni", "telefono", "ingresos")
    faltantes = [c for c in obligatorias if c not in datos]
    if faltantes:
        raise ValueError(f"Faltan campos de inquilino: {', '.join(faltantes)}.")
    ingresos = datos["ingresos"]
    if isinstance(ingresos, str):
        ingresos = float(ingresos.replace(",", ".").replace(" ", ""))
    return Inquilino(
        nombre=str(datos["nombre"]),
        dni=str(datos["dni"]),
        telefono=str(datos["telefono"]),
        ingresos=float(ingresos),
    )
