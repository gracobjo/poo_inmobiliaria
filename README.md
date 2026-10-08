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
├── main.py                          # Punto de entrada
├── README.md
├── ejemplos/
│   └── demo_completa.py             # Demostración de todos los conceptos POO
├── src/
│   ├── __init__.py
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── casa.py                  # Clase Casa (núcleo del dominio)
│   │   ├── contrato.py              # Clase Contrato
│   │   └── inquilino.py             # Clase Inquilino
│   ├── servicios/
│   │   ├── __init__.py
│   │   └── gestion_inmobiliaria.py  # Gestión de cartera
│   └── utils/
│       ├── __init__.py
│       ├── constantes.py            # Enums EstadoCasa y TipoOperacion
│       └── validadores.py           # ValidadoresInmobiliarios
└── tests/
    ├── __init__.py
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

### Demo completa (recomendado)

```bash
python main.py
```

Equivale a ejecutar directamente:

```bash
python -m ejemplos.demo_completa
```

La demo muestra, en orden:

1. Creación de objetos y atributos de clase  
2. Reserva y venta con AITP  
3. Alquiler, contrato y regla del 35 %  
4. Decoración y reforma con IVA  
5. Cálculos de €/m², comparación de inversión y rentabilidad  
6. Informe de cartera  
7. Encapsulamiento y `try`/`except` ante datos inválidos  

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
