import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Galvani: Eletroquímica", layout="centered")

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
                <input type="range" id="slider-anodo" min="-0.45" max="0.00
