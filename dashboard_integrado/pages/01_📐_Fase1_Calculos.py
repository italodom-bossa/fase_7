"""
Página Fase 1 - Cálculo de Área e Insumos Agrícolas
FarmTech Solutions - Dashboard Integrado
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from servicos.fase1_calculos import (
    calcular_area_circulo,
    calcular_area_retangulo,
    converter_para_hectares,
    calcular_insumos,
    formatar_numero_br,
    calcular_custo_estimado,
    gerar_relatorio_completo
)
from config import INSUMOS_POR_CULTURA

# Configuração da página
st.set_page_config(
    page_title="Fase 1 - Cálculos Agrícolas",
    page_icon="📐",
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
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #1B5E20;
    }
    .resultado-card {
        background-color: #E8F5E9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 10px 0;
    }
    .custo-card {
        background-color: #FFF3E0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📐 Fase 1 - Cálculo de Área e Insumos Agrícolas")
st.markdown("### Sistema de Dimensionamento de Plantio e Gestão de Insumos")

st.markdown("---")

# Descrição
with st.expander("ℹ️ Sobre esta Fase"):
    st.markdown("""
    A **Fase 1** implementa um sistema completo para:

    - **Cálculo de Área:** Suporte a áreas circulares (café) e retangulares (soja)
    - **Conversão de Unidades:** Automática de m² para hectares
    - **Gestão de Insumos:** Cálculo preciso baseado na cultura e área
    - **Estimativa de Custos:** Valores aproximados para planejamento

    **Culturas Suportadas:**
    - 🌱 **Café:** Área circular, insumos específicos
    - 🌾 **Soja:** Área retangular, com Bradyrhizobium
    """)

st.markdown("---")

# Tabs para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["🧮 Calculadora", "📊 Tabela de Insumos", "📝 Histórico"])

# TAB 1: CALCULADORA
with tab1:
    st.markdown("## 🧮 Calculadora de Área e Insumos")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Dados da Cultura")

        # Seleção de cultura
        cultura_selecionada = st.selectbox(
            "Selecione a cultura:",
            options=list(INSUMOS_POR_CULTURA.keys()),
            help="Cada cultura tem insumos específicos"
        )

        # Tipo de área baseado na cultura
        if cultura_selecionada == "Café":
            tipo_area = "circular"
            st.info("☕ Café: Área circular (plantio em curvas de nível)")
        else:
            tipo_area = "retangular"
            st.info("🌾 Soja: Área retangular (plantio convencional)")

        st.markdown("### Dimensões da Área")

        # Campos de entrada baseados no tipo
        if tipo_area == "circular":
            raio = st.number_input(
                "Raio da área (metros):",
                min_value=1.0,
                max_value=10000.0,
                value=100.0,
                step=1.0,
                help="Raio da área circular em metros"
            )
            dimensoes = {"raio": raio}

        else:  # retangular
            col_dim1, col_dim2 = st.columns(2)
            with col_dim1:
                largura = st.number_input(
                    "Largura (metros):",
                    min_value=1.0,
                    max_value=10000.0,
                    value=200.0,
                    step=1.0
                )
            with col_dim2:
                comprimento = st.number_input(
                    "Comprimento (metros):",
                    min_value=1.0,
                    max_value=10000.0,
                    value=500.0,
                    step=1.0
                )
            dimensoes = {"largura": largura, "comprimento": comprimento}

        # Botão de cálculo
        calcular = st.button("🔍 Calcular Insumos", type="primary", use_container_width=True)

    with col2:
        st.markdown("### Resultados")

        if calcular:
            try:
                # Gerar relatório completo
                area_m2, hectares, insumos, custos = gerar_relatorio_completo(
                    cultura_selecionada,
                    tipo_area,
                    dimensoes
                )

                # Exibir área
                st.markdown(f"""
                <div class="resultado-card">
                    <h3>📏 Área Calculada</h3>
                    <p style="font-size: 20px;">
                        <strong>{formatar_numero_br(area_m2)} m²</strong><br>
                        ≈ <strong>{formatar_numero_br(hectares)} hectares</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Exibir insumos
                st.markdown("#### 🌱 Insumos Necessários")

                df_insumos = pd.DataFrame([
                    {
                        "Insumo": nome,
                        "Quantidade": f"{formatar_numero_br(valor)}",
                        "Custo (R$)": f"R$ {formatar_numero_br(custos[nome])}"
                    }
                    for nome, valor in insumos.items()
                ])

                st.dataframe(df_insumos, use_container_width=True, hide_index=True)

                # Custo total
                custo_total = custos["TOTAL"]
                st.markdown(f"""
                <div class="custo-card">
                    <h3>💰 Custo Total Estimado</h3>
                    <p style="font-size: 24px; color: #F57C00;">
                        <strong>R$ {formatar_numero_br(custo_total)}</strong>
                    </p>
                    <p style="font-size: 14px; color: #666;">
                        * Valores aproximados para planejamento
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Salvar no session_state para histórico
                if 'historico_calculos' not in st.session_state:
                    st.session_state.historico_calculos = []

                st.session_state.historico_calculos.append({
                    'cultura': cultura_selecionada,
                    'tipo_area': tipo_area,
                    'area_m2': area_m2,
                    'hectares': hectares,
                    'custo_total': custo_total
                })

                # Botão de download
                st.download_button(
                    label="📥 Baixar Relatório (CSV)",
                    data=df_insumos.to_csv(index=False).encode('utf-8'),
                    file_name=f"relatorio_insumos_{cultura_selecionada.lower()}.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"❌ Erro ao calcular: {str(e)}")

        else:
            st.info("👆 Preencha os dados e clique em 'Calcular Insumos'")

# TAB 2: TABELA DE INSUMOS
with tab2:
    st.markdown("## 📊 Tabela de Insumos por Cultura")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ☕ Café")
        df_cafe = pd.DataFrame([
            {"Insumo": k, "Quantidade/ha": f"{v} {k.split('(')[1].split(')')[0] if '(' in k else ''}"}
            for k, v in INSUMOS_POR_CULTURA["Café"].items()
        ])
        st.dataframe(df_cafe, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("### 🌾 Soja")
        df_soja = pd.DataFrame([
            {"Insumo": k, "Quantidade/ha": f"{v} {k.split('(')[1].split(')')[0] if '(' in k else ''}"}
            for k, v in INSUMOS_POR_CULTURA["Soja"].items()
        ])
        st.dataframe(df_soja, use_container_width=True, hide_index=True)

    st.info("""
    💡 **Nota:** Os valores apresentados são recomendações médias.
    Para um plano de adubação preciso, consulte um engenheiro agrônomo e realize análise de solo.
    """)

# TAB 3: HISTÓRICO
with tab3:
    st.markdown("## 📝 Histórico de Cálculos")

    if 'historico_calculos' in st.session_state and st.session_state.historico_calculos:
        df_historico = pd.DataFrame(st.session_state.historico_calculos)
        df_historico['area_m2'] = df_historico['area_m2'].apply(lambda x: formatar_numero_br(x))
        df_historico['hectares'] = df_historico['hectares'].apply(lambda x: formatar_numero_br(x))
        df_historico['custo_total'] = df_historico['custo_total'].apply(lambda x: f"R$ {formatar_numero_br(x)}")

        df_historico.columns = ['Cultura', 'Tipo de Área', 'Área (m²)', 'Hectares', 'Custo Total']

        st.dataframe(df_historico, use_container_width=True, hide_index=True)

        # Botão limpar histórico
        if st.button("🗑️ Limpar Histórico"):
            st.session_state.historico_calculos = []
            st.rerun()
    else:
        st.info("📭 Nenhum cálculo realizado ainda. Use a aba 'Calculadora' para começar.")

st.markdown("---")

# Informações adicionais
with st.expander("📚 Informações Técnicas"):
    st.markdown("""
    ### Fórmulas Utilizadas

    **Área Circular:**
    ```
    A = π × r²
    ```

    **Área Retangular:**
    ```
    A = largura × comprimento
    ```

    **Conversão para Hectares:**
    ```
    hectares = área_m² / 10.000
    ```

    **Cálculo de Insumos:**
    ```
    quantidade_insumo = valor_por_hectare × hectares
    ```

    ### Fontes de Dados
    - Embrapa - Recomendações de adubação
    - IAC - Instituto Agronômico de Campinas
    - Boas práticas agronômicas
    """)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><strong>Fase 1</strong> - Sistema de Cálculo de Área e Insumos Agrícolas</p>
    <p>FarmTech Solutions | FIAP 2025</p>
</div>
""", unsafe_allow_html=True)
