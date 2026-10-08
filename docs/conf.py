"""Configuración Sphinx — documentación generada desde los Markdown de docs/."""

from __future__ import annotations

project = "Sistema Inmobiliario POO"
copyright = "2026, gracobjo"
author = "gracobjo"
release = "1.0.0"

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "es"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = "Sistema Inmobiliario POO"

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]
myst_heading_anchors = 3
myst_fence_as_directive = ["mermaid"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"
