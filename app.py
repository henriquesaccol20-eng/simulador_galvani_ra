import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Biofísica: Experimento de Galvani", layout="wide")

st.title("⚡ Simulação Física: O Galvanismo")
st.markdown("Mova os sliders para gerar uma ddp e aplicar um 'choque' na rã.")

# Barra lateral com os controles
st.sidebar.header("Configurações de Voltagem")
v_anodo = st.sidebar.slider("Potencial Anodo (Zinco) [V]", -2.0, 2.0, -0.76)
v_catodo = st.sidebar.slider("Potencial Catodo (Cobre) [V]", -2.0, 2.0, 0.34)
ddp = v_catodo - v_anodo

st.sidebar.metric("Diferença de Potencial", f"{ddp:.2f} V")

# O "Motor" de Física (Matter.js + HTML/JS)
html_code = f"""
<div id="canvas-container" style="width: 100%; height: 500px; background: #f0f2f6; border-radius: 10px;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
    const {{ Engine, Render, Runner, Bodies, Composite, Constraint, Vector }} = Matter;
    
    const engine = Engine.create();
    const render = Render.create({{
        element: document.getElementById('canvas-container'),
        engine: engine,
        options: {{ width: 800, height: 500, wireframes: false, background: '#f0f2f6' }}
    }});

    // Chão
    const ground = Bodies.rectangle(400, 480, 810, 60, {{ isStatic: true, render: {{ fillStyle: '#2ecc71' }} }});
    
    // Partes da Perna (Corpo, Coxa, Canela)
    const body = Bodies.rectangle(300, 200, 100, 40, {{ isStatic: true, render: {{ fillStyle: '#1e5d2f' }} }});
    const coxa = Bodies.rectangle(380, 200, 80, 20, {{ render: {{ fillStyle: '#27ae60' }} }});
    const canela = Bodies.rectangle(460, 200, 90, 15, {{ render: {{ fillStyle: '#2ecc71' }} }});

    // Articulações (Constraints)
    const joint1 = Constraint.create({{
        bodyA: body, pointA: {{ x: 40, y: 0 }},
        bodyB: coxa, pointB: {{ x: -30, y: 0 }},
        stiffness: 0.8, length: 5
    }});
    
    const joint2 = Constraint.create({{
        bodyA: coxa, pointA: {{ x: 30, y: 0 }},
        bodyB: canela, pointB: {{ x: -40, y: 0 }},
        stiffness: 0.8, length: 5
    }});

    // Mola que mantém a perna em repouso
    const muscle = Constraint.create({{
        bodyA: body, pointA: {{ x: 80, y: 50 }},
        bodyB: canela, pointB: {{ x: 0, y: 0 }},
        stiffness: 0.01, length: 150,
        render: {{ visible: false }}
    }});

    Composite.add(engine.world, [ground, body, coxa, canela, joint1, joint2, muscle]);

    // Lógica do Choque baseado na ddp do Streamlit
    const ddpVal = {ddp};
    if (Math.abs(ddpVal) > 0.5) {{
        // Aplica uma força súbita para cima e para frente (o chute)
        Matter.Body.applyForce(canela, canela.position, {{ x: 0.05 * Math.abs(ddpVal), y: -0.08 * Math.abs(ddpVal) }});
    }}

    Render.run(render);
    const runner = Runner.create();
    Runner.run(runner, engine);
</script>
"""

components.html(html_code, height=520)

st.info("💡 **Física em ação:** O motor Matter.js calcula a gravidade e a resistência das articulações. Quando a ddp ultrapassa 0.5V, um vetor de força é aplicado na 'canela', simulando a contração muscular galvânica.")
