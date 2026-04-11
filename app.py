import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Biofísica UFSM - Galvani", layout="wide")

st.title("⚡ Simulação Estabilizada: O Experimento de Galvani")
st.markdown("Ajuste a ddp. A rã só reagirá se a voltagem for suficiente para romper o limiar de repouso (~0.5V).")

# Controles
col_a, col_b = st.columns(2)
with col_a:
    v_anodo = st.slider("Potencial Anodo (Zinco) [V]", -2.0, 2.0, -0.76)
with col_b:
    v_catodo = st.slider("Potencial Catodo (Cobre) [V]", -2.0, 2.0, 0.34)

ddp = v_catodo - v_anodo
st.metric("Diferença de Potencial Real", f"{ddp:.2f} V")

# Botão de estímulo para evitar que ela fique "doida" sozinha
estimular = st.button("⚡ Aplicar Estímulo (Choque)")

# Motor de Física com estabilização
html_code = f"""
<div id="canvas-container" style="width: 100%; height: 450px; background: #222; border-radius: 15px; border: 2px solid #444;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
    const {{ Engine, Render, Runner, Bodies, Composite, Constraint }} = Matter;
    
    const engine = Engine.create();
    const render = Render.create({{
        element: document.getElementById('canvas-container'),
        engine: engine,
        options: {{ width: 800, height: 450, wireframes: false, background: 'transparent' }}
    }});

    // Chão (Mesa de dissecção)
    const ground = Bodies.rectangle(400, 430, 810, 60, {{ isStatic: true, render: {{ fillStyle: '#333' }} }});
    
    // Partes da rã com AMORTECIMENTO (frictionAir) para não ficar a 100 por hora
    const body = Bodies.rectangle(250, 200, 80, 40, {{ isStatic: true, render: {{ fillStyle: '#1e5d2f' }} }});
    const coxa = Bodies.rectangle(330, 200, 70, 25, {{ frictionAir: 0.1, render: {{ fillStyle: '#27ae60' }} }});
    const canela = Bodies.rectangle(400, 200, 80, 18, {{ frictionAir: 0.1, render: {{ fillStyle: '#2ecc71' }} }});

    // Articulações firmes
    const joint1 = Constraint.create({{
        bodyA: body, pointA: {{ x: 35, y: 0 }},
        bodyB: coxa, pointB: {{ x: -30, y: 0 }},
        stiffness: 0.9, length: 2
    }});
    
    const joint2 = Constraint.create({{
        bodyA: coxa, pointA: {{ x: 30, y: 0 }},
        bodyB: canela, pointB: {{ x: -35, y: 0 }},
        stiffness: 0.9, length: 2
    }});

    // Mola muscular (mantém a perna em repouso)
    const muscle = Constraint.create({{
        bodyA: body, pointA: {{ x: 0, y: 0 }},
        bodyB: canela, pointB: {{ x: 0, y: 0 }},
        stiffness: 0.05, length: 160, render: {{ strokeStyle: '#444', lineWidth: 1 }}
    }});

    Composite.add(engine.world, [ground, body, coxa, canela, joint1, joint2, muscle]);

    // Aplica o choque APENAS se o botão for clicado E a ddp for alta
    if ({str(estimular).lower()} && Math.abs({ddp}) > 0.5) {{
        Matter.Body.applyForce(canela, canela.position, {{ 
            x: 0.08 * Math.abs({ddp}), 
            y: -0.12 * Math.abs({ddp}) 
        }});
    }}

    Render.run(render);
    const runner = Runner.create();
    Runner.run(runner, engine);
</script>
"""

components.html(html_code, height=470)

st.help("Se a ddp for menor que 0.5V, o sistema nervoso da rã não atinge o limiar de despolarização e nada acontece. Tente aumentar a ddp e clicar em 'Aplicar Estímulo'!")
