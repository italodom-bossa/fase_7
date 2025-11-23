"""
Página Fase 4 - Irrigação Inteligente com ML
FarmTech Solutions - Dashboard Integrado
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path
import numpy as np

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from servicos.fase4_ml import (
    ModeloIrrigacao,
    AnalisadorHistoricoML,
    gerar_dados_exemplo_ml,
    calcular_impacto_ml
)

# Configuração da página
st.set_page_config(
    page_title="Fase 4 - Irrigação Inteligente com ML",
    page_icon="💧",
    layout="wide"
)

# Importar e aplicar CSS global
from styles import apply_global_css
apply_global_css()

# CSS customizado
st.markdown("""
<style>
    /* Fundo branco para toda a página */
    .main {
        background-color: #999 !important;
    }
    .stApp {
        background-color: #999 !important;
    }
    [data-testid="stAppViewContainer"] {
        # background-color: #ffffff !important;
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .positive-prediction {
        background-color: #FFEBEE;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #F44336;
        margin: 10px 0;
    }
    .negative-prediction {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 10px 0;
    }
    .impact-box {
        background-color: #E3F2FD;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("💧 Fase 4 - Irrigação Inteligente com Machine Learning")
st.markdown("### Sistema Preditivo de Irrigação com Scikit-learn")

st.markdown("---")

# Descrição
with st.expander("ℹ️ Sobre o Sistema de IA"):
    st.markdown("""
    **Irrigação Inteligente com ML** utiliza um modelo RandomForest treinado para:

    - **Prever necessidade de irrigação** baseado em sensores (pH, umidade, nutrientes)
    - **Otimizar consumo de água** reduzindo desperdícios em ~20%
    - **Considerar múltiplas variáveis** simultaneamente
    - **Fornecer recomendações** com índice de confiança

    **Variáveis de Entrada:**
    - 💧 **Umidade do Solo:** 0-100% (ideal: 40-80%)
    - 🧪 **pH do Solo:** 0-14 (ideal: 5.5-7.5)
    - 🌱 **Fósforo:** 0-1.5 (ideal: ≥0.8)
    - 🌾 **Potássio:** 0-1.5 (ideal: ≥0.8)

    **Benefícios:**
    - ✅ Economia de água até 20%
    - ✅ Redução de custos operacionais
    - ✅ Menor impacto ambiental
    - ✅ Melhor desenvolvimento das plantas
    """)

st.markdown("---")

# Inicializar session state
if 'historico_predicoes_ml' not in st.session_state:
    predicoes, df_sensores = gerar_dados_exemplo_ml()
    st.session_state.historico_predicoes_ml = predicoes
    st.session_state.df_sensores_ml = df_sensores

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🧠 Preditor", "📊 Análise Histórica", "💰 Impacto", "📈 Dados"])

# TAB 1: PREDITOR
with tab1:
    st.markdown("## 🧠 Preditor de Irrigação com ML")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Entrada de Sensores")

        col_input1, col_input2 = st.columns(2)

        with col_input1:
            umidade = st.slider(
                "💧 Umidade do Solo (%)",
                min_value=0.0,
                max_value=100.0,
                value=45.0,
                step=0.1,
                help="Percentual de umidade no solo"
            )

            fosforo = st.slider(
                "🌱 Fósforo",
                min_value=0.0,
                max_value=1.5,
                value=1.0,
                step=0.1
            )

        with col_input2:
            ph = st.slider(
                "🧪 pH do Solo",
                min_value=3.0,
                max_value=9.0,
                value=6.5,
                step=0.1,
                help="Escala de acidez/alcalinidade"
            )

            potassio = st.slider(
                "🌾 Potássio",
                min_value=0.0,
                max_value=1.5,
                value=1.0,
                step=0.1
            )

        # Botão para prever
        if st.button("🔮 Fazer Predição", type="primary", use_container_width=True):
            modelo = ModeloIrrigacao()
            resultado = modelo.prever_irrigacao(fosforo, potassio, ph, umidade)

            # Adicionar ao histórico
            resultado["timestamp"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            resultado["umidade"] = umidade
            resultado["ph"] = ph
            resultado["fosforo"] = fosforo
            resultado["potassio"] = potassio

            st.session_state.historico_predicoes_ml.append(resultado)

            # Exibir resultado
            st.markdown("### Resultado da Predição")

            if resultado["deve_irrigar"]:
                st.markdown(f"""
                <div class="positive-prediction">
                    <h3>💧 {resultado['recomendacao']}</h3>
                    <p><strong>Confiança:</strong> {resultado['confianca']:.1f}%</p>
                    <p><strong>Motivo:</strong> {resultado['motivo']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="negative-prediction">
                    <h3>✅ {resultado['recomendacao']}</h3>
                    <p><strong>Confiança:</strong> {resultado['confianca']:.1f}%</p>
                    <p><strong>Motivo:</strong> {resultado['motivo']}</p>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("### Status dos Sensores")

        # Cards de status
        cor_umidade = "🟢" if 40 <= umidade <= 80 else "🔴"
        cor_ph = "🟢" if 5.5 <= ph <= 7.5 else "🔴"
        cor_fosforo = "🟢" if fosforo >= 0.8 else "🔴"
        cor_potassio = "🟢" if potassio >= 0.8 else "🔴"

        st.markdown(f"""
        <div class="prediction-card">
            <h4>{cor_umidade} Umidade</h4>
            <h2>{umidade:.1f}%</h2>
            <p>Ideal: 40-80%</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="prediction-card">
            <h4>{cor_ph} pH</h4>
            <h2>{ph:.2f}</h2>
            <p>Ideal: 5.5-7.5</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: ANÁLISE HISTÓRICA
with tab2:
    st.markdown("## 📊 Análise Histórica de Predições")

    if st.session_state.historico_predicoes_ml:
        analisador = AnalisadorHistoricoML(st.session_state.historico_predicoes_ml)
        stats = analisador.estatisticas_gerais()

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total de Predições",
                stats["total_predicoes"]
            )

        with col2:
            st.metric(
                "Irrigações Recomendadas",
                stats["predicoes_positivas"]
            )

        with col3:
            st.metric(
                "Sem Necessidade",
                stats["predicoes_negativas"]
            )

        with col4:
            st.metric(
                "Confiança Média",
                f"{stats['confianca_media']:.1f}%"
            )

        st.markdown("---")

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de tendência de umidade
            umidades = analisador.tendencia_umidade()
            fig_umidade = go.Figure()
            fig_umidade.add_trace(go.Scatter(
                y=umidades,
                mode='lines+markers',
                name='Umidade',
                line=dict(color='#2196F3'),
                fill='tozeroy'
            ))
            fig_umidade.update_layout(
                title="💧 Tendência de Umidade",
                xaxis_title="Leitura",
                yaxis_title="Umidade (%)",
                hovermode='x unified'
            )
            st.plotly_chart(fig_umidade, use_container_width=True)

        with col2:
            # Gráfico de tendência de pH
            phs = analisador.tendencia_ph()
            fig_ph = go.Figure()
            fig_ph.add_trace(go.Scatter(
                y=phs,
                mode='lines+markers',
                name='pH',
                line=dict(color='#4CAF50'),
                fill='tozeroy'
            ))
            fig_ph.update_layout(
                title="🧪 Tendência de pH",
                xaxis_title="Leitura",
                yaxis_title="pH",
                hovermode='x unified'
            )
            st.plotly_chart(fig_ph, use_container_width=True)

        st.markdown("---")

        # Distribuição de confiança
        confianca_dist = analisador.predicoes_por_confianca()
        fig_confianca = px.bar(
            x=list(confianca_dist.keys()),
            y=list(confianca_dist.values()),
            title="Distribuição de Confiança das Predições",
            labels={"x": "Faixa de Confiança", "y": "Quantidade"},
            color_discrete_sequence=["#FF6B6B"]
        )
        st.plotly_chart(fig_confianca, use_container_width=True)

        st.markdown("---")

        # Tabela de histórico
        st.markdown("### 📋 Histórico Completo de Predições")
        df_historico = pd.DataFrame(st.session_state.historico_predicoes_ml)

        # Selecionar colunas para exibição (apenas as que existem)
        desired_cols = ["timestamp", "recomendacao", "confianca", "umidade", "ph", "fosforo", "potassio"]
        display_cols = [col for col in desired_cols if col in df_historico.columns]
        df_display = df_historico[display_cols].tail(20)

        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("📭 Nenhuma predição realizada ainda. Use a aba 'Preditor' para começar.")

# TAB 3: IMPACTO
with tab3:
    st.markdown("## 💰 Análise de Impacto Econômico e Ambiental")

    col1, col2, col3 = st.columns(3)

    with col1:
        area_hectares = st.number_input(
            "Área da propriedade (hectares):",
            min_value=1.0,
            max_value=1000.0,
            value=10.0,
            step=0.5
        )

    with col2:
        st.info(f"📊 Total de predições: {len(st.session_state.historico_predicoes_ml)}")

    with col3:
        predicoes_positivas = sum(
            1 for p in st.session_state.historico_predicoes_ml
            if p.get("deve_irrigar", False)
        )
        st.info(f"💧 Irrigações recomendadas: {predicoes_positivas}")

    st.markdown("---")

    # Calcular impacto
    impacto = calcular_impacto_ml(
        predicoes_positivas,
        len(st.session_state.historico_predicoes_ml),
        area_hectares
    )

    # Exibir impacto
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="impact-box">
            <h4>💧 Consumo Total</h4>
            <h2>{impacto['consumo_total_litros']:,}</h2>
            <p>litros</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="impact-box">
            <h4>♻️ Economia de Água</h4>
            <h2>{impacto['economia_litros']:,}</h2>
            <p>litros economizados</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="impact-box">
            <h4>💰 Economia Financeira</h4>
            <h2>R$ {impacto['economia_custo']:.2f}</h2>
            <p>economia estimada</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="impact-box">
            <h4>🌍 Redução CO₂</h4>
            <h2>{impacto['reducao_emissoes']:.2f}</h2>
            <p>kg de CO₂</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Resumo detalhado
    st.markdown("### 📈 Resumo Detalhado")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Dados Financeiros:**
        - Custo total de água: R$ {impacto['custo_total']:.2f}
        - Economia com otimização: R$ {impacto['economia_custo']:.2f}
        - Percentual economizado: ~20%
        """)

    with col2:
        st.markdown(f"""
        **Impacto Ambiental:**
        - Emissões totais: {impacto['emissoes_kg_co2']:.2f} kg CO₂
        - Redução de emissões: {impacto['reducao_emissoes']:.2f} kg CO₂
        - Equivalente a ~{int(impacto['reducao_emissoes'] * 0.5)} km rodados a menos
        """)

# TAB 4: DADOS
with tab4:
    st.markdown("## 📈 Dados de Sensores (24h)")

    df_sensores = st.session_state.df_sensores_ml

    if not df_sensores.empty:
        # Tabela
        st.dataframe(df_sensores, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Estatísticas
        st.markdown("### 📊 Estatísticas dos Sensores")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Umidade Média",
                f"{df_sensores['umidade'].mean():.1f}%",
                f"Min: {df_sensores['umidade'].min():.1f}% | Max: {df_sensores['umidade'].max():.1f}%"
            )

        with col2:
            st.metric(
                "pH Médio",
                f"{df_sensores['ph'].mean():.2f}",
                f"Min: {df_sensores['ph'].min():.2f} | Max: {df_sensores['ph'].max():.2f}"
            )

        with col3:
            st.metric(
                "Fósforo Médio",
                f"{df_sensores['fosforo'].mean():.2f}",
                f"Min: {df_sensores['fosforo'].min():.2f} | Max: {df_sensores['fosforo'].max():.2f}"
            )

        with col4:
            st.metric(
                "Potássio Médio",
                f"{df_sensores['potassio'].mean():.2f}",
                f"Min: {df_sensores['potassio'].min():.2f} | Max: {df_sensores['potassio'].max():.2f}"
            )

st.markdown("---")

# Rodapé
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><strong>Fase 4</strong> - Irrigação Inteligente com Machine Learning</p>
    <p>Predições com RandomForest | Otimização de Consumo de Água</p>
    <p>FarmTech Solutions | FIAP 2025</p>
</div>
""", unsafe_allow_html=True)
