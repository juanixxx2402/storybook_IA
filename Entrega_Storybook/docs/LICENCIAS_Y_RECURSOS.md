# Licencias y recursos de terceros

Este inventario identifica los componentes usados o propuestos. Conservar las fichas y licencias de las revisiones exactas que se descarguen. Los pesos, datos, programas y resultados tienen condiciones que deben revisarse por separado. El archivo LICENSE de este paquete es una propuesta MIT para el código propio del equipo.

| Recurso | Procedencia | Licencia o condición publicada | Acción de entrega |
| --- | --- | --- | --- |
| Qwen3 1.7B | Qwen, distribuido localmente mediante Ollama | Apache 2.0 en la ficha del modelo | Registrar tag de Ollama, identificador del modelo y atribución |
| DreamShaper 8 | Lykon, ajuste de SD 1.5. Archivo usado procedente del espejo Yntec/Dreamshaper8 | CreativeML OpenRAIL-M en la ficha de Lykon | Conservar licencia, origen, hash y restricciones de uso |
| Ollama | ollama/ollama | MIT | Registrar versión y conservar avisos si se redistribuye |
| stable-diffusion.cpp | leejet/stable-diffusion.cpp | MIT | Registrar release. Revisar también licencias de componentes del binario |
| Piper actual | OHF-Voice/piper1-gpl | GPL-3.0 según el repositorio actual | Registrar versión de piper-tts instalada. Revisar términos al distribuir el programa |
| Voz sharvard medium | rhasspy/piper-voices, es/es_ES/sharvard/medium | La ficha remite al dataset con CC BY 3.0 y describe dos hablantes y el modelo base de ajuste | Conservar MODEL_CARD, atribuir el recurso y revisar condiciones de la revisión exacta y su base |
| Voz ald medium inicial | rhasspy/piper-voices, es/es_MX/ald/medium | Revisar MODEL_CARD de la revisión descargada | Registrar si esta es la voz realmente activa |
| Streamlit | streamlit/streamlit | Apache 2.0 | Conservar referencia y registrar versión |
| Ambientes | Código procedural del proyecto | Cubiertos por la licencia elegida para el código propio | Documentar fórmulas, parámetros y semilla |

## Fuentes

- https://huggingface.co/Qwen/Qwen3-1.7B
- https://huggingface.co/Lykon/dreamshaper-8
- https://huggingface.co/Yntec/Dreamshaper8/blob/main/dreamshaper_8.safetensors
- https://github.com/ollama/ollama/blob/main/LICENSE
- https://github.com/leejet/stable-diffusion.cpp/blob/master/LICENSE
- https://github.com/OHF-Voice/piper1-gpl
- https://huggingface.co/rhasspy/piper-voices/blob/main/es/es_ES/sharvard/medium/MODEL_CARD
- https://huggingface.co/rhasspy/piper-voices/tree/main/es/es_MX/ald/medium
- https://github.com/streamlit/streamlit/blob/develop/LICENSE

## Consideraciones de voz y contenido

La aplicación utiliza una voz preentrenada. No solicita muestras personales para clonar la voz. Presentar la narración como síntesis de voz y conservar la atribución correspondiente. Para recursos de audio externos que se añadan después, registrar autor, enlace, licencia y fecha de descarga antes de publicarlos.

Los cuentos e imágenes pueden contener sesgos, errores visuales o contenido inadecuado para ciertas edades. Revisar los resultados de los géneros infantil y terror antes de compartirlos. El procesamiento local reduce la necesidad de transmitir las ideas a un proveedor externo. Los JSON y audios se almacenan en disco y deben revisarse si la idea contiene información personal.

## Datos exactos por registrar

Modelo de voz y hablante activo, versión de Piper, licencia de su revisión descargada, release de stable-diffusion.cpp, hash SHA256 de DreamShaper, tag e identificador de Qwen en Ollama y revisiones de las fichas conservadas.
