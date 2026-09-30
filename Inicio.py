"""
💗 Nube de Mari — Nube de Palabras
Aplicación Streamlit con diseño rosado y creativo

Instalación:
    pip install streamlit wordcloud matplotlib pandas Pillow numpy

Ejecución:
    streamlit run wordcloud_app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
import random
from collections import Counter
from wordcloud import WordCloud, STOPWORDS


def html(codigo):
    """Muestra HTML/CSS. Usa st.html (Streamlit nuevo) y si no existe, st.markdown."""
    if hasattr(st, "html"):
        st.html(codigo)
    else:
        st.markdown(codigo, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Nube de Mari",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — rosado, suave y creativo
# (cambia estos colores si quieres otro tono)
# ─────────────────────────────────────────────
html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Pacifico&display=swap');

    .stApp, .stApp p, .stApp label, .stApp input, .stApp textarea,
    .stApp button, .stApp h1, .stApp h2, .stApp h3, .stApp li {
        font-family: 'Poppins', sans-serif;
    }

    /* Cajas con borde (st.container) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #fbcfe8 !important;
        border-radius: 24px !important;
        background: #ffffff;
        box-shadow: 0 6px 20px rgba(236,72,153,0.08);
    }

    /* Fondo general rosa clarito */
    .stApp {
        background: linear-gradient(180deg, #fff0f6 0%, #ffe4ef 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 2px dashed #f9a8d4;
    }
    [data-testid="stSidebar"] h2 {
        font-family: 'Pacifico', cursive !important;
        color: #db2777 !important;
        font-weight: 400 !important;
        font-size: 1.6rem !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #be185d !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
    }
    [data-testid="stSidebar"] label {
        color: #9d174d !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #fbcfe8 !important;
    }

    /* Inputs */
    textarea, input[type="text"] {
        background-color: #fffafc !important;
        border: 2px solid #fbcfe8 !important;
        border-radius: 14px !important;
        color: #500724 !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #ec4899 !important;
        box-shadow: 0 0 0 3px rgba(236,72,153,0.18) !important;
    }
    [data-baseweb="select"] > div {
        background: #fffafc !important;
        border: 2px solid #fbcfe8 !important;
        border-radius: 14px !important;
    }

    /* Títulos y texto */
    h1, h2, h3 {
        color: #9d174d !important;
        font-weight: 700 !important;
    }
    p, li {
        color: #6b2143 !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #ec4899, #f472b6) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.4rem !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(236,72,153,0.35) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 22px rgba(236,72,153,0.45) !important;
    }
    [data-testid="stDownloadButton"] button {
        background: #ffffff !important;
        color: #db2777 !important;
        border: 2px solid #f472b6 !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        background: #fdf2f8 !important;
        transform: translateY(-2px);
    }

    /* Métricas */
    [data-testid="metric-container"], [data-testid="stMetric"] {
        background: #ffffff;
        border: 2px solid #fbcfe8;
        border-radius: 20px;
        padding: 18px 22px;
        box-shadow: 0 6px 18px rgba(236,72,153,0.10);
    }
    [data-testid="stMetricValue"] {
        color: #db2777 !important;
        font-weight: 700 !important;
    }

    /* Encabezado */
    .header-card {
        background: linear-gradient(135deg, #f472b6 0%, #ec4899 50%, #c084fc 100%);
        border-radius: 28px;
        padding: 38px 40px;
        margin-bottom: 26px;
        box-shadow: 0 12px 30px rgba(236,72,153,0.30);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .header-card h1 {
        font-family: 'Pacifico', cursive !important;
        color: #ffffff !important;
        font-weight: 400 !important;
        font-size: 2.8rem !important;
        margin: 0 !important;
    }
    .header-card p {
        color: #fff0f6 !important;
        font-size: 1.05rem !important;
        margin: 8px 0 0 0 !important;
    }
    .corazones {
        position: absolute;
        font-size: 1.4rem;
        opacity: 0.55;
        animation: flotar 4s ease-in-out infinite;
    }
    @keyframes flotar {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-10px); }
    }

    /* Tarjetas */
    .section-card {
        background: #ffffff;
        border: 2px solid #fbcfe8;
        border-radius: 24px;
        padding: 24px 28px;
        margin-bottom: 16px;
        box-shadow: 0 6px 20px rgba(236,72,153,0.08);
    }
    .info-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 16px;
        background: #fdf2f8;
        border-radius: 16px;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .info-item:hover { transform: translateX(6px); }

    .uso-tag {
        display: inline-block;
        background: #fce7f3;
        border: 1px solid #f9a8d4;
        border-radius: 999px;
        padding: 6px 14px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #9d174d;
        margin: 4px 3px;
    }

    /* Barras de frecuencia */
    .freq-row {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 14px;
        margin: 5px 0;
        background: #ffffff;
        border: 1px solid #fce7f3;
        border-radius: 14px;
        transition: background 0.15s, transform 0.15s;
    }
    .freq-row:hover { background: #fdf2f8; transform: translateX(4px); }
    .freq-bar {
        height: 10px;
        background: linear-gradient(90deg, #f9a8d4, #ec4899);
        border-radius: 999px;
        display: inline-block;
    }
    .rank-tag {
        background: #fce7f3;
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #db2777;
        min-width: 40px;
        text-align: center;
    }

    /* Paleta en bienvenida */
    .swatch {
        display: inline-block;
        width: 18px; height: 18px;
        border-radius: 50%;
        margin-right: 3px;
        border: 2px solid #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.15);
    }

    div[data-testid="stExpander"] {
        border: 2px solid #fbcfe8 !important;
        border-radius: 18px !important;
        background: #ffffff !important;
    }
    hr { border-color: #fbcfe8 !important; }

    .wc-container {
        background: #ffffff;
        border: 2px solid #fbcfe8;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(236,72,153,0.12);
        margin-bottom: 16px;
    }

    .footer {
        text-align: center;
        color: #db2777;
        font-size: 0.9rem;
        padding: 20px 0 6px 0;
    }
</style>
""")


