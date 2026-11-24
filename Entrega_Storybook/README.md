# historIA

Aplicación local que convierte una idea y un género en un cuento de exactamente cinco escenas. Cada escena presenta texto, una ilustración, narración sintética y un ambiente sonoro. La interfaz permite navegar por las escenas y abrir historias guardadas.


## Componentes

| Componente | Implementación |
| --- | --- |
| Relato | Qwen3 1.7B mediante Ollama local |
| Título | Solicitud adicional al mismo modelo a partir de las cinco escenas |
| Ilustraciones | DreamShaper 8 mediante stable-diffusion.cpp |
| Voz | Piper. Confirmar en `narrar.py` si está activa `es_ES-sharvard-medium` o la voz inicial `es_MX-ald-medium` |
| Ambiente | Síntesis procedural con Python y selección por palabras clave |
| Interfaz | Streamlit con estilos CSS y animación local de un libro |
| Persistencia | JSON, PNG y WAV en carpetas locales por cuento |

## Requisitos del equipo

- Windows de 64 bits y Python 3.12 como entorno de referencia.
- Git, uv y Ollama instalados.
- Perfil utilizado durante el desarrollo comunicado por el autor: 12 GB de RAM DDR4, AMD Radeon(TM) Graphics y disco SSD. CPU exacta pendiente de registrar.
- Presupuesto orientativo de 8 a 12 GB de disco libre para dependencias, modelos, descargas y resultados. Puede variar con los binarios y las cachés.
- La generación se realiza por etapas y las imágenes de una en una. El tiempo real depende del procesador y debe medirse en la instalación final.
- Para las pruebas, cerrar aplicaciones de alto consumo y registrar la RAM disponible. Una GPU dedicada es opcional en el perfil CPU.
- Internet durante instalación y descarga inicial. Con dependencias y modelos disponibles, el flujo debe probarse sin conexión.

## Estructura del proyecto

| Ruta | Contenido |
| --- | --- |
| `pyproject.toml` y `uv.lock` | Dependencias y resolución exacta del entorno real |
| `.streamlit/config.toml` | Tema visual |
| `src/storybook_ia/main.py` | Solicitud de cuento y validación |
| `src/storybook_ia/ilustrar.py` | Generación de imágenes |
| `src/storybook_ia/narrar.py` | Síntesis de voz |
| `src/storybook_ia/ambientar.py` | Composición de ambientes |
| `src/storybook_ia/app.py` | Interfaz y coordinación |
| `models/dreamshaper_8.safetensors` | Pesos descargados de DreamShaper |
| `models/<carpeta-del-binario>/sd-cli.exe` | Ejecutable y DLL de stable-diffusion.cpp, conservando la distribución completa |
| `src/storybook_ia/voces/` | Archivo ONNX y configuración JSON de Piper |
| `salidas/cuentos/<identificador>/` | JSON, imágenes, voces y ambientes de cada cuento |
| `docs/` | Informe, guion y documentación de licencias |
| `evidencias/` | Capturas y registros de las pruebas seleccionadas |

## Instalación paso a paso

### 1. Instalar herramientas

Instalar Git, uv y Ollama desde sus sitios oficiales. Reiniciar la terminal después de instalar.

