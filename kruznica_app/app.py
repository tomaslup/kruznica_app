import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import BytesIO

# ------------------------------------------------
# Funkcie
# ------------------------------------------------
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# --- tu máš svoje pomocné funkcie ---
def generuj_body(...):
    # funkcia na výpočet súradníc
    ...

# --- sem vlož novú funkciu ---
def export_pdf_image_with_info(radius, points, x_points, y_points, color="red"):
    fig, ax = plt.subplots(figsize=(8,8))

    # Kruh
    theta_circle = np.linspace(0, 2 * np.pi, 500)
    x_circle = radius * np.cos(theta_circle)
    y_circle = radius * np.sin(theta_circle)
    ax.plot(x_circle, y_circle, 'b-')
    ax.scatter(x_points, y_points, c=color)

    # Číslovanie bodov
    for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
        ax.text(x, y, str(i), fontsize=10, ha='right', va='bottom')

    # Grid a rovnaké mierky
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_aspect("equal", adjustable="box")
    margin = radius * 0.5
    ax.set_xlim(-radius-margin, radius+margin)
    ax.set_ylim(-radius-margin, radius+margin)

    # Súradnice + autor info
    info_text = "Súradnice bodov:\n"
    for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
        info_text += f"Bod {i}: ({x:.2f}, {y:.2f})\n"
    info_text += "\nAutor: Tomáš Lupták\nKontakt: 278103@vutbr.cz\nPoužité technológie: Python, Streamlit, Matplotlib"

    ax.text(radius + margin*0.05, 0, info_text, fontsize=10, ha='left', va='center', family='monospace')

    # Export do PDF
    pdf_bytes = BytesIO()
    fig.savefig(pdf_bytes, format='pdf', bbox_inches='tight')
    pdf_bytes.seek(0)
    plt.close(fig)
    return pdf_bytes

# --- potom ide hlavná časť aplikácie ---
def main():
    st.title("Kružnica s bodmi")
    radius = st.slider("Polomer kružnice", 1, 10, 5)
    points = st.slider("Počet bodov", 1, 20, 6)

    # tu voláš svoju funkciu na generovanie bodov
    theta = np.linspace(0, 2*np.pi, points, endpoint=False)
    x_points = radius * np.cos(theta)
    y_points = radius * np.sin(theta)

    # vizualizácia grafu
    fig, ax = plt.subplots()
    ax.plot(radius*np.cos(theta), radius*np.sin(theta))
    ax.scatter(x_points, y_points, color="red")
    st.pyplot(fig)

    # tlačidlo na export
    if st.button("Exportovať do PDF"):
        pdf_bytes = export_pdf_image_with_info(radius, points, x_points, y_points, color="red")
        st.download_button("Stiahnuť PDF", pdf_bytes, file_name="kruznica.pdf")

if __name__ == "__main__":
    main()

def calculate_points(radius, points):
    theta_points = np.linspace(0, 2 * np.pi, points, endpoint=False)
    x_points = radius * np.cos(theta_points)
    y_points = radius * np.sin(theta_points)
    return x_points, y_points

def draw_circle(radius, points, color="red", annotate=True):
    theta_circle = np.linspace(0, 2 * np.pi, 500)
    x_circle = radius * np.cos(theta_circle)
    y_circle = radius * np.sin(theta_circle)
    x_points, y_points = calculate_points(radius, points)

    fig, ax = plt.subplots()
    ax.plot(x_circle, y_circle, 'b-')
    ax.scatter(x_points, y_points, c=color)

    if annotate:
        for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
            ax.text(x, y, str(i), fontsize=10, ha='right', va='bottom')

    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_aspect("equal", adjustable="box")
    margin = radius * 0.3
    ax.set_xlim(-radius-margin, radius+margin)
    ax.set_ylim(-radius-margin, radius+margin)

    return fig, x_points, y_points

def export_pdf_image(radius, points, x_points, y_points):
    fig, _, _ = draw_circle(radius, points, annotate=True)
    pdf_bytes = BytesIO()
    fig.savefig(pdf_bytes, format='pdf', bbox_inches='tight')
    pdf_bytes.seek(0)
    plt.close(fig)
    return pdf_bytes

# ------------------------------------------------
# Streamlit UI
# ------------------------------------------------
st.title("Kružnica - vizualizácia")

radius = st.slider("Polomer kružnice:", 1, 20, 5)
points = st.slider("Počet bodov na kružnici:", 3, 100, 6)
color = st.color_picker("Farba bodov:", "#FF0000")

fig, x_points, y_points = draw_circle(radius, points, color)
st.pyplot(fig)

coords_df = pd.DataFrame({"Bod": range(1, points + 1), "X": x_points, "Y": y_points})
st.subheader("Súradnice bodov")
st.dataframe(coords_df)

st.sidebar.title("O autorovi")
st.sidebar.info("""
**Meno:** Tomáš Lupták  
**Kontakt:** 278103@vutbr.cz  
**Použité technológie:** Python, Streamlit, Matplotlib
""")
if st.button("Exportovať do PDF"):
    pdf_bytes = export_pdf_image_with_info(radius, points, x_points, y_points, color)
    st.download_button("Stiahnuť PDF", pdf_bytes, file_name="kruznica.pdf")


