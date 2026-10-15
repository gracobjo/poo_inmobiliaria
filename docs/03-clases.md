# Catálogo de clases

## Resumen

| Clase | Módulo | Rol |
|---|---|---|
| `EstadoCasa` | `utils/constantes.py` | Enum de estado de vivienda |
| `TipoOperacion` | `utils/constantes.py` | Enum de operaciones (incl. `RESOLUCION`) |
| `IniciativaResolucion` | `utils/constantes.py` | Quién solicita la baja del contrato |
| `CausaResolucion` | `utils/constantes.py` | Causas LAU de resolución |
| `ValidadoresInmobiliarios` | `utils/validadores.py` | Validaciones estáticas |
| `Inquilino` | `modelos/inquilino.py` | Cliente / inquilino |
| `Contrato` / `ResolucionContrato` | `modelos/contrato.py` | Contrato y baja formal |
| `Reserva` | `modelos/reserva.py` | Reserva con cliente y fecha |
| `Casa` | `modelos/casa.py` | Vivienda (núcleo) |
| `GestionInmobiliaria` | `servicios/gestion_inmobiliaria.py` | Cartera en memoria |
| `Database` | `persistencia/database.py` | Conexión y esquema SQLite |
| `RepositorioInmobiliario` | `persistencia/repositorio.py` | Persistencia CRUD |
| `AppInmobiliaria` | `servicios/app_inmobiliaria.py` | Fachada dominio + BD |
| `AppGrafica` | `ui/app_grafica.py` | Ventana tkinter |

---

## `EstadoCasa` / `TipoOperacion`

**EstadoCasa:** `DISPONIBLE`, `RESERVADA`, `VENDIDA`, `ALQUILADA`, `EN_REFORMA`

**TipoOperacion:** `VENTA`, `ALQUILER`, `REFORMA`, `DECORACION`, `RESERVA`, `RESOLUCION`

**IniciativaResolucion:** `ARRENDADOR`, `ARRENDATARIO`, `AJENA`

**CausaResolucion:** causas tipadas (impagos, desistimiento, mutuo acuerdo, etc.) con `descripcion`, `iniciativa` y `para_iniciativa(...)`.

---

## `ValidadoresInmobiliarios`

Métodos estáticos:

| Método | Comprueba |
|---|---|
| `es_positivo(valor)` | Número > 0 |
| `es_string_no_vacio(texto)` | Cadena con contenido |
| `es_cp_valido(cp)` | CP español 01000–52999 |
| `es_fecha_valida(fecha)` | `date`/`datetime`/string ISO |
| `parsear_importe(texto)` | Euros en formato ES/EN (`250.000`, `250,000`, `250k`…) |

---

## `Inquilino`

| Miembro | Tipo | Notas |
|---|---|---|
| `nombre` | `str` | Público |
| `_dni` / `dni` | `str` | Privado, property solo lectura |
| `telefono` | `str` | Público |
| `_ingresos` / `ingresos` | `float` | Property con setter validado |
| `tope_renta` | `float` | `ingresos * 0.35` (solo lectura) |

**Métodos**

- `puede_alquilar(renta_mensual, renta_ya_comprometida=0) -> bool` — regla del **35 % acumulada**  
  (`renta + comprometida <= ingresos * 0.35`)

---

## `Contrato` / `ResolucionContrato`

Atributos encapsulados (properties): `inquilino`, `fecha_inicio`, `fecha_fin`, `renta`, `fianza`

| Método | Descripción |
|---|---|
| `calcular_total_pagado(hasta=None)` | Fianza + renta × meses completos |
| `esta_vigente(en_fecha=None)` | `inicio <= fecha <= fin` |
| `meses_transcurridos(en_fecha=None)` | Meses completos desde el inicio |
| `preparar_resolucion(causa, iniciativa, ...)` | Valida causa/plazos y devuelve `ResolucionContrato` |

`ResolucionContrato` (dataclass inmutable): causa, iniciativa, fecha, observaciones y snapshot del contrato.

---

## `Reserva`

Dataclass inmutable: `cliente` (`Inquilino`) + `fecha` (`datetime`).

Se asocia a una vivienda en estado `RESERVADA` y se limpia al liberar, comprar o alquilar.

---

## `Casa`

### Atributos de clase

| Atributo | Default | Uso |
|---|---|---|
| `total_casas` | `0` | Contador de instancias |
| `impuesto_aitp` | `0.10` | Impuesto en compra |
| `iva_reforma` | `0.21` | IVA en reformas |

### Atributos de instancia (principales)

