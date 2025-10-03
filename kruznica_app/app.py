import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# --- export do PDF ---
def export_pdf_image_with_info(radius, points, x_points, y_points, color="red"):
    fig, ax = plt.subplots(figsize=(8,8))

    # 1️⃣ vykreslenie kruhu (hladká čiara)
    theta_circle = np.linspace(0, 2 * np.pi, 500)
    x_circle = radius * np.cos(theta_circle)
    y_circle = radius * np.sin(theta_circle)
    ax.plot(x_circle, y_circle, 'b-')

    # 2️⃣ body na kružnici
    ax.scatter(x_points, y_points, c=color)

    # 3️⃣ číslovanie bodov
    for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
        ax.text(x, y, str(i), fontsize=10, ha='right', va='bottom')

    # osová sústava
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_aspect("equal", adjustable="box")
    margin = radius * 0.5
    ax.set_xlim(-radius-margin, radius+margin)
    ax.set_ylim(-radius-margin, radius+margin)

    # 4️⃣ text dáme mimo grafu – pod obrázok
    info_text = "Súradnice bodov:\n"
    for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
        info_text += f"Bod {i}: ({x:.2f}, {y:.2f})\n"
    info_text += "\nAutor: Tomáš Lupták\nKontakt: 278103@vutbr.cz\nPoužité technológie: Python, Streamlit, Matplotlib"

    # využijeme fig.text namiesto ax.text (umiestnenie pod grafom)
    fig.text(0.1, -0.05, info_text, ha='left', va='top', fontsize=9, family='monospace')

    # uloženie do PDF
    pdf_bytes = BytesIO()
    fig.savefig(pdf_bytes, format='pdf', bbox_inches='tight')
    pdf_bytes.seek(0)
    plt.close(fig)
    return pdf_bytes


# --- hlavná časť aplikácie ---
def main():
    st.title("Kružnica s bodmi")
    radius = st.slider("Polomer kružnice", 1, 10, 5)
    points = st.slider("Počet bodov", 1, 20, 6)

    # výpočet súradníc bodov
    theta = np.linspace(0, 2*np.pi, points, endpoint=False)
    x_points = radius * np.cos(theta)
    y_points = radius * np.sin(theta)

    # vizualizácia grafu
    fig, ax = plt.subplots()
    theta_circle = np.linspace(0, 2*np.pi, 500)
    ax.plot(radius*np.cos(theta_circle), radius*np.sin(theta_circle), 'b-')  # kruh
    ax.scatter(x_points, y_points, color="red")  # body
    st.pyplot(fig)

    # tabuľka so súradnicami priamo v appke
    st.write("### Súradnice bodov")
    for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
        st.write(f"Bod {i}: ({x:.2f}, {y:.2f})")

    # tlačidlo na export
    if st.button("Exportovať do PDF"):
        pdf_bytes = export_pdf_image_with_info(radius, points, x_points, y_points, color="red")
        st.download_button("Stiahnuť PDF", pdf_bytes, file_name="kruznica.pdf")

    
    st.sidebar.title("O autorovi")
    st.sidebar.info("""
    **Meno:** Tomáš Lupták  
    **Kontakt:** 278103@vutbr.cz  
    **Použité technológie:** Python, Streamlit, Matplotlib
    """)

if __name__ == "__main__":
    main()
