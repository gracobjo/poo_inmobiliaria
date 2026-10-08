@ECHO OFF
REM Genera la documentacion HTML con Sphinx (Windows)

pushd %~dp0

if exist "..\.venv\Scripts\sphinx-build.exe" (
  set "SPHINXBUILD=..\.venv\Scripts\sphinx-build.exe"
) else (
  set "SPHINXBUILD=sphinx-build"
)

if "%1" == "clean" (
  if exist _build rmdir /s /q _build
  echo Limpiado _build
  popd
  exit /b 0
)

"%SPHINXBUILD%" -b html . _build\html
if errorlevel 1 (
  echo Error al generar la documentacion.
  popd
  exit /b 1
)

echo.
echo HTML generado en: %CD%\_build\html\index.html
popd