# ─────────────────────────────────────────────
# STOPWORDS (palabras que se ignoran)
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","más","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","también","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","así","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
    "ellos","ellas","nosotros","les","esa","esos","esas","aquel","aquella","aquellos",
    "mi","mis","tu","tus","te","yo","uno","dos","cual","cómo","qué",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw


# ─────────────────────────────────────────────
# PALETAS (colores de la nube)
# Agrega las tuyas copiando una línea
# ─────────────────────────────────────────────
PALETAS = {
    "Rosa Mari 💗":      ["#831843","#9d174d","#be185d","#db2777","#ec4899","#f472b6","#f9a8d4"],
    "Barbie 💖":         ["#ff1493","#ff69b4","#e0218a","#fc0fc0","#c71585","#ff85c0"],
    "Algodón de azúcar": ["#f9a8d4","#c4b5fd","#93c5fd","#fbcfe8","#a78bfa","#f472b6"],
    "Rosa y negro 🖤":   ["#000000","#1f1f1f","#db2777","#ec4899","#9d174d","#3f0d23"],
    "Atardecer 🌅":      ["#f43f5e","#fb7185","#f97316","#fbbf24","#ec4899","#be123c"],
    "Lila soñado 💜":    ["#581c87","#7e22ce","#a855f7","#c084fc","#d8b4fe","#db2777"],
    "Fresa y crema 🍓":  ["#be123c","#e11d48","#fb7185","#fda4af","#9f1239","#f472b6"],
}

FONDOS = {
    "Blanco":        "#ffffff",
    "Rosa clarito":  "#fff0f6",
    "Negro":         "#000000",
}

FORMAS = {
    "Corazón 💗":  "heart",
    "Círculo ⚪":  "circle",
    "Estrella ⭐": "star",
    "Rectángulo":  None,
}


def crear_mascara(forma, size=600):
    """Crea la figura de la nube. 0 = donde van palabras, 255 = vacío."""
    if forma is None:
        return None

    mascara = np.ones((size, size), dtype=np.uint8) * 255

    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        c = size // 2
        mascara[(x - c) ** 2 + (y - c) ** 2 <= (c - 12) ** 2] = 0

    elif forma == "heart":
        # Ecuación del corazón: (x² + y² - 1)³ - x²·y³ ≤ 0
        lin = np.linspace(-1.35, 1.35, size)
        x, y = np.meshgrid(lin, -lin)
        y = y + 0.15
        dentro = (x ** 2 + y ** 2 - 1) ** 3 - (x ** 2) * (y ** 3) <= 0
        mascara[dentro] = 0

    elif forma == "star":
        from PIL import Image, ImageDraw
        img = Image.new("L", (size, size), 255)
        draw = ImageDraw.Draw(img)
        c, r_ext, r_int = size / 2, size / 2 - 10, size / 4.6
        puntos = []
        for i in range(10):
            ang = np.pi / 2 + i * np.pi / 5
            r = r_ext if i % 2 == 0 else r_int
            puntos.append((c + r * np.cos(ang), c - r * np.sin(ang)))
        draw.polygon(puntos, fill=0)
        mascara = np.array(img)

    return mascara


# ─────────────────────────────────────────────
# FUNCIONES PRINCIPALES
# ─────────────────────────────────────────────
def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñàâèêîôùûäëïöü\s]", " ", texto, flags=re.UNICODE)
    palabras = [p for p in texto.split() if p not in stopwords and len(p) >= min_longitud]
    return " ".join(palabras)


def contar_palabras(texto_limpio):
    return pd.DataFrame(Counter(texto_limpio.split()).most_common(50),
                        columns=["Palabra", "Frecuencia"])


def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma):
    colores = PALETAS[paleta_nombre]

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        rng = random_state or random.Random()
        return colores[rng.randint(0, len(colores) - 1)]

    mascara = crear_mascara(forma)
    if mascara is not None:
        ancho, alto = 800, 800
    else:
        ancho, alto = 1000, 520

    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words,
        background_color=fondo, color_func=color_func,
        mask=mascara, collocations=False,
        min_font_size=10, max_font_size=130,
        prefer_horizontal=0.8, relative_scaling=0.5, margin=4,
    ).generate(texto_limpio)

    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig


