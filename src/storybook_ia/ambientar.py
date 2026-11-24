import json
import os
import math
import random
import struct
import wave
from pathlib import Path

CARPETA_CODIGO = Path(__file__).resolve().parent
RAIZ_PROYECTO = CARPETA_CODIGO.parent.parent

FRECUENCIA = 22050
DURACION = 12

PALABRAS = {
    "lluvia": ["lluvia", "llov", "tormenta", "rain", "storm"],
    "fuego": ["fuego", "fogata", "chimenea", "fire", "campfire"],
    "agua": ["arroyo", "río", "rio ", "cascada", "river", "stream", "waterfall"],
    "noche": ["noche", "nocturn", "luna", "night", "moon"],
    "bosque": ["bosque", "árbol", "arbol", "forest", "tree", "bird"],
}


def elegir_ambiente(escena):
    descripcion = f"{escena['texto']} {escena['imagen']}".lower()

    for ambiente, palabras in PALABRAS.items():
        if any(palabra in descripcion for palabra in palabras):
            return ambiente

    return "viento"


def crear_audio(destino, ambiente, semilla):
    azar = random.Random(semilla)
    muestras = bytearray()
    ruido_suave = 0.0
    chasquido = 0.0

    for indice in range(FRECUENCIA * DURACION):
        tiempo = indice / FRECUENCIA
        ruido = azar.uniform(-1, 1)
        ruido_suave = 0.97 * ruido_suave + 0.03 * ruido

        if ambiente == "lluvia":
            valor = ruido * 0.18 + ruido_suave * 0.3

        elif ambiente == "fuego":
            if azar.random() < 0.0008:
                chasquido = azar.uniform(0.3, 0.7)
            chasquido *= 0.96
            valor = ruido_suave * 0.4 + chasquido * ruido

        elif ambiente == "agua":
            burbujeo = math.sin(
                2 * math.pi * 350 * tiempo + 5 * math.sin(2 * math.pi * 3 * tiempo)
            )
            valor = ruido_suave * 0.5 + burbujeo * 0.025

        elif ambiente == "noche":
            pulso = max(0, math.sin(2 * math.pi * 3 * tiempo)) ** 8
            valor = 0.07 * pulso * math.sin(2 * math.pi * 3200 * tiempo)
            valor += ruido_suave * 0.15

        elif ambiente == "bosque":
            fase = tiempo % 3
            canto = 0.0

            if fase < 0.4:
                envolvente = math.sin(math.pi * fase / 0.4) ** 2
                canto = envolvente * math.sin(
                    2 * math.pi * 1800 * fase + 8 * math.sin(2 * math.pi * 7 * fase)
                )

            valor = ruido_suave * 0.25 + canto * 0.09

        else:
            rafaga = 0.5 + 0.5 * math.sin(2 * math.pi * tiempo / 5)
            valor = ruido_suave * (0.3 + rafaga * 0.5)

        fundido = max(0, min(1, tiempo / 0.5, (DURACION - tiempo) / 0.5))
        muestra = int(max(-1, min(1, valor * fundido)) * 32767)
        muestras.extend(struct.pack("<h", muestra))

    with wave.open(str(destino), "wb") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(FRECUENCIA)
        archivo.writeframes(muestras)


def main():
    archivo_cuento = Path(
        os.environ.get("STORYBOOK_CUENTO", CARPETA_CODIGO / "cuento.json")
    )

    if not archivo_cuento.is_file():
        raise SystemExit("No se encontró cuento.json.")

    cuento = json.loads(archivo_cuento.read_text(encoding="utf-8"))
    carpeta_salida = Path(
        os.environ.get("STORYBOOK_SALIDA", RAIZ_PROYECTO / "salidas")
    )
    carpeta_salida.mkdir(exist_ok=True)
    ambientes = []

    for numero, escena in enumerate(cuento["escenas"], start=1):
        ambiente = elegir_ambiente(escena)
        destino = carpeta_salida / f"ambiente-{numero:02d}.wav"
        crear_audio(destino, ambiente, semilla=numero)
        ambientes.append(ambiente)
        print(f"Escena {numero}: {ambiente} → {destino.name}")

    (carpeta_salida / "ambientes.json").write_text(
        json.dumps(ambientes, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("Los cinco ambientes están listos.")


if __name__ == "__main__":
    main()