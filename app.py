import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página
st.set_page_config(page_title="Biofísica UFSM - Galvani", layout="centered")

st.title("⚡ Simulação: O Galvanismo")
st.markdown("Mova os sliders. Se a diferença de potencial (ddp) ultrapassar 0.5V, a perna sofre contração instantânea.")

# Controles
col1, col2 = st.columns(2)
with col1:
    v_anodo = st.slider("Potencial Zinco (Anodo) [V]", -2.0, 2.0, -0.76)
with col2:
    v_catodo = st.slider("Potencial Cobre (Catodo) [V]", -2.0, 2.0, 0.34)

ddp = v_catodo - v_anodo
st.metric("Diferença de Potencial (ddp)", f"{ddp:.2f} V")

# Visualização limpa com Matplotlib
fig, ax = plt.subplots(figsize=(7, 4))

limiar = 0.5
esta_contraindo = abs(ddp) > limiar

# Cálculo do ângulo baseado na ddp
if esta_contraindo:
    # Quanto maior a voltagem, mais a perna levanta
    angulo_coxa = np.deg2rad(30 + (abs(ddp) * 30)) 
else:
    # Posição de repouso
    angulo_coxa = np.deg2rad(30)

# Coordenadas matemáticas das linhas
# 1. Corpo
corpo_x, corpo_y = [0, 1], [1, 1]

# 2. Coxa (depende do ângulo calculado)
coxa_x = [1, 1 + 0.6 * np.cos(angulo_coxa)]
coxa_y = [1, 1 - 0.6 * np.sin(angulo_coxa)]

# 3. Canela (dobra dependendo se está contraindo ou não)
canela_x = [coxa_x[1], coxa_x[1] + 0.5]
canela_y = [coxa_y[1], coxa_y[1] + (0.3 if esta_contraindo else -0.2)]

# Desenhando com linhas grossas e pontas arredondadas (sem juntas feias)
ax.plot(corpo_x, corpo_y, color='#2E7D32', lw=12, solid_capstyle='round', label='Tronco')
ax.plot(coxa_x, coxa_y, color='#4CAF50', lw=10, solid_capstyle='round', label='Coxa')
ax.plot(canela_x, canela_y, color='#81C784', lw=8, solid_capstyle='round', label='Canela')

# Desenhando os metais
ax.scatter([0.2], [1.3], color='#B0BEC5', s=400, zorder=5, label='Zinco')
ax.scatter([1.8], [0.8], color='#FF9800', s=400, zorder=5, label='Cobre')

# Estética do Gráfico
ax.set_xlim(-0.2, 2.5)
ax.set_ylim(0, 2.0)
ax.axis('off') # Tira as bordas
ax.legend(loc='upper right')

# Renderiza no Streamlit
st.pyplot(fig)

# Mensagens de status
if esta_contraindo:
    st.success("⚡ CHOQUE DETECTADO: O limiar de despolarização foi rompido e o músculo contraiu.")
else:
    st.info("Repouso: A voltagem atual é insuficiente para gerar um impulso nervoso.")
