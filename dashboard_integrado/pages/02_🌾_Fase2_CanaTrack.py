"""
Página Fase 2 - CanaTrack360
FarmTech Solutions - Dashboard Integrado
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
from datetime import datetime

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from servicos.fase2_canatrack import (
    RegistroColheita,
    AnalisadorPerdas,
    gerar_dados_exemplo,
    salvar_registro,
    carregar_registros,
    inicializar_com_exemplos
)
from servicos.database import init_fase2_db

# Configuração da página
st.set_page_config(
    page_title="Fase 2 - CanaTrack360",
    page_icon="🌾",
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
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .warning-box {
        background-color: #FFF3E0;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌾 Fase 2 - CanaTrack360")
st.markdown("### Sistema de Rastreabilidade e Análise de Perdas na Colheita")

st.markdown("---")

# Descrição
with st.expander("ℹ️ Sobre o CanaTrack360"):
    st.markdown("""
    **CanaTrack360** é um sistema completo de rastreabilidade que permite:

    - **Registrar cada colheita** com dados detalhados
    - **Analisar perdas** em tempo real
    - **Identificar gargalos** operacionais
    - **Comparar desempenho** entre operadores e máquinas
    - **Gerar sugestões** de melhoria

    **Funcionalidades:**
    - 📊 Análise de perdas por talhão
    - 🏆 Rankings de operadores e máquinas
    - 📈 Gráficos comparativos
    - 💡 Sugestões automatizadas
    - 📥 Importação de dados
    """)

st.markdown("---")

# Inicializar banco de dados
init_fase2_db()
inicializar_com_exemplos()

# Inicializar session state
if 'registros' not in st.session_state:
    st.session_state.registros = carregar_registros()
    if not st.session_state.registros:
        st.session_state.registros = gerar_dados_exemplo()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Novo Registro", "📊 Análise de Perdas", "🏆 Rankings", "💡 Sugestões"])

# TAB 1: NOVO REGISTRO
with tab1:
    st.markdown("## 📋 Registrar Nova Colheita")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Informações da Colheita")

        talhao = st.text_input(
            "Talhão:",
            placeholder="ex: A1",
            help="Identificação do talhão"
        )

        data_colheita = st.date_input(
            "Data da Colheita:",
            value=datetime.now()
        )

        tipo_colheita = st.selectbox(
            "Tipo de Colheita:",
            ["Mecanizada", "Manual", "Mista"]
        )

        quantidade_colhida = st.number_input(
            "Quantidade Colhida (toneladas):",
            min_value=0.0,
            step=0.1,
            value=100.0
        )

    with col2:
        st.markdown("### Equipamento e Operador")

        maquina = st.text_input(
            "Máquina/Colheitadeira:",
            placeholder="ex: Colheitadeira 01"
        )

        operador = st.text_input(
            "Operador:",
            placeholder="Nome do operador"
        )

        st.markdown("### Perdas Estimadas")

        col_perdas1, col_perdas2 = st.columns(2)
        with col_perdas1:
            perda_estimada = st.number_input(
                "Perda Estimada (t):",
                min_value=0.0,
                step=0.1,
                value=10.0
            )

        with col_perdas2:
            perda_real = st.number_input(
                "Perda Real (t):",
                min_value=0.0,
                step=0.1,
                value=5.0
            )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Condições")

        causa_perda = st.selectbox(
            "Causa da Perda:",
            [
                "Regulagem inadequada",
                "Desgaste de componentes",
                "Falha operacional",
                "Umidade alta",
                "Condições climáticas",
                "Outra"
            ]
        )

        condicao_solo = st.selectbox(
            "Condição do Solo:",
            ["Normal", "Úmido", "Seco", "Desfavorável"]
        )

    with col2:
        st.markdown("### Informações Adicionais")

        condicao_clima = st.selectbox(
            "Condição do Clima:",
            ["Seco", "Chuvoso", "Nublado", "Ventoso", "Normal"]
        )

        severidade_perda = st.selectbox(
            "Severidade da Perda:",
            ["Leve", "Média", "Alto", "Crítico"]
        )

    st.markdown("---")

    # Botão para registrar
    if st.button("✅ Registrar Colheita", type="primary", use_container_width=True):
        if not all([talhao, maquina, operador]):
            st.error("❌ Preencha todos os campos obrigatórios!")
        else:
            novo_registro = RegistroColheita(
                talhao=talhao,
                maquina=maquina,
                operador=operador,
                data_colheita=str(data_colheita),
                quantidade_colhida=quantidade_colhida,
                tipo_colheita=tipo_colheita,
                perda_estimada=perda_estimada,
                perda_real=perda_real,
                causa_perda=causa_perda,
                condicao_solo=condicao_solo,
                condicao_clima=condicao_clima,
                severidade_perda=severidade_perda
            )

            # Salvar no banco de dados
            if salvar_registro(novo_registro):
                st.session_state.registros.insert(0, novo_registro)
                st.success("✅ Colheita registrada com sucesso no banco de dados!")
            else:
                st.error("❌ Erro ao salvar no banco de dados")

            # Exibir resumo
            st.markdown("### 📊 Resumo do Registro")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Talhão", talhao)
            with col2:
                st.metric("Quantidade (t)", f"{quantidade_colhida:.1f}")
            with col3:
                st.metric("Perda Real (t)", f"{perda_real:.1f}")
            with col4:
                pct_perda = (perda_real / quantidade_colhida * 100) if quantidade_colhida > 0 else 0
                st.metric("% Perda", f"{pct_perda:.2f}%")

# TAB 2: ANÁLISE DE PERDAS
with tab2:
    st.markdown("## 📊 Análise de Perdas")

    # Criar analisador
    analisador = AnalisadorPerdas(st.session_state.registros)

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
<div class="metric-box">
    <h3>📊 Colheitas Registradas</h3>
    <h2>{len(st.session_state.registros)}</h2>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
<div class="metric-box">
    <h3>📦 Quantidade Total</h3>
    <h2>{analisador.quantidade_colhida_total():.1f} t</h2>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
<div class="metric-box">
    <h3>📉 Perda Total</h3>
    <h2>{analisador.perda_total():.2f} t</h2>
</div>
""", unsafe_allow_html=True)

    with col4:
        pct_total = analisador.percentual_perda_geral()
        st.markdown(f"""
<div class="metric-box">
    <h3>📊 % Perda</h3>
    <h2>{pct_total:.2f}%</h2>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # Tabela de registros
    st.markdown("### 📋 Detalhamento de Colheitas")
    df_registros = pd.DataFrame([r.to_dict() for r in st.session_state.registros])

    # Remover coluna de ID para exibição
    display_cols = [col for col in df_registros.columns if col != "ID"]
    st.dataframe(df_registros[display_cols], use_container_width=True, hide_index=True)

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de perdas por severidade
        severidade_count = analisador.analise_severidade()
        if severidade_count:
            fig_sev = px.pie(
                names=list(severidade_count.keys()),
                values=list(severidade_count.values()),
                title="Distribuição por Severidade",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_sev, use_container_width=True)

    with col2:
        # Gráfico de causas
        causas = analisador.analise_causa()
        if causas:
            fig_causa = px.bar(
                x=list(causas.keys()),
                y=list(causas.values()),
                title="Causas de Perdas",
                labels={"x": "Causa", "y": "Quantidade"},
                color_discrete_sequence=["#FF6B6B"]
            )
            st.plotly_chart(fig_causa, use_container_width=True)

# TAB 3: RANKINGS
with tab3:
    st.markdown("## 🏆 Rankings")

    analisador = AnalisadorPerdas(st.session_state.registros)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 👨‍🌾 Ranking de Operadores")
        ranking_op = analisador.ranking_operadores()
        if not ranking_op.empty:
            st.dataframe(ranking_op, use_container_width=True)
        else:
            st.info("Nenhum dado disponível")

    with col2:
        st.markdown("### 🚜 Ranking de Máquinas")
        ranking_maq = analisador.ranking_maquinas()
        if not ranking_maq.empty:
            st.dataframe(ranking_maq, use_container_width=True)
        else:
            st.info("Nenhum dado disponível")

    with col3:
        st.markdown("### 🌱 Ranking de Talhões")
        ranking_tal = analisador.ranking_talhaos()
        if not ranking_tal.empty:
            st.dataframe(ranking_tal, use_container_width=True)
        else:
            st.info("Nenhum dado disponível")

# TAB 4: SUGESTÕES
with tab4:
    st.markdown("## 💡 Sugestões de Melhoria")

    analisador = AnalisadorPerdas(st.session_state.registros)
    sugestoes = analisador.sugestoes_melhorias()

    if sugestoes:
        for i, sugestao in enumerate(sugestoes, 1):
            st.markdown(f"""
            <div class="warning-box">
                <strong>{i}. {sugestao}</strong>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            <strong>✅ Nenhuma sugestão crítica no momento. Suas operações estão otimizadas!</strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Estatísticas gerais
    st.markdown("### 📈 Estatísticas Gerais")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Perda Média por Colheita",
            f"{analisador.perda_media():.2f} t"
        )

    with col2:
        st.metric(
            "Percentual de Perda Geral",
            f"{analisador.percentual_perda_geral():.2f}%"
        )

st.markdown("---")

# Rodapé
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><strong>Fase 2 - CanaTrack360</strong></p>
    <p>Sistema de Rastreabilidade e Análise de Perdas na Colheita Mecanizada</p>
    <p>FarmTech Solutions | FIAP 2025</p>
</div>
""", unsafe_allow_html=True)