def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# PANEL LATERAL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Nube de Mari")
    st.caption("Convierte cualquier texto en arte ✨")
    st.divider()

    st.markdown("### 💬 Tu texto")
    fuente = st.radio("fuente", ["✍️ Escribir / Pegar", "📂 Subir archivo"],
                      label_visibility="collapsed")
    texto_input = ""

    if fuente == "✍️ Escribir / Pegar":
        texto_input = st.text_area(
            "Texto:", height=190,
            placeholder="Pega aquí una canción, un artículo, reseñas, tu diario... 💌")

        with st.expander("🎀 Cargar un texto de ejemplo"):
            ejemplos = {
                "Maquillaje 💄": """
                El maquillaje es arte, color y expresión. Una buena base ilumina la piel,
                el rubor da vida a las mejillas y el labial rosado completa el look.
                Las sombras brillantes, el delineado y las pestañas largas transforman la mirada.
                El skincare prepara la piel: limpieza, hidratación y protector solar todos los días.
                Glow, brillo, iluminador y rubor son claves para una piel radiante.
                El maquillaje natural resalta la belleza, el maquillaje artístico expresa creatividad.
                Colores rosados, nudes y dorados combinan con cualquier estilo y ocasión.
                """,
                "Medellín 🌸": """
                Medellín es la ciudad de la eterna primavera, famosa por sus flores, su clima
                y la calidez de su gente. La Feria de las Flores llena la ciudad de color,
                silleteros y alegría. El Metro de Medellín es orgullo paisa y conecta la ciudad
                con los metrocables que suben a las montañas. Comuna 13, el Parque Arví,
                el Pueblito Paisa y el Parque Explora son lugares llenos de cultura, arte
                y creatividad. La innovación, el emprendimiento y el diseño crecen en Medellín.
                """,
                "Inteligencia Artificial 🤖": """
                La inteligencia artificial permite crear aplicaciones creativas que convierten
                texto en voz, voz en texto, traducen idiomas y reconocen imágenes.
                Con Python y Streamlit es posible diseñar apps interactivas en pocos minutos.
                El aprendizaje automático, las redes neuronales y el procesamiento del lenguaje
                natural son la base de los asistentes inteligentes. La inteligencia artificial
                transforma el diseño, la educación, la salud y los negocios digitales.
                """,
            }
            ejemplo_sel = st.selectbox("Ejemplo:", list(ejemplos.keys()),
                                       label_visibility="collapsed")
            if st.button("Usar este ejemplo"):
                st.session_state["texto_ejemplo"] = ejemplos[ejemplo_sel]
                st.rerun()

        if "texto_ejemplo" in st.session_state and not texto_input:
            texto_input = st.session_state["texto_ejemplo"]

    else:
        archivo = st.file_uploader("Archivo:", type=["txt", "csv"],
                                   label_visibility="collapsed")
        if archivo:
            if archivo.name.endswith(".txt"):
                texto_input = archivo.read().decode("utf-8", errors="ignore")
            elif archivo.name.endswith(".csv"):
                df_csv = pd.read_csv(archivo)
                col_txt = st.selectbox("Columna de texto:", df_csv.columns.tolist())
                texto_input = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
            st.success(f"Archivo cargado 💗 {len(texto_input):,} caracteres")

    st.divider()

    st.markdown("### 🧹 Limpieza")
    idioma         = st.selectbox("Ignorar palabras comunes en:", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud   = st.slider("Largo mínimo de palabra", 2, 8, 3)
    palabras_extra = st.text_input("Otras palabras a quitar:",
                                   placeholder="ej: bueno, cosa, entonces")

    st.divider()

    st.markdown("### 🎨 Diseño")
    paleta_sel = st.selectbox("Paleta:", list(PALETAS.keys()))
    fondo_sel  = st.radio("Fondo:", list(FONDOS.keys()), horizontal=True)
    forma_sel  = st.selectbox("Forma:", list(FORMAS.keys()))
    max_words  = st.slider("Máximo de palabras:", 20, 200, 90)

    st.divider()
    generar = st.button("✨ CREAR MI NUBE ✨", use_container_width=True)


# ─────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────
html("""
<div class="header-card">
    <span class="corazones" style="top:18px; left:30px;">💗</span>
    <span class="corazones" style="top:60px; right:50px; animation-delay:1s;">✨</span>
    <span class="corazones" style="bottom:18px; left:22%; animation-delay:2s;">🌸</span>
    <span class="corazones" style="bottom:22px; right:24%; animation-delay:1.5s;">💖</span>
    <h1>Nube de Mari</h1>
    <p>Descubre las palabras que más se repiten en cualquier texto y conviértelas en arte 💌</p>
</div>
""")


# ─────────────────────────────────────────────
# PANTALLA DE BIENVENIDA
# ─────────────────────────────────────────────
if not generar or not texto_input.strip():
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        st.markdown("### 💭 ¿Qué es una nube de palabras?")
        st.markdown(
            "Es una imagen donde **las palabras que más se repiten salen más grandes**. "
            "Sirve para ver de un vistazo de qué habla un texto."
        )

        for icono, titulo, desc in [
            ("📊", "Cuenta palabras", "Encuentra las palabras más usadas en tu texto."),
            ("🧹", "Limpia el texto", "Quita palabras comunes como 'de', 'la', 'que'."),
            ("🎀", "Tú eliges el estilo", "Paletas rosadas, forma de corazón, estrella y más."),
            ("💾", "Descarga", "Guarda tu nube en PNG y la tabla de palabras en CSV."),
        ]:
            html(
                f'<div class="info-item">'
                f'<span style="font-size:1.4rem;">{icono}</span>'
                f'<div><strong style="color:#9d174d;">{titulo}</strong>'
                f'<p style="margin:2px 0 0 0; font-size:0.88rem;">{desc}</p></div>'
                f'</div>',
            )

        st.markdown("### 📝 Cómo usarla")
        for i, paso in enumerate([
            "Escribe, pega o sube tu texto en el panel de la izquierda.",
            "Elige tu paleta, fondo y forma favorita.",
            "Dale a **✨ CREAR MI NUBE ✨**.",
            "Descarga tu imagen y compártela 💗",
        ], 1):
            st.markdown(f"**{i}.** {paso}")

    with col_der:
        with st.container(border=True):
            st.markdown("### 💡 Ideas para usarla")
            etiquetas = "".join(f'<span class="uso-tag">{caso}</span>' for caso in [
                "🎵 Letras de canciones", "💬 Reseñas de clientes", "📰 Noticias",
                "📋 Encuestas", "📚 Textos de clase", "💌 Tu diario", "🛍️ Comentarios de redes",
            ])
            html(f"<div>{etiquetas}</div>")

        with st.container(border=True):
            st.markdown("### 🎨 Paletas")
            filas = ""
            for nombre, colores in PALETAS.items():
                bolitas = "".join(f'<span class="swatch" style="background:{c};"></span>' for c in colores)
                filas += (
                    f'<div style="padding:6px 0;">{bolitas}'
                    f'<span style="color:#9d174d; font-size:0.88rem; font-weight:500; margin-left:8px;">{nombre}</span>'
                    f'</div>'
                )
            html(filas)

    if generar and not texto_input.strip():
        st.warning("Escribe o pega un texto en el panel de la izquierda primero 💗")
    st.stop()


# ─────────────────────────────────────────────
# PROCESAMIENTO
# ─────────────────────────────────────────────
stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
if palabras_extra.strip():
    stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

texto_limpio = limpiar_texto(texto_input, stopwords_set, min_longitud)

if not texto_limpio.strip():
    st.error("No quedaron palabras 😢 Baja el largo mínimo o cambia las palabras a ignorar.")
    st.stop()

df_freq        = contar_palabras(texto_limpio)
total_palabras = len(texto_limpio.split())
vocabulario    = len(set(texto_limpio.split()))

m1, m2, m3, m4 = st.columns(4)
m1.metric("💬 Palabras", f"{total_palabras:,}")
m2.metric("🌸 Palabras distintas", f"{vocabulario:,}")
m3.metric("👑 La reina", df_freq.iloc[0]["Palabra"])
m4.metric("🔁 Se repite", int(df_freq.iloc[0]["Frecuencia"]))

st.write("")

# ── Nube ──
with st.spinner("Creando tu nube con amor 💗..."):
    fig_wc = generar_wordcloud(
        texto_limpio, paleta_sel, max_words, FONDOS[fondo_sel], FORMAS[forma_sel]
    )

with st.container(border=True):
    st.markdown(f"**Tu nube** · {paleta_sel} · {forma_sel} · fondo {fondo_sel.lower()}")
    c1, c2, c3 = st.columns([1, 4, 1]) if FORMAS[forma_sel] else st.columns([0.01, 1, 0.01])
    with c2:
        st.pyplot(fig_wc, use_container_width=True)

st.download_button(
    "💾 Descargar mi nube (PNG)",
    data=fig_a_bytes(fig_wc), file_name="nube_de_mari.png", mime="image/png",
    use_container_width=True,
)

st.balloons()
st.divider()

# ── Análisis ──
col_freq, col_tabla = st.columns([3, 2], gap="large")

with col_freq:
    st.markdown("### 🏆 Top 20 palabras")
    top20    = df_freq.head(20)
    max_freq = top20["Frecuencia"].max()

    for rank, (_, row) in enumerate(top20.iterrows(), 1):
        p = row["Palabra"]
        f = int(row["Frecuencia"])
        barra_w = max(14, int((f / max_freq) * 220))
        medalla = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank:02d}")
        html(
            f'<div class="freq-row">'
            f'<span class="rank-tag">{medalla}</span>'
            f'<span style="font-weight:600; color:#831843; min-width:130px;">{p}</span>'
            f'<div class="freq-bar" style="width:{barra_w}px;"></div>'
            f'<span style="color:#db2777; font-weight:700; min-width:28px; text-align:right;">{f}</span>'
            f'</div>',
        )