`id`, `direccion`, `codigo_postal`, `localidad`, `metros_cuadrados`, `precio`, `habitaciones`, `estado`, `contrato`, `historial_operaciones`, `precio_m2`

### Métodos de instancia

| Método | Efecto |
|---|---|
| `reservar(cliente, fecha=None)` | `DISPONIBLE` → `RESERVADA` + `Reserva` |
| `liberar()` | `RESERVADA`/`ALQUILADA` → `DISPONIBLE` (limpia reserva/contrato) |
| `comprar()` | Aplica AITP; estado `VENDIDA` |
| `alquilar(..., renta_ya_comprometida=0)` | Crea `Contrato`; estado `ALQUILADA` (35 % acumulado) |
| `resolver_contrato(causa, iniciativa, ...)` | Baja formal; estado `DISPONIBLE` + `RESOLUCION` |
| `decorar(coste)` | Suma coste al precio |
| `reformar(coste)` | Suma coste+IVA; estado `EN_REFORMA` |
| `finalizar_reforma()` | `EN_REFORMA` → `DISPONIBLE` |
| `calcular_rentabilidad(renta)` | % bruto anual |

### Métodos de clase / estáticos

| Método | Tipo | Uso |
|---|---|---|
| `desde_diccionario(datos)` | classmethod | Factory |
| `cambiar_impuesto_aitp(x)` | classmethod | Configura AITP |
| `calcular_precio_m2(p, m2)` | staticmethod | €/m² |
| `comparar_inversion(a, b)` | staticmethod | Menor €/m² |

### Persistencia auxiliar

- `restaurar_historial(ops)`
- `asociar_contrato(contrato)`
- `asociar_reserva(reserva)`

---

## `GestionInmobiliaria`

Lista privada `_propiedades`.

| Método | Descripción |
|---|---|
| `agregar_propiedad(casa)` | Alta en cartera |
| `listar_disponibles()` | Filtro `DISPONIBLE` |
| `listar_por_localidad(loc)` | Filtro por municipio |
| `buscar_por_precio(min, max)` | Rango de precios |
| `calcular_valor_cartera()` | Suma de precios |
| `generar_informe_cartera()` | Texto resumen (incluye cliente/fecha en reservas) |

---

## `Database`

- Abre/crea fichero SQLite
- Crea tablas (`casas`, `clientes`, `contratos`, `solicitudes`, `resoluciones_contrato`, `reservas`)
- Expone `conexion` y `cerrar()`

---

## `RepositorioInmobiliario`

Traduce objetos ↔ filas:

- Casas: `listar_casas`, `guardar_casa`, `eliminar_casa`
- Clientes: `guardar_cliente`, `obtener_cliente_por_dni`
- Solicitudes: `crear_solicitud`, `listar_solicitudes`, `actualizar_estado_solicitud`
- Contratos: sincronizados al guardar una casa alquilada
- Reservas: sincronizadas al guardar una casa reservada
- Resoluciones: `registrar_resolucion`, `listar_resoluciones`

---

## `AppInmobiliaria`

Fachada usada por la UI.

| Método | Descripción |
|---|---|
| `cargar()` | Recarga cartera desde BD |
| `agregar_casa(casa)` | Memoria + SQLite |
| `sincronizar(casa)` | Persiste cambios y recarga |
| `obtener_casa(id)` | Búsqueda por id |
| `guardar_cliente` / `obtener_cliente_por_dni` | Perfil de cliente en SQLite |
| `listar_contratos()` | Pares `(casa, contrato)` vigentes |
| `renta_comprometida(dni)` | Suma de rentas vigentes del DNI |
| `resolver_contrato(...)` | Baja formal + historial + sincronizar |
| `listar_resoluciones(...)` | Historial de bajas |
| `crear_solicitud(...)` | Interés del cliente |
| `listar_solicitudes(...)` | Bandeja del agente |
| `atender_solicitud(id)` | Marca `ATENDIDA` |
| `_sembrar_datos()` | Inventario inicial si BD vacía |

---

## `AppGrafica` (UI)

Hereda de `tk.Tk`.

Responsabilidades:

1. Pantalla de selección de perfil
2. Panel Agente (tabla + acciones, contratos y resoluciones)
3. Panel Cliente (perfil cargar/guardar, filtros, contratos, solicitudes)
4. Estilos visuales, tarjetas de contrato y diálogos de baja

Métodos clave: `_mostrar_inicio`, `_mostrar_agente`, `_mostrar_cliente`, `_cliente_cargar_perfil`, `_cliente_mis_contratos`, `_dialogo_resolver_contrato`, `_agente_*`.
