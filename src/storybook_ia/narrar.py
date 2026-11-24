import json
import os
import subprocess
import sys
from pathlib import Path

CARPETA_CODIGO = Path(__file__).resolve().parent
RAIZ_PROYECTO = CARPETA_CODIGO.parent.parent


def main():
    archivo_cuento = Path(
        os.environ.get("STORYBOOK_CUENTO", CARPETA_CODIGO / "cuento.json")
    )
    carpeta_voces = CARPETA_CODIGO / "voces"

    if not archivo_cuento.is_file():
        raise SystemExit("No se encontró cuento.json junto a narrar.py.")

    if not (carpeta_voces / "es_ES-sharvard-medium.onnx").is_file():
        raise SystemExit("Descarga la voz dentro de src/storybook_ia/voces.")

    cuento = json.loads(archivo_cuento.read_text(encoding="utf-8"))
    carpeta_salida = Path(
        os.environ.get("STORYBOOK_SALIDA", RAIZ_PROYECTO / "salidas")
    )
    carpeta_salida.mkdir(exist_ok=True)

    for numero, escena in enumerate(cuento["escenas"], start=1):
        audio = carpeta_salida / f"voz-{numero:02d}.wav"
        print(f"Narrando escena {numero}/5...", flush=True)

        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m", "piper",
                    "-m", "es_ES-sharvard-medium",
                    "--data-dir", str(carpeta_voces),
                    "-f", str(audio),
                    "--", escena["texto"],
                ],
                check=True,
            )
        except subprocess.CalledProcessError as error:
            raise SystemExit(
                f"Falló la narración de la escena {numero}. "
                "Revisa las últimas líneas de la terminal."
            ) from error

        if not audio.is_file() or audio.stat().st_size <= 44:
            raise SystemExit(f"No se generó audio válido para la escena {numero}.")

        print(f"Guardado: {audio.name}")

    print("Las cinco narraciones están en la carpeta salidas.")


if __name__ == "__main__":
    main()