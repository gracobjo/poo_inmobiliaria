# Catálogo de clases

## Resumen

| Clase | Módulo | Rol |
|---|---|---|
| `EstadoCasa` | `utils/constantes.py` | Enum de estado de vivienda |
| `TipoOperacion` | `utils/constantes.py` | Enum de operaciones |
| `ValidadoresInmobiliarios` | `utils/validadores.py` | Validaciones estáticas |
| `Inquilino` | `modelos/inquilino.py` | Cliente / inquilino |
| `Contrato` | `modelos/contrato.py` | Contrato de alquiler |
| `Casa` | `modelos/casa.py` | Vivienda (núcleo) |
| `GestionInmobiliaria` | `servicios/gestion_inmobiliaria.py` | Cartera en memoria |
| `Database` | `persistencia/database.py` | Conexión y esquema SQLite |
| `RepositorioInmobiliario` | `persistencia/repositorio.py` | Persistencia CRUD |
| `AppInmobiliaria` | `servicios/app_inmobiliaria.py` | Fachada dominio + BD |
| `AppGrafica` | `ui/app_grafica.py` | Ventana tkinter |

---

## `EstadoCasa` / `TipoOperacion`

**EstadoCasa:** `DISPONIBLE`, `RESERVADA`, `VENDIDA`, `ALQUILADA`, `EN_REFORMA`

**TipoOperacion:** `VENTA`, `ALQUILER`, `REFORMA`, `DECORACION`

---

## `ValidadoresInmobiliarios`

Métodos estáticos:

| Método | Comprueba |
|---|---|
| `es_positivo(valor)` | Número > 0 |
| `es_string_no_vacio(texto)` | Cadena con contenido |
| `es_cp_valido(cp)` | CP español 01000–52999 |
| `es_fecha_valida(fecha)` | `date`/`datetime`/string ISO |

---

## `Inquilino`

| Miembro | Tipo | Notas |
|---|---|---|
| `nombre` | `str` | Público |
| `_dni` / `dni` | `str` | Privado, property solo lectura |
| `telefono` | `str` | Público |
| `_ingresos` / `ingresos` | `float` | Property con setter validado |

**Métodos**

- `puede_alquilar(renta_mensual) -> bool` — regla del **35 %** (`renta <= ingresos * 0.35`)

---

## `Contrato`

Atributos encapsulados (properties): `inquilino`, `fecha_inicio`, `fecha_fin`, `renta`, `fianza`

| Método | Descripción |
|---|---|
| `calcular_total_pagado(hasta=None)` | Fianza + renta × meses completos |
| `esta_vigente(en_fecha=None)` | `inicio <= fecha <= fin` |

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
| `reservar()` | `DISPONIBLE` → `RESERVADA` |
| `liberar()` | `RESERVADA`/`ALQUILADA` → `DISPONIBLE` |
| `comprar()` | Aplica AITP; estado `VENDIDA` |
| `alquilar(...)` | Crea `Contrato`; estado `ALQUILADA` |
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
| `generar_informe_cartera()` | Texto resumen |

---

## `Database`

- Abre/crea fichero SQLite
- Crea tablas (`casas`, `clientes`, `contratos`, `solicitudes`)
- Expone `conexion` y `cerrar()`

---

## `RepositorioInmobiliario`

Traduce objetos ↔ filas:

- Casas: `listar_casas`, `guardar_casa`, `eliminar_casa`
- Clientes: `guardar_cliente`, `obtener_cliente_por_dni`
- Solicitudes: `crear_solicitud`, `listar_solicitudes`, `actualizar_estado_solicitud`
- Contratos: sincronizados al guardar una casa alquilada

---

## `AppInmobiliaria`

Fachada usada por la UI.

| Método | Descripción |
|---|---|
| `cargar()` | Recarga cartera desde BD |
| `agregar_casa(casa)` | Memoria + SQLite |
| `sincronizar(casa)` | Persiste cambios y recarga |
| `obtener_casa(id)` | Búsqueda por id |
| `crear_solicitud(...)` | Interés del cliente |
| `listar_solicitudes(...)` | Bandeja del agente |
| `atender_solicitud(id)` | Marca `ATENDIDA` |
| `_sembrar_datos()` | Inventario inicial si BD vacía |

---

## `AppGrafica` (UI)

Hereda de `tk.Tk`.

Responsabilidades:

1. Pantalla de selección de perfil
2. Panel Agente (tabla + acciones)
3. Panel Cliente (perfil, filtros, solicitudes)
4. Estilos visuales y diálogos

Métodos clave: `_mostrar_inicio`, `_mostrar_agente`, `_mostrar_cliente`, `_cliente_solicitud`, `_agente_*`.
