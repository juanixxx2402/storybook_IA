# Cómo integrar y cerrar la entrega

## Archivos preparados

- `README.md` para colocar en la raíz del repositorio.
- `.gitignore` para combinar con el existente.
- `LICENSE` con propuesta MIT para el código propio. Revisar la elección con los titulares antes de publicar.
- `docs/Informe_Tecnico_Storybook.pdf` con arquitectura, metodología, decisiones, resultados cualitativos y pendientes identificados.
- `docs/Informe_Tecnico_Storybook.md` como versión editable del contenido.
- `docs/GUION_VIDEO.md` para grabar la demostración.
- `docs/LICENCIAS_Y_RECURSOS.md` para atribuciones y recursos.
- `evidencias/REGISTRO_PRUEBAS.md` para completar las tres pruebas y la comparación.

Este paquete contiene documentación para integrar al proyecto funcional. El código fuente completo y sus archivos reales de dependencias deben provenir de la carpeta de trabajo del autor. La versión final del repositorio y la reproducción en otra máquina requieren verificarlos juntos.

## Pasos de integración

1. Copiar README y documentación a la carpeta `storybook-ia` que ya funciona.
2. Combinar `.gitignore` con el existente. Revisar LICENSE y las atribuciones.
3. Conservar `pyproject.toml` y `uv.lock` de la instalación funcional. No sustituirlos por una lista inventada de versiones.
4. Confirmar nombre de voz, hablante, CPU y parámetros de ilustración.
5. Completar tres pruebas y una comparación controlada. Añadir evidencias al informe editable y volver a exportar su PDF.
6. Grabar el video siguiendo el guion y conservar el tiempo real de generación.
7. Publicar el código y documentación en GitHub público, con el enlace y un commit de entrega identificable.
8. Probar instalación limpia siguiendo el README, y ejecución sin red con los modelos ya descargados.

## Registrar el entorno desde la raíz

Estos comandos muestran datos del entorno. Seleccionar los valores técnicos antes de incorporarlos al informe.

```powershell
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_ComputerSystem | Select-Object @{Name='RAM_GB';Expression={[math]::Round($_.TotalPhysicalMemory / 1GB, 1)}}
Get-CimInstance Win32_VideoController | Select-Object Name
uv run python --version
uv --version
ollama --version
ollama list
uv pip show streamlit piper-tts onnxruntime
Get-FileHash .\models\dreamshaper_8.safetensors -Algorithm SHA256
```

Registrar también el nombre del ZIP de stable-diffusion.cpp usado y su versión o release.

## Subir a Git

Desde la raíz del proyecto funcional, revisar y guardar el contenido.

```powershell
git init
git status --short
git add .
git diff --cached --stat
git diff --cached --name-only
git commit -m "Prepara entrega de historIA y documentacion tecnica"
```

Comprobar que la lista incluya el código de `src/storybook_ia`, README, licencia, tema, `pyproject.toml`, `uv.lock` y documentos, y que excluya modelos, entornos y secretos. Si ya existían archivos grandes rastreados, el patrón en `.gitignore` no los retira del índice ni del historial. Revisar ese caso antes del push.

El comando para conectar y publicar se completa con la URL real del repositorio y la rama actual. Obtener ambos con `git remote -v` y `git branch --show-current`. Si el remoto ya tiene contenido, comprobarlo antes de integrar cambios. El repositorio debe ser público para cumplir el enunciado.

## Qué falta para afirmar que la entrega está completa

| Entregable | Estado |
| --- | --- |
| README, licencia propuesta y guía de modelos | Preparados. Pendiente contrastar con código final |
| PDF técnico | Preparado con resultados cualitativos. Pendientes capturas y mediciones |
| Repositorio público | URL, commit y publicación pendientes |
| Video de demostración | Guion preparado. Grabación pendiente |
| Aplicación local | Funcionamiento reportado por el autor. Pendiente revisión del código final y prueba de instalación limpia |
| Tres pruebas y comparación | Registro preparado. Adjuntar resultados y evidencias reales |

Para revisar la versión final, compartir una copia de `src`, `.streamlit`, `pyproject.toml`, `uv.lock`, README y documentación. Excluir `.venv`, modelos y binarios para reducir el tamaño. Adjuntar por separado las capturas y resultados de prueba seleccionados.
