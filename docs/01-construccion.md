# Cómo se ha construido la aplicación

## Objetivo

El **Sistema Inmobiliario POO** es una aplicación educativa y operativa básica que modela una inmobiliaria con Programación Orientada a Objetos en Python. Sirve a dos perfiles:

- **Agente:** gestiona cartera, operaciones y solicitudes.
- **Cliente:** consulta viviendas disponibles y registra interés (visita, compra, alquiler).

## Enfoque de construcción (por capas)

La app se construyó de dentro hacia fuera, manteniendo el dominio independiente de la UI y de la base de datos.

```text
1. Utilidades     → enums + validadores
2. Modelos        → Casa, Inquilino, Contrato (reglas de negocio)
3. Servicios      → GestionInmobiliaria (cartera en memoria)
4. Persistencia   → SQLite (Database + Repositorio)
5. Fachada app    → AppInmobiliaria (sincroniza dominio ↔ BD)
6. Interfaz       → tkinter dual Agente/Cliente
7. Entrada        → main.py (+ demo consola)
8. Tests          → unittest sobre el dominio
```

## Fases realizadas

| Fase | Entregable | Idea clave |
|---|---|---|
| 1 | `src/utils/` | Constantes tipadas y validaciones reutilizables |
| 2 | `src/modelos/` | Encapsulamiento, properties, métodos de instancia/clase/estáticos |
| 3 | `src/servicios/gestion_inmobiliaria.py` | Orquestación de cartera sin UI |
| 4 | `tests/` | Verificación del dominio con unittest |
| 5 | `ejemplos/demo_completa.py` | Recorrido pedagógico por consola |
| 6 | `src/persistencia/` + `AppInmobiliaria` | Persistencia SQLite y semillas |
| 7 | `src/ui/app_grafica.py` | Menú dual gráfico y flujos de uso real |

## Decisiones de diseño

### Dominio rico (no anémico)
Las reglas viven en los objetos (`Casa.comprar()`, `Inquilino.puede_alquilar()`), no solo en la UI. Así la demo, los tests y la interfaz reutilizan la misma lógica.

### Separación UI / dominio / persistencia
- La UI llama a `AppInmobiliaria`, no escribe SQL.
- El repositorio traduce filas SQLite ↔ objetos de dominio.
- `GestionInmobiliaria` trabaja en memoria; la fachada recarga tras cada cambio relevante.

### Persistencia ligera
SQLite en `data/inmobiliaria.db`: sin servidor, portable y suficiente para el alcance académico/demo.

### Roles sin autenticación compleja
La pantalla inicial elige perfil (Agente/Cliente). No hay login con contraseña: el foco es el dominio y los flujos.

### Dualidad educativa y usable
- `python main.py --demo` → conceptos POO en consola.
- `python main.py` → uso gráfico con guardado real.

## Stack tecnológico

| Pieza | Tecnología |
|---|---|
| Lenguaje | Python 3.14+ |
| UI | `tkinter` / `ttk` |
| BD | `sqlite3` |
| Tests | `unittest` |
| Diagramas (docs) | Mermaid en Markdown |
| Control de versiones | Git / GitHub |

## Flujo de arranque en tiempo de ejecución

1. `main.py` parsea argumentos.
2. Sin `--demo`: importa `ejecutar_app()`.
3. Se crea `AppInmobiliaria` → abre/crea SQLite → carga casas (o siembra datos).
4. Se abre `AppGrafica` (ventana tkinter).
5. El usuario elige Agente o Cliente y opera; cada cambio relevante se sincroniza a disco.
6. Al cerrar, se cierra la conexión SQLite.

## Principios POO aplicados

- **Encapsulamiento:** atributos privados (`_dni`, `_propiedades`, `_estado`) y properties.
- **Abstracción:** servicios y repositorio ocultan detalles de lista/SQL.
- **Colaboración:** `Casa` usa `Inquilino` y crea `Contrato`.
- **Enums:** estados y tipos de operación tipados.
- **Validación defensiva:** `ValueError` / `TypeError` ante datos inválidos.
