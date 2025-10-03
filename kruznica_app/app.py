import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import os
import pandas as pd
text = text.encode('latin-1', 'replace').decode('latin-1')
# ------------------------------------------------
# Funkcia na výpočet súradníc bodov
# ------------------------------------------------
def calculate_points(radius, points):
    theta_points = np.linspace(0, 2 * np.pi, points, endpoint=False)
    x_points = radius * np.cos(theta_points)
    y_points = radius * np.sin(theta_points)
    return x_points, y_points

# ------------------------------------------------
# Funkcia na vykreslenie kružnice
# ------------------------------------------------
def draw_circle(radius, points, color="red"):
    # husté body pre hladký kruh
    theta_circle = np.linspace(0, 2 * np.pi, 500)
    x_circle = radius * np.cos(theta_circle)
    y_circle = radius * np.sin(theta_circle)

    # body na kružnici
    x_points, y_points = calculate_points(radius, points)

    fig, ax = plt.subplots()
    ax.plot(x_circle, y_circle, 'b-')        # kruh
    ax.scatter(x_points, y_points, c=color)  # vyznačené body

    # číslovanie bodov
    for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
        ax.text(x, y, str(i), fontsize=10, ha='right', va='bottom')

    # Grid
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

    # Rovnaké mierky
    ax.set_aspect("equal", adjustable="box")

    # Nastav rozsah podľa veľkosti kruhu
    margin = radius * 0.3
    ax.set_xlim(-radius - margin, radius + margin)
    ax.set_ylim(-radius - margin, radius + margin)

    return fig, x_points, y_points

# ------------------------------------------------
# Funkcia na export do PDF
# ------------------------------------------------
def export_pdf(radius, points, x_points, y_points, img_path="circle.png", pdf_path="circle.pdf"):
    # Uloženie obrázka kružnice
    fig, _, _ = draw_circle(radius, points)
    fig.savefig(img_path, bbox_inches="tight")
    plt.close(fig)

    # PDF dokument
    pdf = FPDF()
    pdf.add_page()

    # Cesta k Arial fontu vo Windows
    font_path = "C:\\Windows\\Fonts\\arial.ttf"
    if os.path.exists(font_path):
        pdf.add_font("ArialUnicode", "", font_path, uni=True)
        pdf.set_font("ArialUnicode", size=12)
    else:
        pdf.set_font("Arial", size=12)  # fallback

    # Nadpis
    pdf.cell(200, 10, txt=f"Kružnica s polomerom {radius} a {points} bodmi", ln=True, align="L")

    # Súradnice bodov
    pdf.cell(200, 10, txt="Súradnice bodov:", ln=True, align="L")
    for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
        pdf.cell(200, 8, txt=f"Bod {i}: ({x:.2f}, {y:.2f})", ln=True, align="L")

    # Obrázok
    pdf.image(img_path, x=10, y=80, w=180)

    # Info o autorovi
    pdf.set_y(-40)
    pdf.cell(200, 10, txt="Autor: Tomáš Lupták", ln=True, align="L")
    pdf.cell(200, 10, txt="Kontakt: 278103@vutbr.cz", ln=True, align="L")
    pdf.cell(200, 10, txt="Použité technológie: Python, Streamlit, Matplotlib, FPDF2", ln=True, align="L")

    # Uloženie PDF
    pdf.output(pdf_path)
    return pdf_path

# ------------------------------------------------
# Streamlit UI
# ------------------------------------------------
st.title("Kružnica - vizualizácia")

# Inputy
radius = st.slider("Polomer kružnice:", 1, 20, 5)
points = st.slider("Počet bodov na kružnici:", 3, 100, 6)
color = st.color_picker("Farba bodov:", "#FF0000")

# Vykreslenie grafu
fig, x_points, y_points = draw_circle(radius, points, color)
st.pyplot(fig)

# Tabuľka so súradnicami
coords_df = pd.DataFrame({"Bod": range(1, points + 1), "X": x_points, "Y": y_points})
st.subheader("Súradnice bodov")
st.dataframe(coords_df)

# Informácie o autorovi
st.sidebar.title("O autorovi")
st.sidebar.info("""
**Meno:** Tomáš Lupták  
**Kontakt:** 278103@vutbr.cz  
**Použité technológie:** Python, Streamlit, Matplotlib, FPDF2
""")

# Export do PDF
if st.button("Exportovať do PDF"):
    pdf_file = export_pdf(radius, points, x_points, y_points)
    with open(pdf_file, "rb") as f:
        st.download_button("Stiahnuť PDF", f, file_name="kruznica.pdf")


