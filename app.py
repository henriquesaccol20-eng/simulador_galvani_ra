import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configurações do Título
st.set_page_config(page_title="Experimento de Galvani", layout="centered")
st.title("⚡ Simulação: O Galvanismo e a Força Vital")
st.write("Mova os sliders para alterar o potencial dos metais e observar a reação da rã.")

# Controles de voltagem
st.sidebar.header("Parâmetros dos Metais")
v_anodo = st.sidebar.slider("Potencial Anodo (Zinco) [V]", -2.0, 2.0, -0.76)
v_catodo = st.sidebar.slider("Potencial Catodo (Cobre) [V]", -2.0, 2.0, 0.34)

ddp = v_catodo - v_anodo

# Interface de resultados
st.metric("Diferença de Potencial (ddp)", f"{ddp:.2f} V")

# Lógica do Desenho (Matplotlib)
fig, ax = plt.subplots(figsize=(6, 4))

# Se a ddp for maior que 0.2V, a rã contrai (chuta)
limiar = 0.2
angulo = np.deg2rad(70) if abs(ddp) > limiar else np.deg2rad(20)

# Coordenadas do desenho da rã (Linhas verdes)
ax.plot([0, 0.8], [1, 1], color='#4CAF50', lw=10) # Corpo
ax.plot([0.8, 0.8 + 0.5*np.cos(angulo)], [1, 1 + 0.5*np.sin(angulo)], color='#4CAF50', lw=8) # Coxa
ax.plot([0.8 + 0.5*np.cos(angulo), 1.6], [1 + 0.5*np.sin(angulo), 1.2 if abs(ddp) > limiar else 0.7], color='#4CAF50', lw=5) # Canela

# Desenho dos eletrodos
ax.scatter([0.1], [1.1], color='silver', s=250, label='Zinco (Anodo)')
ax.scatter([1.5], [0.8], color='#B87333', s=250, label='Cobre (Catodo)')

# Ajustes do gráfico
ax.set_xlim(-0.2, 2.0)
ax.set_ylim(0, 2.0)
ax.axis('off')
ax.legend(loc='upper right')

st.pyplot(fig)

if abs(ddp) > limiar:
    st.success("⚠️ CORRENTE DETECTADA: O músculo despolarizou e contraiu!")
else:
    st.info("Músculo em repouso. A ddp é insuficiente.")