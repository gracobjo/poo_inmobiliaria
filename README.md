# Sistema Inmobiliario POO

Proyecto educativo en **Python 3.14+** que modela la gestión de una inmobiliaria mediante **Programación Orientada a Objetos**: viviendas, inquilinos, contratos de alquiler y un servicio de cartera.

El sistema permite dar de alta propiedades, venderlas (con impuesto AITP), alquilarlas (regla del 35 % de ingresos), aplicar mejoras (decoración y reforma con IVA), calcular rentabilidad y generar informes.

---

## Conceptos POO aplicados

| Concepto | Dónde se aplica | Descripción breve |
|---|---|---|
| **Clase / objeto** | `Casa`, `Inquilino`, `Contrato`, `GestionInmobiliaria` | Modelan entidades del dominio inmobiliario |
| **Encapsulamiento** | `_dni`, `_precio`, `_estado`, `_propiedades` | Atributos privados expuestos con *properties* |
| **Properties** | `Casa.precio`, `Inquilino.dni`, `Contrato.renta` | Lectura controlada (y escritura validada cuando procede) |
| **Métodos de instancia** | `comprar()`, `alquilar()`, `decorar()`, `reformar()` | Operan sobre el estado de un objeto concreto |
| **Métodos de clase** | `Casa.desde_diccionario()`, `Casa.cambiar_impuesto_aitp()` | Reciben `cls` y afectan a la clase o fabrican instancias |
| **Métodos estáticos** | `Casa.calcular_precio_m2()`, `Casa.comparar_inversion()` | Utilidades sin acceso a `self` ni `cls` |
| **Atributos de clase** | `total_casas`, `impuesto_aitp`, `iva_reforma` | Estado compartido por todas las viviendas |
| **Enumeraciones** | `EstadoCasa`, `TipoOperacion` | Conjuntos cerrados de valores de dominio |
| **Validación / excepciones** | `ValidadoresInmobiliarios` + `ValueError` | Invariantes del dominio con errores explícitos |
| **Colaboración entre objetos** | `Casa` ↔ `Inquilino` ↔ `Contrato` | El alquiler crea un contrato ligado a un inquilino |
| **Servicio de aplicación** | `GestionInmobiliaria` | Orquesta la cartera sin mezclarse con el modelo |
| **Tests unitarios** | `tests/test_casa.py`, `tests/test_contrato.py` | Verifican comportamiento con `unittest` |

---

## Estructura del proyecto

```text
poo_inmobiliaria/
├── main.py                          # Punto de entrada (UI gráfica)
├── README.md
├── data/                            # SQLite (inmobiliaria.db)
├── ejemplos/
│   └── demo_completa.py             # Demo por consola (--demo)
├── src/
│   ├── modelos/                     # Casa, Contrato, Inquilino
│   ├── persistencia/                # SQLite (Database + Repositorio)
│   ├── servicios/                   # GestionInmobiliaria + AppInmobiliaria
│   ├── ui/                          # Interfaz tkinter Agente/Cliente
│   └── utils/                       # Enums y validadores
└── tests/
    ├── test_casa.py
    └── test_contrato.py
```

---

## Requisitos

- **Python 3.14+**
- Sin dependencias externas (solo biblioteca estándar)

---

## Instrucciones de ejecución

Desde la raíz del proyecto (`poo_inmobiliaria/`):

### Interfaz gráfica Agente / Cliente (recomendado)

```bash
python main.py
```

Se abre una ventana tkinter con dos perfiles:

| Perfil | Puede hacer |
|---|---|
| **Agente** | Alta de viviendas, reserva, venta, alquiler, reformas, informe y gestión de solicitudes |
| **Cliente** | Buscar disponibles, ver detalle, solicitar visita/compra/alquiler y comprobar la regla del 35 % |

Los datos se guardan en `data/inmobiliaria.db` (SQLite). La primera ejecución crea un inventario de ejemplo.

### Demo por consola

```bash
python main.py --demo
```

### Tests unitarios

```bash
python -m unittest discover -s tests -v
```

---

## Reglas de negocio destacadas

| Regla | Detalle |
|---|---|
| **AITP** | Impuesto sobre el precio en la compra (`Casa.impuesto_aitp`, por defecto 10 %) |
| **IVA reforma** | Se aplica al coste de reforma (`Casa.iva_reforma`, por defecto 21 %) |
| **Regla del 35 %** | La renta mensual no puede superar el 35 % de los ingresos del inquilino |
| **Rentabilidad bruta** | `(renta_mensual × 12 / precio) × 100` |
| **Estados** | `DISPONIBLE`, `RESERVADA`, `VENDIDA`, `ALQUILADA`, `EN_REFORMA` |

---

## Ejemplo rápido de uso

```python
from datetime import date
from src.modelos.casa import Casa
from src.modelos.inquilino import Inquilino
from src.servicios.gestion_inmobiliaria import GestionInmobiliaria

gestion = GestionInmobiliaria()
casa = Casa("Calle Mayor 1", "28013", 80, 200_000, 3, localidad="Madrid")
gestion.agregar_propiedad(casa)

inquilino = Inquilino("Ana López", "12345678Z", "600111222", 3_000)
casa.alquilar(inquilino, renta=900, fianza=1_800, fecha_inicio=date(2026, 1, 1))

print(gestion.generar_informe_cartera())
```

---

## Autoría

Proyecto académico de demostración de POO en Python — *Sistema Inmobiliario POO*.