- [Git](https://git-scm.com/downloads)
- [uv para Windows](https://docs.astral.sh/uv/getting-started/installation/)
- [Ollama para Windows](https://ollama.com/download/windows)

### 2. Obtener el código

Clonar el repositorio público del equipo o descargar su ZIP. Desde PowerShell, entrar a la raíz de `storybook-ia`, donde aparece `pyproject.toml`.

```powershell
git --version
uv --version
ollama --version
```

### 3. Instalar dependencias

Conservar los archivos `pyproject.toml` y `uv.lock` del proyecto funcional. Ejecutar en la raíz:

```powershell
uv sync --locked
```

Si todavía no existe un archivo de bloqueo, ejecutar `uv sync`, comprobar la aplicación y publicar el `uv.lock` generado. Las dependencias directas conocidas son `streamlit` y `piper-tts`. La biblioteca estándar aporta JSON, HTTP local, rutas, subprocess, generación de ondas y escritura WAV. Instalar Piper mediante uv incorpora sus dependencias, incluido el runtime ONNX compatible.

### 4. Descargar el modelo de texto

Abrir Ollama y ejecutar:

```powershell
ollama pull qwen3:1.7b
ollama list
```

En `main.py`, comprobar `MODELO = "qwen3:1.7b"` y el endpoint `http://127.0.0.1:11434/api/generate`. Los pesos de Ollama se almacenan en su ubicación administrada. No es necesario copiarlos a `models`.

### 5. Descargar DreamShaper y el ejecutable de imágenes

Descargar únicamente `dreamshaper_8.safetensors` y guardarlo en `models/` en la raíz. El archivo de referencia ocupa aproximadamente 2,13 GB. Conservar su licencia y origen.

- [Autor y ficha de DreamShaper 8](https://huggingface.co/Lykon/dreamshaper-8)
- [Archivo usado en la comparación del proyecto](https://huggingface.co/Yntec/Dreamshaper8/blob/main/dreamshaper_8.safetensors)
- [Releases de stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp/releases)

Descargar un paquete de Windows x64 para CPU compatible con el procesador. Extraer todo el paquete dentro de `models`, conservando las DLL junto a `sd-cli.exe`. El script de referencia busca el ejecutable recursivamente dentro de `models`. Si la instalación funcional utiliza `tools/sd`, conservar esa ruta y reflejarla en `ilustrar.py`.

En `ilustrar.py`, comprobar la ruta del modelo. El perfil de comparación propuesto usa 512 × 512 y 20 pasos. Registrar los parámetros realmente activos, incluida la semilla y el método de muestreo del binario utilizado.

### 6. Descargar la voz

Desde `src/storybook_ia`:

```powershell
uv run python -m piper.download_voices es_ES-sharvard-medium --data-dir .\voces
```

Comprobar los dos archivos:

```powershell
Test-Path .\voces\es_ES-sharvard-medium.onnx
Test-Path .\voces\es_ES-sharvard-medium.onnx.json
```

En `narrar.py`, el nombre de voz del comando y el archivo comprobado deben coincidir. Si se conserva `es_MX-ald-medium`, descargar esa voz con el mismo comando cambiando su identificador. Sharvard contiene dos hablantes según su ficha actual. Registrar el hablante seleccionado y la versión de Piper antes de cerrar la entrega.

### 7. Ejecutar

Volver a la raíz e iniciar Streamlit:

```powershell
uv run streamlit run .\src\storybook_ia\app.py
```

Abrir la URL local que muestra la terminal, normalmente `http://localhost:8501`. Mantener Ollama y la terminal de Streamlit en ejecución.

## Ejemplo de uso

**Idea**. Una niña con impermeable amarillo descubre que el faro de su pueblo se apagó cuando el barco de su padre intenta regresar entre la niebla. Debe cruzar el muelle, subir al faro y encontrar una forma de guiarlo.

**Género**. Aventura.

1. Escribir la idea y seleccionar el género.
2. Pulsar el botón de creación y esperar la animación del libro.
3. Leer el título y recorrer exactamente cinco escenas.
4. Reproducir la narración y el ambiente en controles separados.
5. Volver a abrir la historia desde la biblioteca.

El título y las ilustraciones concretas varían entre ejecuciones. El título puede editarse o volver a proponerse con IA desde el lector.

## Datos y flujo de ejecución

`main.py` produce un JSON con `titulo`, `protagonista_visual` y `escenas`. Cada escena tiene `texto` e `imagen`. La interfaz propone el título con el relato completo y valida el cuento. Luego ejecuta los scripts de imagen, voz y ambiente mediante subprocess.

`STORYBOOK_CUENTO` indica el JSON que deben leer y `STORYBOOK_SALIDA` el destino de los recursos. Cada nuevo cuento tiene una carpeta identificada con fecha y UUID. Solo después de comprobar los quince recursos esperados se escribe `completo.txt` y el cuento aparece como completo.

El ambiente se elige por palabras clave y se sintetiza con ruido y ondas. La animación del libro se realiza con HTML y CSS locales. Los archivos de modelos preentrenados se usan para inferencia.

## Comprobación de funcionamiento

- Generar tres cuentos distintos conservando sus cinco escenas completas.
- Comparar dos configuraciones con el mismo JSON y las mismas condiciones.
- Registrar CPU, RAM, GPU, versiones, resolución, pasos, semillas y tiempos reales.
- Probar navegación, correspondencia de texto y voz, ambientes pertinentes y reapertura.
- Desconectar la red tras instalar los recursos y generar un cuento nuevo con Ollama activo.
- Seguir `evidencias/REGISTRO_PRUEBAS.md` para adjuntar capturas y resultados.

## Solución de problemas

| Síntoma | Acción |
| --- | --- |
| Ollama no responde | Abrir Ollama y comprobar `ollama list`, el modelo y el endpoint local. |
| Falta `sd-cli.exe` | Revisar la extracción completa y la búsqueda del ejecutable en `ilustrar.py`. |
| `InvalidProtobuf` | Volver a descargar el ONNX y comprobar la integridad contra el origen. |
| `Unable to find voice` | Revisar la carpeta `voces`, el ONNX, su JSON y el identificador del script. |
| Cinco escenas repetidas | Revisar los prompts y confirmar el modelo Qwen3 1.7B activo. |
| Imágenes antiguas | Abrir el cuento correcto. Cada cuento nuevo tiene su propia carpeta. |
| Etapa interrumpida | Leer el error y conservar la carpeta parcial para diagnosticarlo. La interfaz todavía no ofrece reanudación automática. |

## Publicación

Conservar en Git el código fuente, `pyproject.toml`, `uv.lock`, tema, README, licencia y documentación. Excluir `.venv`, modelos, binarios descargados, secretos y resultados masivos. Seleccionar las evidencias que se publicarán de forma expresa. `.gitignore` no deja de rastrear archivos que ya estaban en el historial.

## Licencias y derechos

Se propone MIT para el código propio, sujeto a revisión de los titulares del proyecto. Las herramientas, modelos y voces conservan sus licencias independientes. Revisar `docs/LICENCIAS_Y_RECURSOS.md`, conservar atribuciones y descargar recursos desde sus fuentes. Publicar exclusivamente archivos cuya redistribución esté autorizada.
