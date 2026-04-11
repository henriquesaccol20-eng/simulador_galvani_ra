import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Biofísica UFSM - Galvani v3", layout="centered")

st.title("⚡ Simulação Dinâmica: O Choque de Galvani")
st.markdown("Mova os sliders para gerar uma ddp acima de 0.5V e clique no botão para aplicar o estímulo. O espasmo agora é violento!")

# Controles de voltagem centralizados
col1, col2 = st.columns(2)
with col1:
    v_anodo = st.slider("Potencial Zinco (Anodo) [V]", -2.0, 2.0, -0.76)
with col2:
    v_catodo = st.slider("Potencial Cobre (Catodo) [V]", -2.0, 2.0, 0.34)

ddp = v_catodo - v_anodo
st.metric("Diferença de Potencial Total", f"{ddp:.2f} V")

# Botão de estímulo (O gatilho do choque)
aplicar_choque = st.button("🔴 Aplicar Choque")

# Motor de Física com aesthetics limpos e movimento violento
html_code = f"""
<div id="canvas-container" style="width: 100%; height: 500px; background: #222; border-radius: 15px; border: 2px solid #555;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
    const {{ Engine, Render, Runner, Bodies, Composite, Constraint }} = Matter;
    
    const engine = Engine.create();
    const render = Render.create({{
        element: document.getElementById('canvas-container'),
        engine: engine,
        options: {{ width: 800, height: 500, wireframes: false, background: 'transparent' }}
    }});

    // Mesa de dissecção (Chão)
    const table = Bodies.rectangle(400, 480, 810, 60, {{ isStatic: true, render: {{ fillStyle: '#333' }} }});
    
    // Partes da Rã com frictionAir baixo para movimento solto
    const frog_torso = Bodies.rectangle(200, 200, 100, 50, {{ isStatic: true, render: {{ fillStyle: '#1e5d2f' }} }});
    const coxa = Bodies.rectangle(290, 200, 80, 25, {{ frictionAir: 0.01, render: {{ fillStyle: '#27ae60' }} }});
    const canela = Bodies.rectangle(370, 200, 90, 18, {{ frictionAir: 0.01, render: {{ fillStyle: '#2ecc71' }} }});

    // Articulações (Constraints) COM RENDER INVISÍVEL
    const joint1 = Constraint.create({{
        bodyA: frog_torso, pointA: {{ x: 45, y: 0 }},
        bodyB: coxa, pointB: {{ x: -35, y: 0 }},
        stiffness: 0.8, length: 5,
        render: {{ visible: false }} // 👈 Remove a linha preta
    }});
    
    const joint2 = Constraint.create({{
        bodyA: coxa, pointA: {{ x: 35, y: 0 }},
        bodyB: canela, pointB: {{ x: -40, y: 0 }},
        stiffness: 0.8, length: 5,
        render: {{ visible: false }} // 👈 Remove a linha preta
    }});

    // Mola muscular de retorno (Stiffness baixo para contração dramática)
    const muscle = Constraint.create({{
        bodyA: frog_torso, pointA: {{ x: 90, y: 30 }},
        bodyB: canela, pointB: {{ x: 0, y: 0 }},
        stiffness: 0.01, // 👈 Muito mais suave
        length: 160,
        render: {{ visible: false }} // 👈 Totalmente invisível
    }});

    Composite.add(engine.world, [table, frog_torso, coxa, canela, joint1, joint2, muscle]);

    // Aplica a força APENAS se o botão for clicado E ddp > 0.5V
    if ({str(aplicar_choque).lower()} && Math.abs({ddp}) > 0.5) {{
        // Força VIOLENTA (X*20) aplicada instantaneamente
        Matter.Body.applyForce(canela, canela.position, {{ 
            x: 1.6 * Math.abs({ddp}), // 👈 Força maciça em X
            y: -2.4 * Math.abs({ddp}) // 👈 Força maciça em Y (pulo)
        }});
    }}

    Render.run(render);
    const runner = Runner.create();
    Runner.run(runner, engine);
</script>
"""

components.html(html_code, height=520)

st.info("💡 **A Física do Choque:** O motor de física Matter.js aplica um vetor de força instantâneo na canela quando a ddp ultrapassa o limiar de despolarização (~0.5V). Sem as linhas de articulação visíveis, a estética fica mais limpa, focando apenas na resposta muscular violenta.")
