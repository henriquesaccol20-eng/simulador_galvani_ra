import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Galvani: Tensão e Movimento", layout="centered")

# O painel de controle e a animação agora são 100% integrados em Canvas (HTML5)
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 10px; background: white;}
        .painel { background: #f8f9fa; padding: 20px; border-radius: 12px; border: 1px solid #ccc; width: 100%; max-width: 600px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .controle { margin-bottom: 15px; }
        .controle label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 14px;}
        input[type=range] { width: 100%; cursor: pointer; }
        input[type=range]:disabled { cursor: not-allowed; opacity: 0.6; }
        .destaque { color: #d32f2f; font-size: 1.5em; font-weight: bold; }
        canvas { border: 2px solid #ddd; border-radius: 12px; background: #fafafa; }
    </style>
</head>
<body>

    <div class="painel">
        <div class="controle">
            <label>Catodo (Cobre - Valor Fixo): <span style="color:#B87333;">+0.34 V</span></label>
            <input type="range" disabled value="0.34" min="-2" max="2">
        </div>
        <div class="controle">
            <label>Anodo (Zinco - Ajustável): <span id="val-anodo">-0.76 V</span></label>
            <input type="range" id="slider-anodo" min="-3" max="0" step="0.05" value="-0.76">
        </div>
        <div style="text-align: center; margin-top: 15px; font-size: 18px;">
            Diferença de Potencial (ddp): <span class="destaque" id="val-ddp">1.10 V</span>
        </div>
    </div>

    <canvas id="canvas" width="600" height="350"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const sliderAnodo = document.getElementById('slider-anodo');
        const valAnodo = document.getElementById('val-anodo');
        const valDdp = document.getElementById('val-ddp');

        const CATODO = 0.34; // Fixo
        let time = 0; // Controla o andamento da animação

        function drawScene(ddp) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Desenhar os "Eletrodos" no fundo
            ctx.fillStyle = '#C0C0C0'; ctx.fillRect(80, 200, 40, 100); // Zinco
            ctx.fillStyle = '#B87333'; ctx.fillRect(480, 200, 40, 100); // Cobre
            
            // Fios conectando à rã
            ctx.beginPath(); ctx.moveTo(100, 200); ctx.quadraticCurveTo(100, 100, 250, 180); 
            ctx.strokeStyle = '#888'; ctx.lineWidth = 3; ctx.stroke();
            ctx.beginPath(); ctx.moveTo(500, 200); ctx.quadraticCurveTo(500, 100, 350, 180); ctx.stroke();

            // 2. A MÁGICA DA AGITAÇÃO: Matemática pura baseada na ddp
            let anguloBase = Math.PI / 8; // Repouso
            let variacao = 0;

            if (ddp > 0.5) {
                // Intensidade aumenta conforme a ddp passa de 0.5
                let intensidade = ddp - 0.5; 
                
                // Amplitude = o quão alto a perna levanta
                let amplitude = intensidade * 0.4; 
                
                // Frequência = o quão rápido ela treme (aumenta com a ddp)
                let frequencia = intensidade * 20; 
                
                variacao = Math.sin(time * frequencia) * amplitude;
                
                // Impede que a perna dobre para baixo (atravessando a mesa)
                if (variacao < 0) variacao = variacao * 0.2; 
            }

            // Calculando as posições das articulações
            let anguloCoxa = anguloBase + variacao;
            // A canela dobra ainda mais que a coxa
            let anguloCanela = anguloCoxa + (Math.PI / 6) + (variacao * 1.5);

            let troncoX = 180, troncoY = 180;
            let coxaX = troncoX + 90, coxaY = troncoY;
            
            let joelhoX = coxaX + Math.cos(anguloCoxa) * 90;
            let joelhoY = coxaY - Math.sin(anguloCoxa) * 90;

            let peX = joelhoX + Math.cos(anguloCanela) * 80;
            let peY = joelhoY - Math.sin(anguloCanela) * 80;

            // 3. Desenhando a Rã (Linhas limpas e arredondadas)
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

        // Loop de animação contínuo (60 frames por segundo)
        function animate() {
            let anodo = parseFloat(sliderAnodo.value);
            let ddp = CATODO - anodo; // Calcula a voltagem atual
            
            // Atualiza os textos na tela
            valAnodo.innerText = anodo.toFixed(2) + ' V';
            valDdp.innerText = ddp.toFixed(2) + ' V';

            // Desenha a rã com a ddp atual
            drawScene(ddp);
            
            time += 0.05; // O tempo passa
            requestAnimationFrame(animate); // Chama o próximo frame
        }

        animate(); // Inicia o loop
    </script>
</body>
</html>
"""

components.html(html_code, height=650)