with col_tabla:
    st.markdown("### 📋 Tabla de palabras")
    st.dataframe(
        df_freq.head(30).style
               .background_gradient(subset=["Frecuencia"], cmap="RdPu")
               .format({"Frecuencia": "{:,}"}),
        use_container_width=True, height=500,
    )
    st.download_button(
        "💾 Descargar tabla (CSV)",
        data=df_freq.to_csv(index=False).encode("utf-8"),
        file_name="palabras_mari.csv", mime="text/csv",
        use_container_width=True,
    )

st.divider()

with st.expander("👀 Ver el texto limpio"):
    preview = texto_limpio[:2500] + ("..." if len(texto_limpio) > 2500 else "")
    html(
        f'<p style="background:#fdf2f8; padding:16px; border-radius:16px; line-height:1.8;">{preview}</p>',
    )

html('<div class="footer">Hecho con 💗 por Mari</div>')

plt.close("all")        letter-spacing: 1.2px !important;
    }
    [data-testid="stSidebar"] label {
        color: #9d174d !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #fbcfe8 !important;
    }

    /* Inputs */
    textarea, input[type="text"] {
        background-color: #fffafc !important;
        border: 2px solid #fbcfe8 !important;
        border-radius: 14px !important;
        color: #500724 !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #ec4899 !important;
        box-shadow: 0 0 0 3px rgba(236,72,153,0.18) !important;
    }
    [data-baseweb="select"] > div {
        background: #fffafc !important;
        border: 2px solid #fbcfe8 !important;
        border-radius: 14px !important;
    }

    /* Títulos y texto */
    h1, h2, h3 {
        color: #9d174d !important;
        font-weight: 700 !important;
    }
    p, li {
        color: #6b2143 !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #ec4899, #f472b6) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.4rem !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(236,72,153,0.35) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 22px rgba(236,72,153,0.45) !important;
    }
    [data-testid="stDownloadButton"] button {
        background: #ffffff !important;
        color: #db2777 !important;
        border: 2px solid #f472b6 !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        background: #fdf2f8 !important;
        transform: translateY(-2px);
    }

    /* Métricas */
    [data-testid="metric-container"], [data-testid="stMetric"] {
        background: #ffffff;
        border: 2px solid #fbcfe8;
        border-radius: 20px;
        padding: 18px 22px;
        box-shadow: 0 6px 18px rgba(236,72,153,0.10);
    }
    [data-testid="stMetricValue"] {
        color: #db2777 !important;
        font-weight: 700 !important;
    }

    /* Encabezado */
    .header-card {
        background: linear-gradient(135deg, #f472b6 0%, #ec4899 50%, #c084fc 100%);
        border-radius: 28px;
        padding: 38px 40px;
        margin-bottom: 26px;
        box-shadow: 0 12px 30px rgba(236,72,153,0.30);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .header-card h1 {
        font-family: 'Pacifico', cursive !important;
        color: #ffffff !important;
        font-weight: 400 !important;
        font-size: 2.8rem !important;
        margin: 0 !important;
    }
    .header-card p {
        color: #fff0f6 !important;
        font-size: 1.05rem !important;
        margin: 8px 0 0 0 !important;
    }
    .corazones {
        position: absolute;
        font-size: 1.4rem;
        opacity: 0.55;
        animation: flotar 4s ease-in-out infinite;
    }
    @keyframes flotar {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-10px); }
    }

    /* Tarjetas */
    .section-card {
        background: #ffffff;
        border: 2px solid #fbcfe8;
        border-radius: 24px;
        padding: 24px 28px;
        margin-bottom: 16px;
        box-shadow: 0 6px 20px rgba(236,72,153,0.08);
    }
    .info-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 16px;
        background: #fdf2f8;
        border-radius: 16px;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .info-item:hover { transform: translateX(6px); }

    .uso-tag {
        display: inline-block;
        background: #fce7f3;
        border: 1px solid #f9a8d4;
        border-radius: 999px;
        padding: 6px 14px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #9d174d;
        margin: 4px 3px;
    }

    /* Barras de frecuencia */
    .freq-row {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 14px;
        margin: 5px 0;
        background: #ffffff;
        border: 1px solid #fce7f3;
        border-radius: 14px;
        transition: background 0.15s, transform 0.15s;
    }
    .freq-row:hover { background: #fdf2f8; transform: translateX(4px); }
    .freq-bar {
        height: 10px;
        background: linear-gradient(90deg, #f9a8d4, #ec4899);
        border-radius: 999px;
        display: inline-block;
    }
    .rank-tag {
        background: #fce7f3;
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #db2777;
        min-width: 40px;
        text-align: center;
    }

    /* Paleta en bienvenida */
    .swatch {
        display: inline-block;
        width: 18px; height: 18px;
        border-radius: 50%;
        margin-right: 3px;
        border: 2px solid #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.15);
    }

    div[data-testid="stExpander"] {
        border: 2px solid #fbcfe8 !important;
        border-radius: 18px !important;
        background: #ffffff !important;
    }
    hr { border-color: #fbcfe8 !important; }

    .wc-container {
        background: #ffffff;
        border: 2px solid #fbcfe8;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(236,72,153,0.12);
        margin-bottom: 16px;
    }

    .footer {
        text-align: center;
        color: #db2777;
        font-size: 0.9rem;
        padding: 20px 0 6px 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STOPWORDS (palabras que se ignoran)
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","más","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","también","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","así","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
    "ellos","ellas","nosotros","les","esa","esos","esas","aquel","aquella","aquellos",
    "mi","mis","tu","tus","te","yo","uno","dos","cual","cómo","qué",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw


# ─────────────────────────────────────────────
# PALETAS (colores de la nube)
# Agrega las tuyas copiando una línea
# ─────────────────────────────────────────────
PALETAS = {
    "Rosa Mari 💗":      ["#831843","#9d174d","#be185d","#db2777","#ec4899","#f472b6","#f9a8d4"],
    "Barbie 💖":         ["#ff1493","#ff69b4","#e0218a","#fc0fc0","#c71585","#ff85c0"],
    "Algodón de azúcar": ["#f9a8d4","#c4b5fd","#93c5fd","#fbcfe8","#a78bfa","#f472b6"],
    "Rosa y negro 🖤":   ["#000000","#1f1f1f","#db2777","#ec4899","#9d174d","#3f0d23"],
    "Atardecer 🌅":      ["#f43f5e","#fb7185","#f97316","#fbbf24","#ec4899","#be123c"],
    "Lila soñado 💜":    ["#581c87","#7e22ce","#a855f7","#c084fc","#d8b4fe","#db2777"],
    "Fresa y crema 🍓":  ["#be123c","#e11d48","#fb7185","#fda4af","#9f1239","#f472b6"],
}

FONDOS = {
    "Blanco":        "#ffffff",
    "Rosa clarito":  "#fff0f6",
    "Negro":         "#000000",
}

FORMAS = {
    "Corazón 💗":  "heart",
    "Círculo ⚪":  "circle",
    "Estrella ⭐": "star",
    "Rectángulo":  None,
}


def crear_mascara(forma, size=600):
    """Crea la figura de la nube. 0 = donde van palabras, 255 = vacío."""
    if forma is None:
        return None

    mascara = np.ones((size, size), dtype=np.uint8) * 255

    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        c = size // 2
        mascara[(x - c) ** 2 + (y - c) ** 2 <= (c - 12) ** 2] = 0

    elif forma == "heart":
        # Ecuación del corazón: (x² + y² - 1)³ - x²·y³ ≤ 0
        lin = np.linspace(-1.35, 1.35, size)
        x, y = np.meshgrid(lin, -lin)
        y = y + 0.15
        dentro = (x ** 2 + y ** 2 - 1) ** 3 - (x ** 2) * (y ** 3) <= 0
        mascara[dentro] = 0

    elif forma == "star":
        from PIL import Image, ImageDraw
        img = Image.new("L", (size, size), 255)
        draw = ImageDraw.Draw(img)
        c, r_ext, r_int = size / 2, size / 2 - 10, size / 4.6
        puntos = []
        for i in range(10):
            ang = np.pi / 2 + i * np.pi / 5
            r = r_ext if i % 2 == 0 else r_int
            puntos.append((c + r * np.cos(ang), c - r * np.sin(ang)))
        draw.polygon(puntos, fill=0)
        mascara = np.array(img)

    return mascara


# ─────────────────────────────────────────────
# FUNCIONES PRINCIPALES
# ─────────────────────────────────────────────
def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñàâèêîôùûäëïöü\s]", " ", texto, flags=re.UNICODE)
    palabras = [p for p in texto.split() if p not in stopwords and len(p) >= min_longitud]
    return " ".join(palabras)


def contar_palabras(texto_limpio):
    return pd.DataFrame(Counter(texto_limpio.split()).most_common(50),
                        columns=["Palabra", "Frecuencia"])


def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma):
    colores = PALETAS[paleta_nombre]

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        rng = random_state or random.Random()
        return colores[rng.randint(0, len(colores) - 1)]

    mascara = crear_mascara(forma)
    if mascara is not None:
        ancho, alto = 800, 800
    else:
        ancho, alto = 1000, 520

    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words,
        background_color=fondo, color_func=color_func,
        mask=mascara, collocations=False,
        min_font_size=10, max_font_size=130,
        prefer_horizontal=0.8, relative_scaling=0.5, margin=4,
    ).generate(texto_limpio)

    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig


def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# PANEL LATERAL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Nube de Mari")
    st.caption("Convierte cualquier texto en arte ✨")
    st.divider()

    st.markdown("### 💬 Tu texto")
    fuente = st.radio("fuente", ["✍️ Escribir / Pegar", "📂 Subir archivo"],
                      label_visibility="collapsed")
    texto_input = ""

    if fuente == "✍️ Escribir / Pegar":
        texto_input = st.text_area(
            "Texto:", height=190,
            placeholder="Pega aquí una canción, un artículo, reseñas, tu diario... 💌")

        with st.expander("🎀 Cargar un texto de ejemplo"):
            ejemplos = {
                "Maquillaje 💄": """
                El maquillaje es arte, color y expresión. Una buena base ilumina la piel,
                el rubor da vida a las mejillas y el labial rosado completa el look.
                Las sombras brillantes, el delineado y las pestañas largas transforman la mirada.
                El skincare prepara la piel: limpieza, hidratación y protector solar todos los días.
                Glow, brillo, iluminador y rubor son claves para una piel radiante.
                El maquillaje natural resalta la belleza, el maquillaje artístico expresa creatividad.
                Colores rosados, nudes y dorados combinan con cualquier estilo y ocasión.
                """,
                "Medellín 🌸": """
                Medellín es la ciudad de la eterna primavera, famosa por sus flores, su clima
                y la calidez de su gente. La Feria de las Flores llena la ciudad de color,
                silleteros y alegría. El Metro de Medellín es orgullo paisa y conecta la ciudad
                con los metrocables que suben a las montañas. Comuna 13, el Parque Arví,
                el Pueblito Paisa y el Parque Explora son lugares llenos de cultura, arte
                y creatividad. La innovación, el emprendimiento y el diseño crecen en Medellín.
                """,
                "Inteligencia Artificial 🤖": """
                La inteligencia artificial permite crear aplicaciones creativas que convierten
                texto en voz, voz en texto, traducen idiomas y reconocen imágenes.
                Con Python y Streamlit es posible diseñar apps interactivas en pocos minutos.
                El aprendizaje automático, las redes neuronales y el procesamiento del lenguaje
                natural son la base de los asistentes inteligentes. La inteligencia artificial
                transforma el diseño, la educación, la salud y los negocios digitales.
                """,
            }
            ejemplo_sel = st.selectbox("Ejemplo:", list(ejemplos.keys()),
                                       label_visibility="collapsed")
            if st.button("Usar este ejemplo"):
                st.session_state["texto_ejemplo"] = ejemplos[ejemplo_sel]
                st.rerun()

        if "texto_ejemplo" in st.session_state and not texto_input:
            texto_input = st.session_state["texto_ejemplo"]

    else:
        archivo = st.file_uploader("Archivo:", type=["txt", "csv"],
                                   label_visibility="collapsed")
        if archivo:
            if archivo.name.endswith(".txt"):
                texto_input = archivo.read().decode("utf-8", errors="ignore")
            elif archivo.name.endswith(".csv"):
                df_csv = pd.read_csv(archivo)
                col_txt = st.selectbox("Columna de texto:", df_csv.columns.tolist())
                texto_input = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
            st.success(f"Archivo cargado 💗 {len(texto_input):,} caracteres")

    st.divider()

    st.markdown("### 🧹 Limpieza")
    idioma         = st.selectbox("Ignorar palabras comunes en:", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud   = st.slider("Largo mínimo de palabra", 2, 8, 3)
    palabras_extra = st.text_input("Otras palabras a quitar:",
                                   placeholder="ej: bueno, cosa, entonces")

    st.divider()

    st.markdown("### 🎨 Diseño")
    paleta_sel = st.selectbox("Paleta:", list(PALETAS.keys()))
    fondo_sel  = st.radio("Fondo:", list(FONDOS.keys()), horizontal=True)
    forma_sel  = st.selectbox("Forma:", list(FORMAS.keys()))
    max_words  = st.slider("Máximo de palabras:", 20, 200, 90)

    st.divider()
    generar = st.button("✨ CREAR MI NUBE ✨", use_container_width=True)


# ─────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-card">
    <span class="corazones" style="top:18px; left:30px;">💗</span>
    <span class="corazones" style="top:60px; right:50px; animation-delay:1s;">✨</span>
    <span class="corazones" style="bottom:18px; left:22%; animation-delay:2s;">🌸</span>
    <span class="corazones" style="bottom:22px; right:24%; animation-delay:1.5s;">💖</span>
    <h1>Nube de Mari</h1>
    <p>Descubre las palabras que más se repiten en cualquier texto y conviértelas en arte 💌</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PANTALLA DE BIENVENIDA
# ─────────────────────────────────────────────
if not generar or not texto_input.strip():
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        st.markdown("### 💭 ¿Qué es una nube de palabras?")
        st.markdown(
            "Es una imagen donde **las palabras que más se repiten salen más grandes**. "
            "Sirve para ver de un vistazo de qué habla un texto."
        )

        for icono, titulo, desc in [
            ("📊", "Cuenta palabras", "Encuentra las palabras más usadas en tu texto."),
            ("🧹", "Limpia el texto", "Quita palabras comunes como 'de', 'la', 'que'."),
            ("🎀", "Tú eliges el estilo", "Paletas rosadas, forma de corazón, estrella y más."),
            ("💾", "Descarga", "Guarda tu nube en PNG y la tabla de palabras en CSV."),
        ]:
            st.markdown(
                f'<div class="info-item">'
                f'<span style="font-size:1.4rem;">{icono}</span>'
                f'<div><strong style="color:#9d174d;">{titulo}</strong>'
                f'<p style="margin:2px 0 0 0; font-size:0.88rem;">{desc}</p></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("### 📝 Cómo usarla")
        for i, paso in enumerate([
            "Escribe, pega o sube tu texto en el panel de la izquierda.",
            "Elige tu paleta, fondo y forma favorita.",
            "Dale a **✨ CREAR MI NUBE ✨**.",
            "Descarga tu imagen y compártela 💗",
        ], 1):
            st.markdown(f"**{i}.** {paso}")

    with col_der:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 💡 Ideas para usarla")
        for caso in [
            "🎵 Letras de canciones", "💬 Reseñas de clientes", "📰 Noticias",
            "📋 Encuestas", "📚 Textos de clase", "💌 Tu diario", "🛍️ Comentarios de redes",
        ]:
            st.markdown(f'<span class="uso-tag">{caso}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🎨 Paletas")
        for nombre, colores in PALETAS.items():
            bolitas = "".join(f'<span class="swatch" style="background:{c};"></span>' for c in colores)
            st.markdown(
                f'<div style="padding:6px 0;">{bolitas}'
                f'<span style="color:#9d174d; font-size:0.88rem; font-weight:500; margin-left:8px;">{nombre}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    if generar and not texto_input.strip():
        st.warning("Escribe o pega un texto en el panel de la izquierda primero 💗")
    st.stop()


# ─────────────────────────────────────────────
# PROCESAMIENTO
# ─────────────────────────────────────────────
stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
if palabras_extra.strip():
    stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

texto_limpio = limpiar_texto(texto_input, stopwords_set, min_longitud)

if not texto_limpio.strip():
    st.error("No quedaron palabras 😢 Baja el largo mínimo o cambia las palabras a ignorar.")
    st.stop()

df_freq        = contar_palabras(texto_limpio)
total_palabras = len(texto_limpio.split())
vocabulario    = len(set(texto_limpio.split()))

m1, m2, m3, m4 = st.columns(4)
m1.metric("💬 Palabras", f"{total_palabras:,}")
m2.metric("🌸 Palabras distintas", f"{vocabulario:,}")
m3.metric("👑 La reina", df_freq.iloc[0]["Palabra"])
m4.metric("🔁 Se repite", int(df_freq.iloc[0]["Frecuencia"]))

st.markdown("<br>", unsafe_allow_html=True)

# ── Nube ──
with st.spinner("Creando tu nube con amor 💗..."):
    fig_wc = generar_wordcloud(
        texto_limpio, paleta_sel, max_words, FONDOS[fondo_sel], FORMAS[forma_sel]
    )

st.markdown('<div class="wc-container">', unsafe_allow_html=True)
st.markdown(f"**Tu nube** · {paleta_sel} · {forma_sel} · fondo {fondo_sel.lower()}")
c1, c2, c3 = st.columns([1, 4, 1]) if FORMAS[forma_sel] else st.columns([0.01, 1, 0.01])
with c2:
    st.pyplot(fig_wc, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.download_button(
    "💾 Descargar mi nube (PNG)",
    data=fig_a_bytes(fig_wc), file_name="nube_de_mari.png", mime="image/png",
    use_container_width=True,
)

st.balloons()
st.divider()

# ── Análisis ──
col_freq, col_tabla = st.columns([3, 2], gap="large")

with col_freq:
    st.markdown("### 🏆 Top 20 palabras")
    top20    = df_freq.head(20)
    max_freq = top20["Frecuencia"].max()

    for rank, (_, row) in enumerate(top20.iterrows(), 1):
        p = row["Palabra"]
        f = int(row["Frecuencia"])
        barra_w = max(14, int((f / max_freq) * 220))
        medalla = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank:02d}")
        st.markdown(
            f'<div class="freq-row">'
            f'<span class="rank-tag">{medalla}</span>'
            f'<span style="font-weight:600; color:#831843; min-width:130px;">{p}</span>'
            f'<div class="freq-bar" style="width:{barra_w}px;"></div>'
            f'<span style="color:#db2777; font-weight:700; min-width:28px; text-align:right;">{f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_tabla:
    st.markdown("### 📋 Tabla de palabras")
    st.dataframe(
        df_freq.head(30).style
               .background_gradient(subset=["Frecuencia"], cmap="RdPu")
               .format({"Frecuencia": "{:,}"}),
        use_container_width=True, height=500,
    )
    st.download_button(
        "💾 Descargar tabla (CSV)",
        data=df_freq.to_csv(index=False).encode("utf-8"),
        file_name="palabras_mari.csv", mime="text/csv",
        use_container_width=True,
    )

st.divider()

with st.expander("👀 Ver el texto limpio"):
    preview = texto_limpio[:2500] + ("..." if len(texto_limpio) > 2500 else "")
    st.markdown(
        f'<p style="background:#fdf2f8; padding:16px; border-radius:16px; line-height:1.8;">{preview}</p>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="footer">Hecho con 💗 por Mari</div>', unsafe_allow_html=True)

plt.close("all")
