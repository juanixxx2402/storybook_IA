import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODELO = "qwen3:1.7b"
URL_OLLAMA = "http://127.0.0.1:11434/api/generate"
ARCHIVO_CUENTO = Path(__file__).with_name("cuento.json")


def generar_cuento(idea, genero):
    prompt = f"""
    Eres un escritor de cuentos breves ilustrados.

    IDEA DEL USUARIO:
    {idea}

    GÉNERO:
    {genero}

    Escribe un cuento original en español con exactamente cinco escenas.
    Usa la idea del usuario como base de los acontecimientos.
    Mantén los nombres, los rasgos y los hechos establecidos.

    Cada escena debe cumplir una función:
    1. Presentación: muestra al protagonista, su lugar y lo que desea.
    2. Problema: ocurre algo que dificulta alcanzar ese deseo.
    3. Intento: el protagonista actúa, pero aparece una complicación nueva.
    4. Decisión: toma una decisión que permite enfrentar el problema.
    5. Desenlace: muestra el resultado y resuelve el conflicto principal.

    REGLAS NARRATIVAS:
    - Escribe entre 35 y 55 palabras por escena.
    - Cada escena comienza donde terminó la anterior.
    - En cada escena sucede una acción nueva con una consecuencia.
    - Evita repetir frases, descubrimientos o conversaciones.
    - Presenta un problema concreto y una solución comprensible.
    - El desenlace debe surgir de las acciones del protagonista.
    - Ajusta el tono, los acontecimientos y el final al género indicado.

    Devuelve un objeto JSON con estas claves:
    - titulo: título específico del cuento en español.
    - protagonista_visual: descripción en inglés del aspecto físico
      y la ropa del protagonista, de un máximo de 30 palabras.
    - escenas: lista de exactamente cinco objetos.

    Cada objeto de escenas contiene:
    - texto: narración en español de esa escena.
    - imagen: descripción visual en inglés, de entre 25 y 40 palabras,
      que represente un instante concreto del texto de esa escena.

    REGLAS PARA imagen:
    - Describe la acción visible, el lugar y los objetos importantes.
    - Usa acciones y composiciones distintas entre escenas.
    - Alterna encuadres cuando ayude a mostrar la acción.
    - Conserva los lugares y objetos cuando la historia lo requiera.
    - Evita conceptos abstractos que no puedan verse en una ilustración.
    - La descripción debe corresponder al texto de su propia escena.
    """

    datos = {
        "model": MODELO,
        "prompt": prompt,
                "format": {
            "type": "object",
            "properties": {
                "titulo": {"type": "string", "minLength": 1},
                "protagonista_visual": {"type": "string", "minLength": 1},
                "escenas": {
                    "type": "array",
                    "minItems": 5,
                    "maxItems": 5,
                    "items": {
                        "type": "object",
                        "properties": {
                            "texto": {"type": "string", "minLength": 1},
                            "imagen": {"type": "string", "minLength": 1},
                        },
                        "required": ["texto", "imagen"],
                    },
                },
            },
            "required": ["titulo", "protagonista_visual", "escenas"],
        },
        "stream": False,
        "think": False,
        "keep_alive": 0,
    }
    solicitud = Request(
        URL_OLLAMA,
        data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    with urlopen(solicitud, timeout=300) as respuesta:
        resultado = json.load(respuesta)

    return json.loads(resultado["response"])


def texto_valido(valor):
    return isinstance(valor, str) and bool(valor.strip())


def validar_cuento(cuento):
    if not isinstance(cuento, dict):
        raise ValueError("Se esperaba un objeto JSON con el cuento.")

    if not texto_valido(cuento.get("titulo")):
        raise ValueError("El cuento no tiene título.")

    if not texto_valido(cuento.get("protagonista_visual")):
        raise ValueError("Falta la descripción visual del protagonista.")

    escenas = cuento.get("escenas")
    if not isinstance(escenas, list) or len(escenas) != 5:
        raise ValueError("El modelo debe devolver exactamente cinco escenas.")

    for numero, escena in enumerate(escenas, start=1):
        if not isinstance(escena, dict) or not all(
            texto_valido(escena.get(campo)) for campo in ("texto", "imagen")
        ):
            raise ValueError(f"La escena {numero} necesita texto e imagen.")
        for campo, nombre in (("texto", "texto"), ("imagen", "descripción visual")):
            escenas_vistas = {}

        for numero, escena in enumerate(escenas, start=1):
            contenido = " ".join(escena[campo].casefold().split())

            if contenido in escenas_vistas:
                anterior = escenas_vistas[contenido]
                raise ValueError(
                    f"Las escenas {anterior} y {numero} repiten el mismo {nombre}."
                )

            escenas_vistas[contenido] = numero


def main():
    idea = input("Idea del cuento: ").strip()
    genero = input("Género: ").strip()

    if not idea or not genero:
        print("Escribe una idea y un género.")
        return

    print("Generando el cuento...")
    try:
        cuento = generar_cuento(idea, genero)
        validar_cuento(cuento)
    except HTTPError as error:
        print(f"Ollama devolvió el error HTTP {error.code}.")
        print(error.read().decode("utf-8", errors="replace"))
        return
    except (URLError, TimeoutError) as error:
        print(f"No pude obtener respuesta. Verifica que Ollama esté abierto. {error}")
        return
    except (ValueError, KeyError) as error:
        print(f"La respuesta del modelo no pasó la validación. {error}")
        return

    ARCHIVO_CUENTO.write_text(
        json.dumps(cuento, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n{cuento['titulo']}")
    for numero, escena in enumerate(cuento["escenas"], start=1):
        print(f"\nEscena {numero}\n{escena['texto']}")

    print(f"\nGuardado en {ARCHIVO_CUENTO.name}")


if __name__ == "__main__":
    main()