"""
Dashboard Integrado - FarmTech Solutions
Fase 7 - FIAP

Sistema unificado integrando todas as fases do projeto (1-4, 6)
"""

import streamlit as st
from datetime import datetime
from servicos.database import init_all_databases

# Inicializar bancos de dados
init_all_databases()

# Configuração da página
st.set_page_config(
    page_title="FarmTech Solutions - Dashboard Integrado",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar e aplicar CSS global
from styles import apply_global_css
apply_global_css()

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1B5E20;
        text-align: center;
        padding: 1rem 0;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E7D32;
        text-align: center;
        padding: 0.5rem 0;
        font-weight: 600;
    }
    .phase-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        border: 1px solid #e0e0e0;
    }
    .phase-card h3 {
        color: #1B5E20;
        margin-top: 0;
        font-weight: bold;
    }
    .phase-card h4 {
        color: #2E7D32;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    .phase-card p {
        color: #212121;
        line-height: 1.6;
        font-weight: 500;
    }
    .phase-card ul {
        color: #424242;
        line-height: 1.8;
    }
    .phase-card li {
        color: #424242;
        margin: 0.3rem 0;
        color: #424242 !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 5px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
    }
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #616161;
        font-size: 0.9rem;
    }
    /* Seção de Tecnologias - Fundo branco e fonte escura */
    .main {
        background-color: #999 !important;
    }
    .stApp {
        background-color: #999 !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #999 !important;
    }
    .stMarkdown h2 {
        color: #1B5E20 !important;
    }
    .stMarkdown strong {
        color: #2E7D32 !important;
        font-weight: 700;
    }
    .stMarkdown ul {
        color: #fff;
    }
    .stMarkdown li {
        color: #fff;
        line-height: 1.8;
    }
    .stMarkdown p {
        color: #212121;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🌾 FarmTech Solutions</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema Integrado de Gestão Agrícola</p>', unsafe_allow_html=True)

# Informações do sidebar
with st.sidebar:
    st.markdown("### 👥 Equipe")
    st.markdown("""
    - Italo Domingues (RM 561787)
    - Maison Ramos (RM 565616)
    """)

# Conteúdo principal
st.markdown("## 📋 Visão Geral do Sistema")

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Fases Integradas",
        value="5",
        delta="100%",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="Tecnologias",
        value="15+",
        delta="Python, R, ML, IoT",
        delta_color="off"
    )

with col3:
    st.metric(
        label="Modelos ML",
        value="6",
        delta="99% acurácia",
        delta_color="normal"
    )

with col4:
    st.metric(
        label="Sensores IoT",
        value="4",
        delta="Tempo real",
        delta_color="normal"
    )

st.markdown("---")

# Descrição das fases
st.markdown("## 🎯 Fases do Projeto")

# Linha 1: Fases 1, 2, 3
col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown("""
        <div class="phase-card">
            <h3>📐 Fase 1</h3>
            <h4>Cálculos e Insumos</h4>
            <p>Sistema de cálculo de área de plantio e gerenciamento de insumos agrícolas.</p>
            <ul>
                <li>Cálculo de área circular/retangular</li>
                <li>Gestão de insumos (Café e Soja)</li>
                <li>Análise estatística com R</li>
                <li>Operações CRUD completas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown("""
        <div class="phase-card">
            <h3>🌾 Fase 2</h3>
            <h4>CanaTrack360</h4>
            <p>Sistema de rastreabilidade de colheita de cana-de-açúcar.</p>
            <ul>
                <li>Registro de colheitas</li>
                <li>Análise de perdas</li>
                <li>Banco de dados Oracle</li>
                <li>Rankings de produtividade</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown("""
        <div class="phase-card">
            <h3>🤖 Fase 3</h3>
            <h4>IoT e Machine Learning</h4>
            <p>Sistema IoT com ESP32 e modelos preditivos.</p>
            <ul>
                <li>Sensores: DHT22, LDR, botões</li>
                <li>Irrigação automática</li>
                <li>5 modelos ML (99% acurácia)</li>
                <li>PostgreSQL com CRUD</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Linha 2: Fases 4 e 6
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("""
        <div class="phase-card">
            <h3>💧 Fase 4</h3>
            <h4>Dashboard e IA</h4>
            <p>Dashboard interativo com predições em tempo real.</p>
            <ul>
                <li>Interface Streamlit</li>
                <li>RandomForest preditivo</li>
                <li>Gráficos interativos</li>
                <li>Monitoramento contínuo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown("""
        <div class="phase-card">
            <h3>👁️ Fase 6</h3>
            <h4>Visão Computacional</h4>
            <p>Detecção de objetos com YOLOv8.</p>
            <ul>
                <li>YOLOv8 nano</li>
                <li>3 modelos: 30, 60 e 100 épocas</li>
                <li>82 imagens (cats/dogs)</li>
                <li>Correção de labels e retreinamento</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Tecnologias utilizadas
st.markdown("## 💻 Tecnologias Utilizadas")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    **Linguagens:**
    - Python 3.11+
    - R 4.0+
    - C/C++ (Arduino)
    - SQL
    """)

with col2:
    st.markdown("""
    **Frameworks:**
    - Streamlit
    - Scikit-learn
    - PyTorch
    - Ultralytics YOLO
    """)

with col3:
    st.markdown("""
    **Bancos de Dados:**
    - PostgreSQL
    - Oracle DB
    - JSON (local)
    """)

with col4:
    st.markdown("""
    **IoT:**
    - ESP32
    - Sensores (DHT22, LDR)
    - Automação
    """)

st.markdown("---")

# Rodapé
st.markdown("""
<div class="footer">
    <p><strong>FarmTech Solutions</strong> - Sistema Integrado de Gestão Agrícola</p>
    <p>Fase 7 - FIAP | 2025</p>
    <p>🤖 Desenvolvido com tecnologias de ponta para o agronegócio do futuro</p>
</div>
""", unsafe_allow_html=True)
