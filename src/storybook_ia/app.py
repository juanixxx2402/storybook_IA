import json
import re
from html import escape
from urllib.request import Request, urlopen
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st

import main as motor
from main import generar_cuento, validar_cuento

CARPETA_CODIGO = Path(__file__).resolve().parent
RAIZ_PROYECTO = CARPETA_CODIGO.parent.parent
SALIDAS = RAIZ_PROYECTO / "salidas"
CARPETA_CUENTOS = SALIDAS / "cuentos"

st.set_page_config(page_title="Storybook IA", page_icon="📖", layout="wide")
st.markdown('<div class="marca">histor<span>IA</span></div>', unsafe_allow_html=True)
st.caption("Cuentos ilustrados que empiezan contigo")
st.markdown(
    """
    <style>
        [data-testid="stForm"] {
            border: 0;
            border-radius: 16px;
            padding: 0;
            box-shadow: none;
        }

        [data-testid="stAppViewContainer"] {
            background: #ffffff;
        }

        [data-testid="stTextArea"] [data-baseweb="textarea"] {
            background: #ffffff;
            border: 1px solid #d8dce6;
            border-radius: 12px;
            box-shadow: none;
        }

        [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within {
            border-color: #6336c5;
            box-shadow: 0 0 0 2px #eee8fa;
        }

        [data-testid="stFormSubmitButton"] button[kind="primary"] {
            background: #6336c5;
            border-color: #6336c5;
            color: #ffffff;
        }

        [data-testid="stFormSubmitButton"] button[kind="primary"]:hover {
            background: #512ba5;
            border-color: #512ba5;
        }

        [data-testid="stTextArea"] textarea {
            background: #ffffff;
            color: #182237;
            padding: 14px 16px;
            line-height: 1.6;
        }

        [data-testid="stTextArea"] textarea::placeholder {
            color: #667085;
        }


        [data-testid="stAppViewContainer"] { font-family: Arial, sans-serif; }
        .block-container { max-width: 1180px; padding-top: 2.4rem; padding-bottom: 3rem; }
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background: #ffffff; color: #202437; }
        [data-testid="stHeading"], [data-testid="stMarkdownContainer"] { color: #202437; }
        .marca { font-family: Georgia, serif; font-size: 30px; font-weight: 700; letter-spacing: -1px; }
        .marca span { color: #6336c5; }
        .titulo-inicio { font-family: Georgia, serif; font-size: clamp(32px, 5vw, 48px); letter-spacing: -1.5px; line-height: 1.15; margin: 1.2rem 0 1rem; }
        .titulo-cuento { font-family: Georgia, serif; text-align: center; font-size: clamp(30px, 4vw, 48px); line-height: 1.2; margin: .4rem auto 1.2rem; max-width: 850px; letter-spacing: -1px; overflow-wrap: anywhere; }
        .titulo-portada { font-family: Georgia, serif; font-size: 22px; line-height: 1.3; margin: 12px 0; overflow-wrap: anywhere; }
        .numero-escena { font-size: 12px; font-weight: 600; letter-spacing: 2px; color: #746886; margin-top: 16px; }
        .texto-cuento { font-family: Georgia, serif; font-size: 21px; line-height: 1.85; margin: 15px 0 30px; overflow-wrap: anywhere; }
        .contador { text-align: center; font-size: 14px; color: #635e70; padding: 10px; }
        .st-key-lector { background: #faf9fc; border: 1px solid #eeebf2; border-radius: 24px; padding: 24px; margin-bottom: 22px; }
        .st-key-lector img { border-radius: 16px; }
        [class*="st-key-portada_"] { border-radius: 18px; background: #fff; }
        [class*="st-key-portada_"] img { border-radius: 12px; }
        [data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button { border-radius: 10px; min-height: 44px; font-weight: 600; }
        [data-testid="stButton"] button[kind="secondary"] { background: #fff; color: #43315e; border: 1px solid #ddd6e8; }
        [data-testid="stButton"] button[kind="secondary"]:hover { background: #f3eefb; border-color: #9474c5; }
        [data-testid="stButton"] button[kind="primary"] { background: #6336c5; color: #fff; border-color: #6336c5; }
        [data-testid="stButton"] button:disabled { opacity: .4; }
        [data-testid="stSelectbox"] [data-baseweb="select"] > div { background: #fff; color: #202437; border-radius: 10px; }
        @media (max-width: 700px) { .st-key-lector { padding: 14px; } .texto-cuento { font-size: 19px; } }

        .cuento-cargando {
            position: fixed;
            inset: 0;
            z-index: 9999;
            display: grid;
            place-items: center;
            background: rgba(250, 250, 253, 0.64);
            backdrop-filter: blur(9px);
            -webkit-backdrop-filter: blur(9px);
        }

        .cuento-libro {
            position: relative;
            width: 164px;
            height: 108px;
            perspective: 650px;
        }

        .cuento-tapa {
            position: absolute;
            inset: 5px -5px -6px;
            border-radius: 11px;
            background: #6336c5;
            box-shadow: 0 12px 26px rgba(77, 44, 138, 0.22);
        }

        .cuento-pagina {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 50%;
            border: 1px solid #e1d9ef;
            background-color: #fffdf8;
            background-image: repeating-linear-gradient(
                to bottom,
                transparent 0 10px,
                #e9e2f4 10px 11px
            );
            background-size: 68% 65%;
            background-position: center;
            background-repeat: no-repeat;
        }

        .cuento-pagina-izquierda {
            left: 0;
            border-radius: 9px 2px 2px 9px;
        }

        .cuento-pagina-derecha {
            right: 0;
            border-radius: 2px 9px 9px 2px;
        }

        .cuento-pagina-animada {
            right: 0;
            border-radius: 2px 9px 9px 2px;
            transform-origin: left center;
            animation: cuento-pasar-pagina 1.8s ease-in-out infinite;
        }

        @keyframes cuento-pasar-pagina {
            0%, 15% { transform: rotateY(0deg); opacity: 1; }
            75%, 90% { transform: rotateY(-180deg); opacity: 1; }
            100% { transform: rotateY(-180deg); opacity: 0; }
        }

        @media (prefers-reduced-motion: reduce) {
            .cuento-pagina-animada { animation: none; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

LIBRO_CARGANDO = """
<div class="cuento-cargando" role="status" aria-label="Generando el cuento">
    <div class="cuento-libro" aria-hidden="true">
        <div class="cuento-tapa"></div>
        <div class="cuento-pagina cuento-pagina-izquierda"></div>
        <div class="cuento-pagina cuento-pagina-derecha"></div>
        <div class="cuento-pagina cuento-pagina-animada"></div>
    </div>
</div>
"""

if "escena_actual" not in st.session_state:
    st.session_state.escena_actual = 0


def cambiar_escena(desplazamiento):
    st.session_state.escena_actual = max(
        0, min(4, st.session_state.escena_actual + desplazamiento)
    )


def ejecutar_script(nombre, carpeta):
    entorno = os.environ.copy()
    entorno["STORYBOOK_CUENTO"] = str(carpeta / "cuento.json")
    entorno["STORYBOOK_SALIDA"] = str(carpeta)
    entorno["PYTHONIOENCODING"] = "utf-8"

    resultado = subprocess.run(
        [sys.executable, str(CARPETA_CODIGO / nombre)],
        cwd=CARPETA_CODIGO,
        env=entorno,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if resultado.returncode != 0:
        detalle = resultado.stdout + "\n" + resultado.stderr
        raise RuntimeError(f"Falló {nombre}\n{detalle[-8000:]}")



def limpiar_titulo(valor):
    if not isinstance(valor, str):
        return ""
    titulo = " ".join(valor.split()).strip(' "“”«»')
    titulo = re.sub(r"^(?:título|titulo)\s*:\s*", "", titulo, flags=re.IGNORECASE)
    if not 2 <= len(titulo.split()) <= 12 or len(titulo) > 100:
        return ""
    if any(c in titulo for c in "{}[]<>`") or not any(c.isalpha() for c in titulo):
        return ""
    if titulo.isupper() or titulo.islower():
        titulo = titulo[:1].upper() + titulo[1:].lower()
    return titulo


def titulo_visible(cuento):
    return limpiar_titulo(cuento.get("titulo")) or "Una historia por descubrir"


def proponer_titulo(cuento, idea="", genero=""):
    escenas = "\n".join(escena["texto"] for escena in cuento["escenas"])
    datos = {
        "model": getattr(motor, "MODELO", "qwen3:1.7b"),
        "prompt": (
            "Escribe un título literario en español para este cuento. "
            "Usa de 2 a 8 palabras y un elemento concreto del relato. "
            "Debe ser claro, legible y corresponder al género. "
            "Usa mayúscula al inicio y en nombres propios. "
            "Devuelve solo un objeto JSON con la clave titulo.\n"
            f"Género: {genero}\nIdea: {idea}\nCuento:\n{escenas}"
        ),
        "format": {"type": "object", "properties": {"titulo": {"type": "string"}}, "required": ["titulo"]},
        "stream": False, "think": False, "keep_alive": 0,
    }
    solicitud = Request(
        getattr(motor, "URL_OLLAMA", "http://127.0.0.1:11434/api/generate"),
        data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urlopen(solicitud, timeout=300) as respuesta:
        resultado = json.load(respuesta)
    titulo = limpiar_titulo(json.loads(resultado["response"]).get("titulo"))
    if not titulo:
        raise ValueError("El modelo devolvió un título que necesita revisión.")
    return titulo


def guardar_cuento(archivo, cuento):
    temporal = archivo.with_name(f".{archivo.name}-{uuid4().hex}.tmp")
    try:
        temporal.write_text(json.dumps(cuento, ensure_ascii=False, indent=2), encoding="utf-8")
        temporal.replace(archivo)
    finally:
        temporal.unlink(missing_ok=True)


def abrir_historia(clave):
    st.session_state.carpeta_cuento = clave
    st.session_state.escena_actual = 0


def elegir_pagina(indice):
    st.session_state.escena_actual = indice


with st.expander("Crear una historia", expanded=not bool(st.session_state.get("carpeta_cuento"))):
    st.markdown('<h1 class="titulo-inicio">Tu próxima historia<br>empieza con una idea.</h1>', unsafe_allow_html=True)
    with st.form("crear_cuento"):
        idea = st.text_area(
            "Idea de la historia",
            placeholder="Una niña descubre que el faro de su pueblo se apagó…",
            height=140,
        )
        genero = st.selectbox(
            "Tipo de historia",
            ["Fantasía", "Aventura", "Misterio", "Infantil", "Terror", "Ciencia ficción"],
        )
        generar = st.form_submit_button("Crear mi historia →", type="primary", use_container_width=True)
if generar:
    if not idea.strip():
        st.warning("Escribe una idea para la historia.")
    else:
        identificador = (
            datetime.now().strftime("%Y%m%d-%H%M%S")
            + "-"
            + uuid4().hex[:6]
        )
        carpeta = CARPETA_CUENTOS / identificador
        animacion = st.empty()
        animacion.markdown(LIBRO_CARGANDO, unsafe_allow_html=True)

        try:
            carpeta.mkdir(parents=True)
            cuento = generar_cuento(idea.strip(), genero)
            try:
                cuento["titulo"] = proponer_titulo(cuento, idea.strip(), genero)
            except Exception:
                cuento["titulo"] = titulo_visible(cuento)
                st.session_state.aviso_titulo = "Se usó un título de respaldo. Puedes proponer otro desde Editar título."
            validar_cuento(cuento)

            (carpeta / "cuento.json").write_text(
                json.dumps(cuento, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            (carpeta / "entrada.json").write_text(
                json.dumps(
                    {"idea": idea.strip(), "genero": genero},
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            for script in ("ilustrar.py", "narrar.py", "ambientar.py"):
                ejecutar_script(script, carpeta)

            for numero in range(1, 6):
                for nombre in (
                    f"escena-{numero:02d}.png",
                    f"voz-{numero:02d}.wav",
                    f"ambiente-{numero:02d}.wav",
                ):
                    archivo = carpeta / nombre
                    if not archivo.is_file() or archivo.stat().st_size == 0:
                        raise RuntimeError(f"Falta el archivo generado {nombre}.")

            (carpeta / "completo.txt").write_text("OK", encoding="utf-8")
            st.session_state.carpeta_cuento = str(carpeta)
            st.session_state.escena_actual = 0
            st.success("El cuento está listo.")

        except Exception as error:
            st.error("La generación se interrumpió.")
            st.code(str(error))
            if carpeta.is_dir():
                st.info(f"Los archivos generados se conservaron en {carpeta}")
        finally:
            animacion.empty()

# La biblioteca usa los títulos del JSON y las ilustraciones como portadas.
cuentos_guardados = sorted(CARPETA_CUENTOS.glob("*/completo.txt"), reverse=True)
archivos = {str(m.parent): m.parent / "cuento.json" for m in cuentos_guardados}
cuento_anterior = CARPETA_CODIGO / "cuento.json"
if cuento_anterior.is_file():
    archivos["anterior"] = cuento_anterior

historias = {}
for clave, archivo in archivos.items():
    try:
        datos = json.loads(archivo.read_text(encoding="utf-8-sig"))
        if not isinstance(datos, dict):
            raise ValueError("El cuento debe ser un objeto JSON.")
        historias[clave] = datos
    except (OSError, ValueError) as error:
        st.warning(f"No se pudo leer {archivo.parent.name}. {error}")

if not historias:
    st.info("Aquí aparecerán tus historias ilustradas.")
    st.stop()

seleccion = st.session_state.get("carpeta_cuento")
if seleccion not in historias:
    seleccion = next(iter(historias))
    st.session_state.carpeta_cuento = seleccion

with st.expander("Tus historias", expanded=False):
    columnas = st.columns(3, gap="large")
    for indice_portada, (clave, datos) in enumerate(historias.items()):
        recursos = SALIDAS if clave == "anterior" else Path(clave)
        with columnas[indice_portada % 3]:
            with st.container(border=True, key=f"portada_{indice_portada}"):
                portada = recursos / "escena-01.png"
                if portada.is_file():
                    st.image(str(portada), width="stretch")
                st.markdown(f'<h3 class="titulo-portada">{escape(titulo_visible(datos))}</h3>', unsafe_allow_html=True)
                st.button("Leer historia →", key=f"abrir_{indice_portada}", on_click=abrir_historia, args=(clave,), use_container_width=True)

if seleccion != st.session_state.get("cuento_visible"):
    st.session_state.cuento_visible = seleccion
    st.session_state.escena_actual = 0

archivo_cuento = archivos[seleccion]
carpeta_recursos = SALIDAS if seleccion == "anterior" else Path(seleccion)
cuento = dict(historias[seleccion])
cuento["titulo"] = titulo_visible(cuento)
try:
    validar_cuento(cuento)
except (ValueError, KeyError, TypeError, AttributeError) as error:
    st.error(f"No se pudo abrir el cuento. {error}")
    st.stop()

if "aviso_titulo" in st.session_state:
    st.info(st.session_state.pop("aviso_titulo"))
st.markdown(f'<h1 class="titulo-cuento">{escape(cuento["titulo"])}</h1>', unsafe_allow_html=True)

with st.expander("Editar título"):
    with st.form(f"titulo_{seleccion}"):
        titulo_editado = st.text_input("Título de la historia", value=cuento["titulo"], max_chars=100)
        guardar = st.form_submit_button("Guardar título")
    if guardar:
        titulo = limpiar_titulo(titulo_editado)
        if not titulo:
            st.warning("Escribe un título de entre 2 y 12 palabras.")
        else:
            try:
                cuento["titulo"] = titulo
                guardar_cuento(archivo_cuento, cuento)
            except OSError as error:
                st.error(f"No se pudo guardar. {error}")
            else:
                st.rerun()
    if st.button("Proponer otro título con IA"):
        animacion = st.empty()
        animacion.markdown(LIBRO_CARGANDO, unsafe_allow_html=True)
        correcto = False
        try:
            cuento["titulo"] = proponer_titulo(cuento)
            guardar_cuento(archivo_cuento, cuento)
            correcto = True
        except Exception as error:
            st.error(f"No se pudo cambiar el título. {error}")
        finally:
            animacion.empty()
        if correcto:
            st.rerun()

indice = st.session_state.escena_actual
numero = indice + 1
escena = cuento["escenas"][indice]
imagen = carpeta_recursos / f"escena-{numero:02d}.png"
voz = carpeta_recursos / f"voz-{numero:02d}.wav"
ambiente = carpeta_recursos / f"ambiente-{numero:02d}.wav"

with st.container(border=True, key="lector"):
    pagina_ilustrada, pagina_lectura = st.columns([1.05, 1], gap="large")
    with pagina_ilustrada:
        if imagen.is_file():
            st.image(str(imagen), width="stretch")
        else:
            st.warning("Falta la imagen de esta escena.")
    with pagina_lectura:
        st.markdown(f'<p class="numero-escena">ESCENA {numero} DE 5</p>', unsafe_allow_html=True)
        parrafos = "".join(f"<p>{escape(p)}</p>" for p in escena["texto"].splitlines() if p.strip())
        st.markdown(f'<div class="texto-cuento">{parrafos}</div>', unsafe_allow_html=True)
        st.caption("NARRACIÓN")
        if voz.is_file():
            st.audio(str(voz), format="audio/wav")
        else:
            st.warning("Falta la narración.")
        st.caption("AMBIENTE SONORO")
        if ambiente.is_file():
            st.audio(str(ambiente), format="audio/wav", loop=True)
        else:
            st.warning("Falta el ambiente.")

anterior, paginas, siguiente = st.columns([1, 2, 1])
with anterior:
    st.button("← Anterior", on_click=cambiar_escena, args=(-1,), disabled=indice == 0, use_container_width=True)
with paginas:
    for posicion, columna in enumerate(st.columns(5)):
        with columna:
            st.button(str(posicion + 1), key=f"pagina_{posicion}", on_click=elegir_pagina, args=(posicion,), type="primary" if posicion == indice else "secondary", use_container_width=True)
with siguiente:
    st.button("Siguiente →", on_click=cambiar_escena, args=(1,), disabled=indice == 4, use_container_width=True)
