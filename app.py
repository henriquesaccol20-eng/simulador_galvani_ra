import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Galvani: Adaptação Muscular", layout="centered")

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
        .nome-metal { color: #1565C0; font-size: 16px; display: block; margin-bottom: 5px; min-height: 20px;}
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
                <label>Catodo (Fixo):</label>
                <span class="nome-metal" style="color:#B87333;">Cobre (Cu)</span>
                <span style="font-weight:bold;">+0.34 V</span>
                <br><br>
                <input type="range" disabled value="0.34" min="-2" max="2">
            </div>
            <div class="controle">
                <label>Anodo (Ajustável):</label>
                <span class="nome-metal" id="nome-metal">Hidrogênio (H)</span>
                <span id="val-anodo" style="font-weight:bold;">0.00 V</span>
                <br><br>
                <input type="range" id="slider-anodo" min="-0.45" max="0.00" step="0.05" value="0.00">
            </div>
        </div>
        <div style="text-align: center; margin-top: 15px; font-size: 16px;">
            Diferença de Potencial (ddp): <span class="destaque" id="val-ddp">0.34 V</span>
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

        const CATODO = 0.34; 
        let time = 0; 
        
        // NOVAS VARIÁVEIS PARA O EFEITO DE ACOMODAÇÃO (Espasmo temporário)
        let energiaEspasmo = 0;
        let ddpAnterior = CATODO - parseFloat(sliderAnodo.value);

        function obterNomeMetal(voltagem) {
            let v = Math.round(voltagem * 100) / 100;
            if (v === 0.00) return "Hidrogênio (H)";
            if (v === -0.05) return "Liga Intermediária";
            if (v === -0.10) return "Liga Intermediária";
            if (v === -0.15) return "Estanho (Sn) / Chumbo (Pb)";
            if (v === -0.20) return "Liga Intermediária";
            if (v === -0.25) return "Níquel (Ni)";
            if (v === -0.30) return "Cobalto (Co)";
            if (v === -0.35) return "Liga Intermediária";
            if (v === -0.40) return "Cádmio (Cd)";
            if (v === -0.45) return "Ferro (Fe)";
            return "Desconhecido";
        }

        // O SEGREDO: O evento 'input' detecta a variação.
        // Toda vez que você move o slider, ele injeta energia no músculo.
        sliderAnodo.addEventListener('input', function() {
            let ddpAtual = CATODO - parseFloat(this.value);
            
            // Se rompeu o limiar de 0.5V E a voltagem está variando
            if (ddpAtual > 0.5 && Math.abs(ddpAtual - ddpAnterior) > 0.01) {
                let intensidade = ddpAtual - 0.5;
                energiaEspasmo = intensidade * 0.5; // Recarrega o espasmo
            }
            ddpAnterior = ddpAtual;
        });

        function drawLeg(ctx, xOffset, yOffset, variacao) {
            let anguloBase = Math.PI / 8; 
            let anguloCoxa = anguloBase + variacao;
            let anguloCanela = anguloCoxa + (Math.PI / 6) + (variacao * 1.5);

            let troncoX = 0 + xOffset, troncoY = 0 + yOffset;
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
        }

        function drawScene() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Eletrodos e Fios
            ctx.fillStyle = '#C0C0C0'; ctx.fillRect(100, 250, 40, 100); 
            ctx.fillStyle = '#B87333'; ctx.fillRect(530, 250, 40, 100); 
            ctx.strokeStyle = '#888'; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(120, 250); ctx.quadraticCurveTo(120, 100, 200, 200); ctx.stroke(); 
            ctx.beginPath(); ctx.moveTo(550, 250); ctx.quadraticCurveTo(550, 100, 350, 200); ctx.stroke(); 

            let variacao = 0;

            // Se ainda tem energia de espasmo, a perna se move
            if (energiaEspasmo > 0.001) {
                variacao = Math.sin(time * 30) * energiaEspasmo;
                if (variacao < 0) variacao = variacao * 0.2; 
                
                // DECAIMENTO: Perde 6% da energia a cada quadro da animação.
                // Isso cria o efeito transitório perfeito. Parou a mão, a rã para.
                energiaEspasmo *= 0.94; 
            } else {
                energiaEspasmo = 0; // Repouso
            }

            // A "Pelve"
            ctx.beginPath(); ctx.moveTo(180, 150); ctx.lineTo(180, 250); 
            ctx.strokeStyle = '#2E7D32'; ctx.lineWidth = 26; ctx.lineCap = 'round'; ctx.stroke();

            // As rãs
            drawLeg(ctx, 180, 150, variacao); 
            drawLeg(ctx, 180, 250, variacao); 
        }

        function animate() {
            let anodo = parseFloat(sliderAnodo.value);
            let ddp = CATODO - anodo; 
            
            valAnodo.innerText = anodo.toFixed(2) + ' V';
            valDdp.innerText = ddp.toFixed(2) + ' V';
            nomeMetalDisplay.innerText = obterNomeMetal(anodo);

            drawScene();
            
            time += 0.05; 
            requestAnimationFrame(animate); 
        }

        animate(); 
    </script>
</body>
</html>
"""

components.html(html_code, height=750)
