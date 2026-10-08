# Manual del desarrollador

## 1. Requisitos

- Python **3.14+**
- Sistema con soporte de `tkinter` (incluido en instaladores oficiales de Windows/macOS; en Linux puede requerir `python3-tk`)
- Git (opcional)

No hay dependencias pip obligatorias: todo usa biblioteca estándar.

## 2. Clonar y ejecutar

```bash
git clone https://github.com/gracobjo/poo_inmobiliaria.git
cd poo_inmobiliaria
python main.py
```

Demo consola:

```bash
python main.py --demo
```

Tests:

```bash
python -m unittest discover -s tests -v
```

## 3. Organización del código

Sigue una arquitectura en capas. Reglas prácticas:

1. **No importes `tkinter` desde `modelos/` ni `persistencia/`.**
2. **No escribas SQL fuera de `persistencia/`.**
3. **La UI solo habla con `AppInmobiliaria`** (o, en demo, con el dominio directamente).
4. **Las reglas de negocio van en el modelo** (`Casa`, `Inquilino`, `Contrato`).

Ver detalle en [02-estructura.md](02-estructura.md) y [03-clases.md](03-clases.md).

## 4. Convenciones

| Tema | Convención |
|---|---|
| Lenguaje de código | Español en nombres de dominio (`Casa`, `alquilar`) |
| Type hints | Obligatorios en APIs públicas |
| Docstrings | Estilo Google/Args-Returns |
| Errores de dominio | `ValueError` / `TypeError` |
| Formato fechas | ISO `YYYY-MM-DD` |
| BD | SQLite; ids enteros autoincrementales |
| Tests | `unittest`, métodos `test_*` |

## 5. Ciclo de un cambio de negocio (ejemplo)

Añadir un nuevo estado o operación típica:

1. Actualizar enum en `utils/constantes.py` si aplica.
2. Implementar método en `Casa` (validaciones + cambio de estado).
3. Persistir efecto vía `AppInmobiliaria.sincronizar` (ya genérico si solo cambia casa/contrato).
4. Exponer botón/acción en `AppGrafica` si es usable.
5. Añadir test en `tests/test_casa.py`.
6. Documentar caso de uso en `docs/04-casos-de-uso.md`.

## 6. Persistencia

### Ubicación
`data/inmobiliaria.db` (creada automáticamente).

### Reiniciar datos de demo
Borra el fichero y vuelve a arrancar:

```bash
# PowerShell
Remove-Item data\inmobiliaria.db -ErrorAction SilentlyContinue
python main.py
```

### Semillas
Si la tabla `casas` está vacía, `AppInmobiliaria._sembrar_datos()` inserta 4 viviendas y un alquiler de ejemplo en Sevilla.

### Extender el esquema
1. Añade `CREATE TABLE` / columnas en `Database._crear_esquema` (o migraciones simples con `ALTER`).
2. Actualiza `RepositorioInmobiliario`.
3. Adapta el dominio si hay nuevos campos.

## 7. Interfaz gráfica

Archivo único principal: `src/ui/app_grafica.py`.

Patrón:

- `_mostrar_inicio` / `_mostrar_agente` / `_mostrar_cliente` reconstruyen el frame contenedor.
- Tras cada mutación: `app.sincronizar(casa)` o `app.agregar_casa(casa)` + refresco de tabla.
- Errores de dominio → `messagebox.showerror`.

Estilos en diccionario `COLORES` y `ttk.Style`.

## 8. Tests

```bash
python -m unittest discover -s tests -v
```

Buenas prácticas:

- En `setUp` de `Casa`, resetear `Casa.total_casas`, `impuesto_aitp`, `iva_reforma`.
- No depender de la UI ni de un `.db` compartido; si pruebas persistencia, usa ruta temporal.

## 9. Depuración rápida

| Síntoma | Comprobar |
|---|---|
| No aparecen casas | ¿Existe `data/inmobiliaria.db`? ¿Estado `DISPONIBLE` en cliente? |
| Error al solicitar visita | Perfil incompleto (nombre/DNI/tel/ingresos) |
| Alquiler rechazado | Regla 35 % |
| CP inválido | Rango 01000–52999 |
| Contador `total_casas` raro | `AppInmobiliaria.cargar()` lo recalcula |

## 10. Importación de datos

Ver el documento dedicado [09-importacion-datos.md](09-importacion-datos.md): requisitos, UML, CSV de prueba y API.

Puntos clave:

- Paquete `src/importacion/`
- UI: `filedialog` en Agente (`Importar datos…`)
- CSV de tipologías: `data/ejemplos/casas_10_tipos.csv`

## 11. Roadmap técnico sugerido

1. Autenticación real (usuario/contraseña, roles).
2. API REST (FastAPI) reutilizando dominio.
3. Fotos y documentos adjuntos.
4. Migraciones de esquema versionadas.
5. Separar `AppGrafica` en módulos por pantalla.
