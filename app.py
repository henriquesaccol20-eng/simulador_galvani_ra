import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Simulador de Galvani", layout="wide")

# O segredo: Colocar os sliders em HTML/JS junto com o motor de física para não recarregar a página.
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
    <style>
        body { font-family: sans-serif; background: white; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .painel { display: flex; gap: 30px; background: #f8f9fa; padding: 20px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 20px; width: 100%; max-width: 800px; justify-content: center;}
        .controle { display: flex; flex-direction: column; align-items: center; }
        input[type=range] { width: 150px; cursor: pointer; }
        .ddp-display { font-size: 24px; font-weight: bold; color: #d32f2f; display: flex; align-items: center; margin-left: 20px;}
        #canvas-container { border-radius: 12px; overflow: hidden; border: 2px solid #eee; }
    </style>
</head>
<body>

    <div class="painel">
        <div class="controle">
            <label>Anodo (Zn): <b id="val-anodo">-0.76 V</b></label>
            <input type="range" id="slider-anodo" min="-3" max="3" step="0.1" value="-0.76">
        </div>
        <div class="controle">
            <label>Catodo (Cu): <b id="val-catodo">0.34 V</b></label>
            <input type="range" id="slider-catodo" min="-3" max="3" step="0.1" value="0.34">
        </div>
        <div class="ddp-display">
            ddp: <span id="val-ddp" style="margin-left: 8px;">1.10 V</span>
        </div>
    </div>

    <div id="canvas-container"></div>

    <script>
        const { Engine, Render, Runner, Bodies, Composite, Constraint } = Matter;
        
        const engine = Engine.create();
        const render = Render.create({
            element: document.getElementById('canvas-container'),
            engine: engine,
            options: { width: 800, height: 400, wireframes: false, background: '#fafafa' }
        });

        // Partes da Rã (Limpo, sem contornos)
        const torso = Bodies.rectangle(300, 250, 100, 40, { isStatic: true, render: { fillStyle: '#2e7d32' }, collisionFilter: { group: -1 } });
        const coxa = Bodies.rectangle(380, 250, 80, 30, { render: { fillStyle: '#4caf50' }, collisionFilter: { group: -1 } });
        const canela = Bodies.rectangle(450, 250, 80, 20, { render: { fillStyle: '#81c784' }, collisionFilter: { group: -1 } });

        // Articulações INVISÍVEIS (render: false)
        const quadril = Constraint.create({
            bodyA: torso, pointA: { x: 40, y: 0 },
            bodyB: coxa, pointB: { x: -30, y: 0 },
            stiffness: 0.9, length: 0, render: { visible: false }
        });
        
        const joelho = Constraint.create({
            bodyA: coxa, pointA: { x: 30, y: 0 },
            bodyB: canela, pointB: { x: -30, y: 0 },
            stiffness: 0.9, length: 0, render: { visible: false }
        });

        // O "Músculo" que vai encolher com o choque (INVISÍVEL)
        const musculo = Constraint.create({
            bodyA: torso, pointA: { x: 0, y: 150 }, // Ponto fixo abaixo
            bodyB: canela, pointB: { x: 0, y: 0 },
            stiffness: 0.02, length: 150, render: { visible: false }
        });

        Composite.add(engine.world, [torso, coxa, canela, quadril, joelho, musculo]);

        Render.run(render);
        const runner = Runner.create();
        Runner.run(runner, engine);

        // Lógica dos Sliders interagindo DIRETAMENTE com a física
        const sliderAnodo = document.getElementById('slider-anodo');
        const sliderCatodo = document.getElementById('slider-catodo');
        const displayDdp = document.getElementById('val-ddp');

        function atualizarFisica() {
            let anodo = parseFloat(sliderAnodo.value);
            let catodo = parseFloat(sliderCatodo.value);
            let ddp = Math.abs(catodo - anodo);
            
            document.getElementById('val-anodo').innerText = anodo.toFixed(2) + ' V';
            document.getElementById('val-catodo').innerText = catodo.toFixed(2) + ' V';
            displayDdp.innerText = ddp.toFixed(2) + ' V';

            // Se a ddp passar de 0.5V, a perna contrai
            if (ddp > 0.5) {
                // Quanto maior a ddp, mais curto o músculo fica (contração mais forte)
                musculo.length = Math.max(50, 150 - (ddp * 40)); 
            } else {
                musculo.length = 150; // Repouso
            }
        }

        sliderAnodo.addEventListener('input', atualizarFisica);
        sliderCatodo.addEventListener('input', atualizarFisica);
        atualizarFisica(); // Inicia com o valor padrão
    </script>
</body>
</html>
"""

# Renderiza a página HTML completa dentro do Streamlit
components.html(html_code, height=700)
