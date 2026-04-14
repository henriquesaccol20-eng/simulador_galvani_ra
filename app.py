import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Galvani: Potenciais de Redução", layout="centered")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 10px; background: white;}
        .painel { background: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ccc; width: 100%; max-width: 650px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .controles-flex { display: flex; justify-content: space-around; gap: 10px; }
        .controle { flex: 1; text-align: center; }
        .controle label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 14px;}
        .nome-metal { color: #1565C0; font-size: 16px; display: block; margin-bottom: 5px; min-height: 25px; font-weight: bold; line-height: 1.2;}
        .valor-reducao { font-weight: bold; color: #333; font-size: 15px; }
        input[type=range] { width: 95%; cursor: pointer; }
        input[type=range]:disabled { cursor: not-allowed; opacity: 0.6; }
        .destaque { color: #d32f2f; font-size: 1.6em; font-weight: bold; }
        
        .btn-choque { background-color: #d32f2f; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: background 0.2s, transform 0.1s; box-shadow: 0 4px 6px rgba(0,0,0,0.2); margin-top: 15px;}
        .btn-choque:hover { background-color: #b71c1c; }
        .btn-choque:active { transform: scale(0.95); box-shadow: 0 2px 3px rgba(0,0,0,0.2);}
        
        canvas { border: 2px solid #ddd; border-radius: 12px; background: #fafafa; margin-top: 10px; }
    </style>
</head>
<body>

    <div class="painel">
        <div class="controles-flex">
            <div class="controle">
                <label>Catodo (Fixo):</label>
                <span class="nome-metal" style="color:#B87333;">Cobre (Cu)</span>
                <span class="valor-reducao">Eº de Redução: +0.34 V</span>
                <br><br>
                <input type="range" disabled value="0.34" min="-2" max="2">
            </div>
            <div class="controle">
                <label>Anodo (Ajustável):</label>
                <span class="nome-metal" id="nome-metal">Hidrogênio (H)</span>
                <span id="val-anodo" class="valor-reducao">Eº de Redução: 0.00 V</span>
                <br><br>
                <input type="range" id="slider-anodo" min="-1.92" max="0.00" step="0.01" value="0.00">
            </div>
        </div>
        <div style="text-align: center; margin-top: 15px; font-size: 16px;">
            Diferença de Potencial (ddp): <span class="destaque" id="val-ddp">0.34 V</span>
        </div>
        <div style="text-align: center;">
            <button id="btn-choque" class="btn-choque">⚡ Aplicar Choque</button>
        </div>
    </div>

    <canvas id="canvas" width="650" height="400"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const sliderAnodo = document.getElementById('slider-anodo');
        const valAnodo = document.getElementById('val-anodo');
        const valDdp = document.getElementById('val-ddp');
        const nomeMetalDisplay = document.getElementById('nome-metal');
        const btnChoque = document.getElementById('btn-choque');

        const CATODO = 0.34; 
        let time = 0; 
        
        let energiaEspasmo = 0;

        function obterNomeMetal(voltagem) {
            let v = Math.round(voltagem * 100) / 100;
            
            if (v >= -0.05) return "Hidrogênio (H)";
            if (v >= -0.15) return "Chumbo (Pb) / Estanho (Sn)";
            if (v >= -0.28) return "Níquel (Ni)";
            if (v >= -0.35) return "Cobalto (Co)";
            if (v >= -0.45) return "Ferro (Fe)";
            if (v >= -0.76) return "Zinco (Zn)";
            if (v >= -1.18) return "Manganês (Mn)";
            if (v >= -1.66) return "Alumínio (Al)";
            
            // Cobre a região entre o alumínio puro e o limite de -1.92V
            return "Alumínio (Al) / Ligas Leves"; 
        }

        btnChoque.addEventListener('click', function() {
            let ddpAtual = CATODO - parseFloat(sliderAnodo.value);
            
            if (ddpAtual > 0.5) {
                let intensidade = ddpAtual - 0.5;
                energiaEspasmo = intensidade * 0.5; 
            }
        });

        function drawLeg(ctx, xOffset, yOffset, variacao) {
            let anguloBase = Math.PI / 8; 
            let anguloCoxa = anguloBase + variacao;
            let anguloCanela = anguloCoxa + (Math.PI / 6) + (variacao * 1.5);
            let troncoX = xOffset, troncoY = yOffset;
            let coxaX = troncoX + 90, coxaY = troncoY;
            let joelhoX = coxaX + Math.cos(anguloCoxa) * 90;
            let joelhoY = coxaY - Math.sin(anguloCoxa) * 90;
            let peX = joelhoX + Math.cos(anguloCanela) * 80;
            let peY = joelhoY - Math.sin(anguloCanela) * 80;

            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            
            ctx.beginPath(); ctx.moveTo(troncoX, troncoY); ctx.lineTo(coxaX, coxaY);
            ctx.strokeStyle = '#2E7D32'; ctx.lineWidth = 26; ctx.stroke();
            ctx.beginPath(); ctx.moveTo(coxaX, coxaY); ctx.lineTo(joelhoX, joelhoY);
            ctx.strokeStyle = '#4CAF50'; ctx.lineWidth = 22; ctx.stroke();
            ctx.beginPath(); ctx.moveTo(joelhoX, joelhoY); ctx.lineTo(peX, peY);
            ctx.strokeStyle = '#81C784'; ctx.lineWidth = 16; ctx.stroke();

            // OS TRÊS DEDOS DA RÃ
            ctx.lineWidth = 6; 
            ctx.strokeStyle = '#81C784'; 

            // Dedo Superior
            let anguloDedo1 = anguloCanela - 0.5; 
            ctx.beginPath();
            ctx.moveTo(peX, peY);
            ctx.lineTo(peX + Math.cos(anguloDedo1) * 50, peY - Math.sin(anguloDedo1) * 50);
            ctx.stroke();

            // Dedo Central
            let anguloDedo2 = anguloCanela;
            ctx.beginPath();
            ctx.moveTo(peX, peY);
            ctx.lineTo(peX + Math.cos(anguloDedo2) * 55, peY - Math.sin(anguloDedo2) * 55);
            ctx.stroke();

            // Dedo Inferior
            let anguloDedo3 = anguloCanela + 0.5; 
            ctx.beginPath();
            ctx.moveTo(peX, peY);
            ctx.lineTo(peX + Math.cos(anguloDedo3) * 50, peY - Math.sin(anguloDedo3) * 50);
            ctx.stroke();
        }

        function drawScene() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#C0C0C0'; ctx.fillRect(100, 250, 40, 100); 
            ctx.fillStyle = '#B87333'; ctx.fillRect(530, 250, 40, 100); 
            
            ctx.strokeStyle = '#888'; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(120, 250); ctx.quadraticCurveTo(120, 100, 200, 200); ctx.stroke(); 
            ctx.beginPath(); ctx.moveTo(550, 250); ctx.quadraticCurveTo(550, 100, 350, 200); ctx.stroke(); 

            let variacao = 0;
            if (energiaEspasmo > 0.001) {
                variacao = Math.sin(time * 2) * energiaEspasmo;
                if (variacao < 0) variacao = variacao * 0.2; 
                energiaEspasmo *= 0.985; 
            } else {
                energiaEspasmo = 0; 
            }

            ctx.beginPath(); ctx.moveTo(180, 150); ctx.lineTo(180, 250); 
            ctx.strokeStyle = '#2E7D32'; ctx.lineWidth = 26; ctx.lineCap = 'round'; ctx.stroke();
            
            drawLeg(ctx, 180, 150, variacao); 
            drawLeg(ctx, 180, 250, variacao); 
        }

        function animate() {
            let anodo = parseFloat(sliderAnodo.value);
            let ddp = CATODO - anodo; 
            
            // Adicionado o prefixo "Eº de Redução:" direto na tela
            valAnodo.innerText = "Eº de Redução: " + anodo.toFixed(2) + ' V';
            valDdp.innerText = ddp.toFixed(2) + ' V';
            nomeMetalDisplay.innerHTML = obterNomeMetal(anodo);
            
            drawScene();
            time += 0.05; 
            requestAnimationFrame(animate); 
        }
        
        animate(); 
    </script>
</body>
</html>
"""

components.html(html_code, height=800)
