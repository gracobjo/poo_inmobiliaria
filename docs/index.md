# Sistema Inmobiliario POO

Documentación generada con **Sphinx** a partir de los ficheros Markdown del directorio `docs/`.

```{toctree}
:maxdepth: 2
:caption: Contenido

README
01-construccion
02-estructura
03-clases
04-casos-de-uso
05-diagramas-uml
06-manual-desarrollador
07-manual-usuario
08-interfaz-ui
09-importacion-datos
```

## Generar esta documentación

Desde la raíz del proyecto, con el entorno virtual activado:

```bash
.\.venv\Scripts\Activate.ps1
sphinx-build -b html docs docs/_build/html
```

Luego abre `docs/_build/html/index.html` en el navegador.
