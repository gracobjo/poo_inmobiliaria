# Estructura de carpetas

## Árbol del repositorio

```text
poo_inmobiliaria/
├── main.py                      # Entrada: UI gráfica o --demo
├── README.md                    # Visión general del proyecto
├── .gitignore
├── data/
│   ├── .gitkeep
│   └── inmobiliaria.db          # Creada en runtime (ignorada por git)
├── docs/                        # Esta documentación
├── ejemplos/
│   ├── __init__.py
│   └── demo_completa.py         # Demo pedagógica por consola
├── src/
│   ├── __init__.py
│   ├── modelos/                 # Dominio de negocio
│   │   ├── casa.py
│   │   ├── contrato.py
│   │   └── inquilino.py
│   ├── persistencia/            # SQLite
│   │   ├── database.py
│   │   └── repositorio.py
│   ├── servicios/               # Casos de uso / fachadas
│   │   ├── gestion_inmobiliaria.py
│   │   └── app_inmobiliaria.py
│   ├── ui/                      # Interfaz gráfica
│   │   └── app_grafica.py
│   └── utils/                   # Transversal
│       ├── constantes.py
│       └── validadores.py
└── tests/
    ├── test_casa.py
    └── test_contrato.py
```

## Responsabilidad por carpeta

| Carpeta | Capas | ¿Qué debe contener? | ¿Qué no debe contener? |
|---|---|---|---|
| `src/utils/` | Transversal | Enums, validadores puros | Lógica de negocio de casas |
| `src/modelos/` | Dominio | Entidades y reglas | SQL, widgets tkinter |
| `src/servicios/` | Aplicación | Orquestación y fachadas | Detalles de layout UI |
| `src/persistencia/` | Infraestructura | Esquema y CRUD SQLite | Reglas de AITP/IVA |
| `src/ui/` | Presentación | Pantallas y eventos | Consultas SQL directas |
| `ejemplos/` | Demo | Scripts didácticos | Persistencia de producción |
| `tests/` | Calidad | Pruebas del dominio | Dependencia de la UI |
| `data/` | Datos | Fichero SQLite local | Código fuente |
| `docs/` | Documentación | Manuales y UML | Lógica ejecutable |

## Dependencias entre capas

```text
ui ──────────► servicios (AppInmobiliaria)
                   │
                   ├──► gestion_inmobiliaria ──► modelos
                   └──► persistencia ──────────► modelos / utils
modelos ───────► utils
ejemplos ──────► modelos / servicios / utils
tests ─────────► modelos / utils
```

Regla: **las dependencias apuntan hacia dentro** (UI y persistencia dependen del dominio; el dominio no conoce la UI).

## Puntos de entrada

| Comando | Módulo | Resultado |
|---|---|---|
| `python main.py` | `src.ui.app_grafica` | App gráfica |
| `python main.py --demo` | `ejemplos.demo_completa` | Demo consola |
| `python -m unittest discover -s tests` | `tests.*` | Suite de tests |

## Base de datos

Ruta por defecto: `data/inmobiliaria.db`

Tablas:

- `casas` — inventario
- `clientes` — personas (inquilinos/interesados)
- `contratos` — alquiler vigente por casa
- `solicitudes` — interés del cliente (visita/compra/alquiler)
