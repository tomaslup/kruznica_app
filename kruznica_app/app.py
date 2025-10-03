import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io

# --- APLIKÁCIA ---
st.title("Body na kružnici")

# Vstup od používateľa
st.sidebar.header("Parametre kružnice")
x_center = st.sidebar.number_input("X súradnica stredu", value=0.0)
y_center = st.sidebar.number_input("Y súradnica stredu", value=0.0)
radius = st.sidebar.number_input("Polomer", min_value=1.0, value=5.0)
num_points = st.sidebar.slider("Počet bodov", min_value=3, max_value=500, value=5)
color = st.sidebar.color_picker("Farba bodov", "#ff0000")

# Vygenerovanie bodov
angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
x_points = x_center + radius * np.cos(angles)
y_points = y_center + radius * np.sin(angles)

# Vykreslenie grafu
fig, ax = plt.subplots()
circle = plt.Circle((x_center, y_center), radius, fill=False, color="blue")
ax.add_artist(circle)

# Body
ax.scatter(x_points, y_points, c=color)

# Rovnaké mierky na osiach
ax.set_aspect("equal")

# Prispôsobenie veľkosti grafu kružnici
ax.set_xlim(x_center - radius*1.2, x_center + radius*1.2)
ax.set_ylim(y_center - radius*1.2, y_center + radius*1.2)

# Popisy osí
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")

# Jemná mriežka
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

# Zobrazenie súradníc
st.subheader("Súradnice bodov")
for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
    st.write(f"Bod {i}: ({x:.2f}, {y:.2f})")

# Informácie o autorovi
st.sidebar.subheader("O autorovi")
st.sidebar.write("Meno: Tomáš Lupták")
st.sidebar.write("Kontakt: 278103@vutbr,cz")
st.sidebar.write("Použité technológie: Python, Streamlit, Matplotlib, FPDF")

# Export do PDF
if st.button("Exportovať do PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Body na kružnici - Výstup", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Stred: ({x_center}, {y_center})", ln=True)
    pdf.cell(200, 10, txt=f"Polomer: {radius}", ln=True)
    pdf.cell(200, 10, txt=f"Počet bodov: {num_points}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Súradnice bodov:", ln=True)
    for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
        pdf.cell(200, 10, txt=f"Bod {i}: ({x:.2f}, {y:.2f})", ln=True)

    # Uloženie grafu do bufferu a vloženie do PDF
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    pdf.image(buf, x=10, y=None, w=180)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Autor: Janko Mrkva", ln=True)
    pdf.cell(200, 10, txt="Email: janko@example.com", ln=True)

    pdf.output("kruznica.pdf")

    st.success("PDF bolo vytvorené! Stiahni si ho z priečinka projektu.")
