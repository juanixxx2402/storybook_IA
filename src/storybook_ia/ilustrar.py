import json
import os
import subprocess
from pathlib import Path
from time import perf_counter

CARPETA_CODIGO = Path(__file__).resolve().parent
RAIZ_PROYECTO = CARPETA_CODIGO.parent.parent
CARPETA_MODELOS = RAIZ_PROYECTO / "models"


def main():
    archivo_cuento = Path(
        os.environ.get("STORYBOOK_CUENTO", CARPETA_CODIGO / "cuento.json")
    )
    modelo = CARPETA_MODELOS / "dreamshaper_8.safetensors"
    ejecutable = next(CARPETA_MODELOS.rglob("sd-cli.exe"), None)

    if not archivo_cuento.is_file():
        raise SystemExit("Genera el cuento con main.py para crear cuento.json.")
    if ejecutable is None:
        raise SystemExit("No se encontró sd-cli.exe dentro de models.")
    if not modelo.is_file():
        raise SystemExit(f"No se encontró el modelo de imágenes en {modelo}.")

    cuento = json.loads(archivo_cuento.read_text(encoding="utf-8"))
    carpeta_salida = Path(
        os.environ.get("STORYBOOK_SALIDA", RAIZ_PROYECTO / "salidas")
    )
    carpeta_salida.mkdir(exist_ok=True)

    for numero, escena in enumerate(cuento["escenas"], start=1):
        imagen = carpeta_salida / f"escena-{numero:02d}.png"

        if imagen.is_file():
            print(f"Escena {numero}: ya existe {imagen.name}, se conserva.")
            continue

        prompt = (
            f"Storybook illustration, {cuento['protagonista_visual']}. "
            f"{escena['imagen']}. Soft watercolor, expressive lighting."
        )

        print(f"Generando escena {numero}/5...", flush=True)
        inicio = perf_counter()

        try:
            subprocess.run(
                [
                    str(ejecutable),
                    "-m", str(modelo),
                    "-p", prompt,
                    "-W", "384",
                    "-H", "384",
                    "--steps", "12",
                    "--seed",  str(41 + numero),
                    "-o", str(imagen),
                ],
                cwd=ejecutable.parent,
                check=True,
            )
        except subprocess.CalledProcessError as error:
            raise SystemExit(
                f"Falló la escena {numero} con código {error.returncode}. "
                "Revisa las últimas líneas de la terminal."
            ) from error

        if not imagen.is_file():
            raise SystemExit(f"No se guardó la imagen de la escena {numero}.")

        print(f"{imagen.name} lista en {perf_counter() - inicio:.1f} segundos.")


if __name__ == "__main__":
    main()