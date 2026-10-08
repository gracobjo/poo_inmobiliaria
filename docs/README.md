# Documentación — Sistema Inmobiliario POO

Índice de la documentación técnica y de usuario del proyecto.

| Documento | Contenido |
|---|---|
| [01 · Cómo se construyó](01-construccion.md) | Enfoque, fases, decisiones de diseño y stack |
| [02 · Estructura de carpetas](02-estructura.md) | Árbol del repositorio y responsabilidad de cada capa |
| [03 · Catálogo de clases](03-clases.md) | Clases, atributos, métodos y responsabilidades |
| [04 · Casos de uso](04-casos-de-uso.md) | Actores, escenarios Agente/Cliente y reglas de negocio |
| [05 · Diagramas UML](05-diagramas-uml.md) | Clases, secuencia, estados, componentes y ER |
| [06 · Manual del desarrollador](06-manual-desarrollador.md) | Entorno, convenciones, extensión y tests |
| [07 · Manual de usuario](07-manual-usuario.md) | Guía paso a paso Agente y Cliente |
| [08 · Interfaz de usuario (UI)](08-interfaz-ui.md) | Pantallas, flujos, widgets y estilo visual |
| [09 · Importación de datos](09-importacion-datos.md) | CSV, TXT, JSON, Excel, dict, DataFrame |

## Arranque rápido

```bash
python main.py          # Interfaz gráfica
python main.py --demo   # Demo por consola
python -m unittest discover -s tests -v
```

Requisito: **Python 3.14+** (biblioteca estándar: `tkinter`, `sqlite3`, `unittest`).

## Documentación HTML (Sphinx)

Estos Markdown se publican con Sphinx + MyST (tema Read the Docs):

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements-docs.txt
sphinx-build -b html docs docs/_build/html
# o: docs\make.bat
```

Abre `docs/_build/html/index.html` en el navegador.
