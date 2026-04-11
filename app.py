import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Galvani: Reação Simultânea", layout="centered")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 10px; background: white;}
        .painel { background: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ccc; width: 100%; max-width: 650px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .controles-flex { display: flex; justify-content: space-around; gap: 10px; }
        .controle { flex: 1; text-align: center; }
        .controle label { display: block; font-weight: bold; margin-bottom: 3px; font-size: 13px;}
        input[type=range] { width: 90%; cursor: pointer; }
        input[type=range]:disabled { cursor: not-allowed; opacity: 0.6; }
        .destaque { color: #d32f2f; font-size: 1.4em; font-weight: bold; }
        canvas { border: 2px solid #ddd; border-radius: 12px; background: #fafafa; }
    </style>
</head>
<body>

    <div class="painel">
        <div class="controles-flex">
            <div class="controle">
                <label>Catodo (Cobre - Valor Fixo): <span style="color:#B87333;">+0.34 V</span></label>
                <input type="range" disabled value="0.34" min="-2" max="2">
            </div>
            <div class="controle">
                <label>Anodo (Zinco - Ajustável): <span id="val-anodo">-0.76 V</span></label>
                <input type="range" id="slider-anodo" min="-3" max="0" step="0.05" value="-0.76">
            </div>
        </div>
        <div style="text-align: center; margin-top: 10px; font-size: 16px;">
            Diferença de Potencial (ddp): <span class="destaque" id="val-ddp">1.10 V</span>
        </div>
    </div>

    <canvas id="canvas" width="650" height="400"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const sliderAnodo = document.getElementById('slider-anodo');
        const valAnodo = document.getElementById('val-anodo');
        const valDdp = document.getElementById('val-ddp');

        const CATODO = 0.34; // Fixo
        let time = 0; // Controla o andamento da animação

        function drawLeg(ctx, xOffset, yOffset, variacao) {
            let anguloBase = Math.PI / 8; // Repouso
            
            // Calculando as posições das articulações
            let anguloCoxa = anguloBase + variacao;
            let anguloCanela = anguloCoxa + (Math.PI / 6) + (variacao * 1.5);

            let troncoX = 0 + xOffset, troncoY = 0 + yOffset;
            let coxaX = troncoX + 90, coxaY = troncoY;
            
            let joelhoX = coxaX + Math.cos(anguloCoxa) * 90;
            let joelhoY = coxaY - Math.sin(anguloCoxa) * 90;

            let peX = joelhoX + Math.cos(anguloCanela) * 80;
            let peY = joelhoY - Math.sin(anguloCanela) * 80;

            // Desenhando a Rã (Linhas limpas e arredondadas)
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            
            // Tronco
            ctx.beginPath(); ctx.moveTo(troncoX, troncoY); ctx.lineTo(coxaX, coxaY);
            ctx.strokeStyle = '#2E7D32'; ctx.lineWidth = 26; ctx.stroke();

            // Coxa
            ctx.beginPath(); ctx.moveTo(coxaX, coxaY); ctx.lineTo(joelhoX, joelhoY);
            ctx.strokeStyle = '#4CAF50'; ctx.lineWidth = 22; ctx.stroke();

            // Canela
            ctx.beginPath(); ctx.moveTo(joelhoX, joelhoY); ctx.lineTo(peX, peY);
            ctx.strokeStyle = '#81C784'; ctx.lineWidth = 16; ctx.stroke();
        }

        function drawScene(ddp) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Desenhar os "Eletrodos" no fundo
            ctx.fillStyle = '#C0C0C0'; ctx.fillRect(100, 250, 40, 100); // Zinco
            ctx.fillStyle = '#B87333'; ctx.fillRect(530, 250, 40, 100); // Cobre
            
            // Fios conectando
            ctx.strokeStyle = '#888'; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(120, 250); ctx.quadraticCurveTo(120, 100, 200, 200); ctx.stroke(); 
            ctx.beginPath(); ctx.moveTo(550, 250); ctx.quadraticCurveTo(550, 100, 350, 200); ctx.stroke(); 

            // 2. A MÁGICA DA AGITAÇÃO SIMULTÂNEA
            let variacao = 0;

            if (ddp > 0.5) {
                let intensidade = ddp - 0.5; 
                let amplitude
