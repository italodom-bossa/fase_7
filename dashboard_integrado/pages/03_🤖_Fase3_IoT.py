"""
Página Fase 3 - IoT e Sensores
FarmTech Solutions - Dashboard Integrado
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import time
from pathlib import Path
from datetime import datetime

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from servicos.fase3_iot import (
    Sensor,
    SistemaIrrigacao,
    gerar_dados_exemplo_sensores,
    gerar_alertas_sensores,
    calcular_historico_resumido,
    carregar_sensores_do_banco,
    simular_e_salvar_leituras,
    carregar_alertas,
    carregar_historico_irrigacao,
    adicionar_contato,
    remover_contato,
    listar_contatos_ativos,
    contar_contatos_ativos
)
from servicos.database import init_fase3_db

# Configuração da página
st.set_page_config(
    page_title="Fase 3 - IoT e Sensores",
    page_icon="🤖",
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
    .sensor-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .alerta-critico {
        background-color: #FFEBEE;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #F44336;
        margin: 10px 0;
    }
    .alerta-alto {
        background-color: #FFF3E0;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 10px 0;
    }
    .alerta-medio {
        background-color: #E3F2FD;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 10px 0;
    }
    /* Cor dos links de email */
    a {
        color: #2C3E50 !important;
        text-decoration: none !important;
    }
    /* Força cor escura no markdown */
    .stMarkdown a {
        color: #2C3E50 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 Fase 3 - IoT e Sensores")
st.markdown("### Sistema de Monitoramento de Sensores com Irrigação Automática")

st.markdown("---")

# Descrição
with st.expander("ℹ️ Sobre o Sistema IoT"):
    st.markdown("""
    **Sistema IoT FarmTech** monitora em tempo real:

    - **DHT22**: Umidade e Temperatura
    - **LDR**: pH do Solo (simulado)
    - **Botões**: Presença de Nutrientes (Fósforo/Potássio)

    **Irrigação Automática:**
    Aciona bomba quando:
    - ✅ Umidade < 40%
    - ✅ pH entre 5.5 e 7.5
    - ✅ Nutrientes presentes

    **Integração AWS:**
    Alertas enviados via SNS quando anomalias detectadas
    """)

st.markdown("---")

# Inicializar banco de dados
init_fase3_db()

# Header com botão de atualização
col_header1, col_header2 = st.columns([4, 1])

with col_header1:
    st.caption(f"🔄 Última atualização: {datetime.now().strftime('%H:%M:%S')}")

with col_header2:
    if st.button("🔄 Atualizar", use_container_width=True):
        st.rerun()

# Carregar dados do banco de dados
sensores = carregar_sensores_do_banco()

# Se não houver dados, usar exemplos
if not sensores["DHT22_01"].leituras:
    sensores = gerar_dados_exemplo_sensores()
else:
    # Gerar e salvar novas leituras simuladas a cada atualização
    sensores = simular_e_salvar_leituras()

# Verificar alertas críticos e mostrar banner
alertas_criticos = [a for a in carregar_alertas(limite=5) if a['severidade'] == 'crítico']
total_contatos_banner = contar_contatos_ativos()

if alertas_criticos:
    if total_contatos_banner > 0:
        st.markdown(f"""
        <div style="background-color: #FFEBEE; padding: 15px; border-radius: 10px; border-left: 6px solid #F44336; margin: 20px 0; animation: pulse 2s infinite;">
            <h3 style="color: #C62828; margin: 0;">🚨 ALERTA CRÍTICO - Notificação Enviada ✅</h3>
            <p style="margin: 10px 0 0 0; font-size: 1.1rem;">
                <strong>{alertas_criticos[0]['titulo']}</strong><br>
                {alertas_criticos[0]['mensagem']}<br>
                <small>📧 {total_contatos_banner} contato(s) notificado(s) via AWS SNS | 🕐 {alertas_criticos[0]['timestamp']}</small>
            </p>
        </div>
        <style>
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.85; }}
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: #FFF3E0; padding: 15px; border-radius: 10px; border-left: 6px solid #FF9800; margin: 20px 0; animation: pulse 2s infinite;">
            <h3 style="color: #E65100; margin: 0;">🚨 ALERTA CRÍTICO - ⚠️ Notificação NÃO Enviada</h3>
            <p style="margin: 10px 0 0 0; font-size: 1.1rem;">
                <strong>{alertas_criticos[0]['titulo']}</strong><br>
                {alertas_criticos[0]['mensagem']}<br>
                <small>❌ Sem contatos cadastrados! Acesse <strong>📇 Contatos</strong> para adicionar | 🕐 {alertas_criticos[0]['timestamp']}</small>
            </p>
        </div>
        <style>
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.85; }}
        }}
        </style>
        """, unsafe_allow_html=True)

# Inicializar sistema de irrigação
if 'sistema_irrigacao' not in st.session_state:
    st.session_state.sistema_irrigacao = SistemaIrrigacao()
    # Carregar histórico do banco
    historico_db = carregar_historico_irrigacao()
    if historico_db:
        st.session_state.sistema_irrigacao.historico_acionamentos = historico_db

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🚨 Alertas", "💧 Irrigação", "📈 Histórico", "📇 Contatos"])

# TAB 1: DASHBOARD
with tab1:
    st.markdown("## 📊 Dashboard de Sensores em Tempo Real")

    # Cards de sensores
    col1, col2, col3, col4 = st.columns(4)

    # DHT22 - Umidade
    with col1:
        umidade = sensores["DHT22_01"].ultima_leitura()
        cor_umidade = "🟢" if 40 <= umidade <= 80 else "🔴"

        st.markdown(f"""
        <div class="sensor-card">
            <h3>💧 Umidade</h3>
            <h2>{cor_umidade} {umidade:.1f}%</h2>
            <p>Ideal: 40-80%</p>
        </div>
        """, unsafe_allow_html=True)

    # LDR - pH
    with col2:
        ph = sensores["LDR_01"].ultima_leitura()
        cor_ph = "🟢" if 5.5 <= ph <= 7.5 else "🔴"

        st.markdown(f"""
        <div class="sensor-card">
            <h3>🧪 pH</h3>
            <h2>{cor_ph} {ph:.2f}</h2>
            <p>Ideal: 5.5-7.5</p>
        </div>
        """, unsafe_allow_html=True)

    # Fósforo
    with col3:
        fosforo = sensores["BTN_FOSFORO"].ultima_leitura()
        status_fosforo = "✅ Presente" if fosforo == 1 else "❌ Ausente"

        st.markdown(f"""
        <div class="sensor-card">
            <h3>🌱 Fósforo</h3>
            <h2>{status_fosforo}</h2>
            <p>Nutriente essencial</p>
        </div>
        """, unsafe_allow_html=True)

    # Potássio
    with col4:
        potassio = sensores["BTN_POTASSIO"].ultima_leitura()
        status_potassio = "✅ Presente" if potassio == 1 else "❌ Ausente"

        st.markdown(f"""
        <div class="sensor-card">
            <h3>🌾 Potássio</h3>
            <h2>{status_potassio}</h2>
            <p>Nutriente essencial</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de Umidade
        leituras_umidade = [l.valor for l in sensores["DHT22_01"].leituras]
        timestamps = [l.timestamp.split()[-1] for l in sensores["DHT22_01"].leituras]

        fig_umidade = go.Figure()
        fig_umidade.add_trace(go.Scatter(
            x=list(range(len(leituras_umidade))),
            y=leituras_umidade,
            mode='lines+markers',
            name='Umidade',
            line=dict(color='#2196F3'),
            fill='tozeroy'
        ))
        fig_umidade.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Mín: 40%")
        fig_umidade.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Máx: 80%")
        fig_umidade.update_layout(
            title="📊 Umidade (últimas 24h)",
            xaxis_title="Horas",
            yaxis_title="Umidade (%)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_umidade, use_container_width=True)

    with col2:
        # Gráfico de pH
        leituras_ph = [l.valor for l in sensores["LDR_01"].leituras]

        fig_ph = go.Figure()
        fig_ph.add_trace(go.Scatter(
            x=list(range(len(leituras_ph))),
            y=leituras_ph,
            mode='lines+markers',
            name='pH',
            line=dict(color='#4CAF50'),
            fill='tozeroy'
        ))
        fig_ph.add_hline(y=5.5, line_dash="dash", line_color="orange", annotation_text="Mín: 5.5")
        fig_ph.add_hline(y=7.5, line_dash="dash", line_color="orange", annotation_text="Máx: 7.5")
        fig_ph.update_layout(
            title="🧪 pH (últimas 24h)",
            xaxis_title="Horas",
            yaxis_title="pH",
            hovermode='x unified'
        )
        st.plotly_chart(fig_ph, use_container_width=True)

# TAB 2: ALERTAS
with tab2:
    st.markdown("## 🚨 Alertas do Sistema")

    # Carregar alertas do banco de dados
    alertas = carregar_alertas(limite=10)

    # Verificar se há contatos cadastrados
    contatos = listar_contatos_ativos()
    total_contatos = len(contatos)

    if alertas:
        st.warning(f"⚠️ {len(alertas)} alerta(s) detectado(s)")

        # Mostrar notificação de envio apenas se houver contatos
        if total_contatos > 0:
            st.success("📧 **Notificações enviadas via AWS SNS**")

            # Montar lista de e-mails
            emails = [c['email'] for c in contatos]

            st.markdown(f"""
            <div style="background-color: #E8F5E9; padding: 15px; border-radius: 5px; border-left: 4px solid #4CAF50; margin: 10px 0; color: #1B5E20;">
                ✅ <strong>E-mails enviados para {len(emails)} contato(s):</strong><br>
                <span style="color: #2E7D32;">{', '.join(emails)}</span><br><br>
                🕐 <strong>Última notificação:</strong> <span style="color: #2E7D32;">{alertas[0]['timestamp']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ **Notificações NÃO enviadas - Sem contatos cadastrados**")
            st.markdown("""
            <div style="background-color: #FFEBEE; padding: 15px; border-radius: 5px; border-left: 4px solid #F44336; margin: 10px 0;">
                ⚠️ <strong>Nenhum contato cadastrado para receber notificações!</strong><br>
                Acesse a aba <strong>📇 Contatos</strong> para adicionar destinatários das notificações.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        for alerta in alertas:
            timestamp_formatado = alerta['timestamp']

            if alerta["severidade"] == "crítico":
                st.markdown(f"""
                <div class="alerta-critico" style="color: #B71C1C;">
                    <strong>🚨 {alerta['titulo']}</strong><br>
                    <span style="color: #C62828;">{alerta['mensagem']}</span><br>
                    <small style="color: #D32F2F;">🕐 {timestamp_formatado} | 📧 Notificação enviada</small>
                </div>
                """, unsafe_allow_html=True)
            elif alerta["severidade"] == "alto":
                st.markdown(f"""
                <div class="alerta-alto" style="color: #E65100;">
                    <strong>⚠️ {alerta['titulo']}</strong><br>
                    <span style="color: #EF6C00;">{alerta['mensagem']}</span><br>
                    <small style="color: #F57C00;">🕐 {timestamp_formatado} | 📧 Notificação enviada</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alerta-medio" style="color: #01579B;">
                    <strong>ℹ️ {alerta['titulo']}</strong><br>
                    <span style="color: #0277BD;">{alerta['mensagem']}</span><br>
                    <small style="color: #0288D1;">🕐 {timestamp_formatado} | 📧 Notificação enviada</small>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.success("✅ Nenhum alerta. Sistema operacional normal!")

# TAB 3: IRRIGAÇÃO
with tab3:
    st.markdown("## 💧 Sistema de Irrigação Automática")

    # Carregar histórico do banco
    historico_irrigacao = carregar_historico_irrigacao(limite=20)

    # Verificar condições atuais
    umidade_atual = sensores["DHT22_01"].ultima_leitura()
    ph_atual = sensores["LDR_01"].ultima_leitura()
    fosforo_presente = sensores["BTN_FOSFORO"].ultima_leitura() == 1
    potassio_presente = sensores["BTN_POTASSIO"].ultima_leitura() == 1
    nutrientes_presentes = fosforo_presente and potassio_presente

    # Determinar se deve estar ativo
    deve_irrigar = umidade_atual < 40 and (5.5 <= ph_atual <= 7.5) and nutrientes_presentes

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Status do Sistema em Tempo Real")

        # Condições de acionamento
        st.markdown("**Condições de Acionamento:**")

        col_cond1, col_cond2, col_cond3 = st.columns(3)

        with col_cond1:
            if umidade_atual < 40:
                st.markdown("✅ **Umidade baixa (necessita irrigação)**")
                st.metric("Umidade", f"{umidade_atual:.1f}%", delta=f"{umidade_atual - 40:.1f}%", delta_color="inverse")
            else:
                st.markdown("⚪ **Umidade adequada (não precisa irrigar)**")
                st.metric("Umidade", f"{umidade_atual:.1f}%")

        with col_cond2:
            if 5.5 <= ph_atual <= 7.5:
                st.markdown("✅ **pH ideal para irrigação**")
                st.metric("pH", f"{ph_atual:.2f}")
            else:
                st.markdown("❌ **pH inadequado (não pode irrigar)**")
                st.metric("pH", f"{ph_atual:.2f}", delta_color="off")

        with col_cond3:
            if nutrientes_presentes:
                st.markdown("✅ **Todos os nutrientes presentes**")
                st.metric("Fósforo", "Presente" if fosforo_presente else "Ausente")
                st.metric("Potássio", "Presente" if potassio_presente else "Ausente")
            else:
                st.markdown("❌ **Nutrientes insuficientes**")
                st.metric("Fósforo", "Presente" if fosforo_presente else "Ausente")
                st.metric("Potássio", "Presente" if potassio_presente else "Ausente")

        st.markdown("---")

        # Status da bomba
        if deve_irrigar:
            st.success("💧 **IRRIGAÇÃO ATIVA**")
            st.info("✅ Todas as condições atendidas! Sistema irrigando automaticamente.")
        else:
            st.info("⏹️ **IRRIGAÇÃO INATIVA**")

            # Explicar por que não está irrigando
            motivos = []
            if umidade_atual >= 40:
                motivos.append(f"• Umidade adequada ({umidade_atual:.1f}% - só irriga quando < 40%)")
            if not (5.5 <= ph_atual <= 7.5):
                motivos.append(f"• pH fora da faixa ideal ({ph_atual:.2f} - precisa estar entre 5.5-7.5)")
            if not nutrientes_presentes:
                if not fosforo_presente:
                    motivos.append("• Fósforo ausente")
                if not potassio_presente:
                    motivos.append("• Potássio ausente")

            if motivos:
                st.markdown("**Condições não atendidas:**")
                for motivo in motivos:
                    st.markdown(motivo)
            else:
                st.markdown("Aguardando condições para irrigação.")

    with col2:
        st.markdown("### Última Irrigação")

        if historico_irrigacao:
            ultima = historico_irrigacao[0]
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Última Irrigação</p>
                <h2 style="margin: 10px 0; font-size: 1.8rem;">🕐 {ultima['Timestamp'].split()[1]}</h2>
                <p style="margin: 5px 0; font-size: 0.85rem; opacity: 0.8;">{ultima['Timestamp'].split()[0]}</p>
                <hr style="border: 0; height: 1px; background: rgba(255,255,255,0.3); margin: 15px 0;">
                <p style="margin: 10px 0; font-size: 1rem;"><strong>{ultima['Motivo']}</strong></p>
                <p style="margin: 5px 0; font-size: 0.9rem;">⏱️ Duração: {ultima['Duração (min)']} minutos</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Nenhuma irrigação registrada ainda")

    st.markdown("---")

    # Histórico de acionamentos
    if historico_irrigacao:
        st.markdown("### 📋 Histórico de Acionamentos")
        df_historico = pd.DataFrame(historico_irrigacao)
        st.dataframe(df_historico, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum histórico de irrigação disponível")

# TAB 4: HISTÓRICO
with tab4:
    st.markdown("## 📈 Resumo do Histórico (24h)")

    df_resumo = calcular_historico_resumido(sensores, horas=24)

    if not df_resumo.empty:
        st.dataframe(df_resumo, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Distribuição de status
        status_counts = df_resumo["Status"].value_counts()

        fig_status = px.pie(
            names=status_counts.index,
            values=status_counts.values,
            title="Distribuição de Status dos Sensores",
            color_discrete_map={
                "✅ Ok": "#4CAF50",
                "⚠️ Baixo": "#FF9800",
                "⚠️ Alto": "#F44336"
            }
        )
        st.plotly_chart(fig_status, use_container_width=True)

# TAB 5: CONTATOS
with tab5:
    st.markdown("## 📇 Gerenciamento de Contatos para Notificações")

    st.markdown("""
    Cadastre os contatos que receberão notificações automáticas por e-mail
    quando alertas forem gerados pelo sistema IoT.
    """)

    st.markdown("---")

    # Formulário de cadastro
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### ➕ Adicionar Novo Contato")

        with st.form("form_adicionar_contato", clear_on_submit=True):
            nome_contato = st.text_input(
                "Nome Completo:",
                placeholder="Ex: João Silva",
                key="input_nome"
            )

            email_contato = st.text_input(
                "E-mail:",
                placeholder="Ex: joao.silva@farmtech.com",
                key="input_email"
            )

            submitted = st.form_submit_button("➕ Adicionar Contato", type="primary", use_container_width=True)

        # Processar fora do form para evitar conflitos
        if submitted:
            if not nome_contato or not email_contato:
                st.error("❌ Nome e e-mail são obrigatórios!")
            elif "@" not in email_contato:
                st.error("❌ E-mail inválido!")
            else:
                try:
                    if adicionar_contato(nome_contato, email_contato, None):
                        st.success(f"✅ Contato {nome_contato} adicionado com sucesso!")
                        time.sleep(1)  # Pequeno delay para mostrar mensagem
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar contato no banco de dados")
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")

    with col2:
        # Estatísticas
        total_contatos = contar_contatos_ativos()

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <h3>📊 Contatos Ativos</h3>
            <h1>{total_contatos}</h1>
            <p>receberão notificações</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if total_contatos > 0:
            st.info("✅ **Notificações ativas**\n\nOs contatos abaixo receberão alertas por e-mail via AWS SNS.")
        else:
            st.warning("⚠️ **Sem contatos cadastrados**\n\nAdicione contatos para receber notificações por e-mail.")

    st.markdown("---")

    # Lista de contatos
    st.markdown("### 📋 Contatos Cadastrados")

    contatos = listar_contatos_ativos()

    if contatos:
        # Criar DataFrame para exibição
        df_contatos = pd.DataFrame(contatos)

        # Adicionar colunas de ação
        for idx, contato in enumerate(contatos):
            col1, col2, col3 = st.columns([3, 6, 2])

            with col1:
                st.markdown(f"**{contato['nome']}**")

            with col2:
                st.markdown(f"<div style='color: #1a1a1a; font-size: 0.95rem;'>📧 {contato['email']}</div>", unsafe_allow_html=True)

            with col3:
                if st.button(f"🗑️ Remover", key=f"remover_{contato['id']}"):
                    if remover_contato(contato['id']):
                        st.success(f"✅ {contato['nome']} removido!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao remover")

            st.markdown("---")

    else:
        st.info("📭 Nenhum contato cadastrado ainda. Adicione contatos usando o formulário acima.")

st.markdown("---")

# Rodapé
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><strong>Fase 3</strong> - IoT e Sensores com Irrigação Automática</p>
    <p>Monitoramento em tempo real | Alertas via AWS SNS</p>
    <p>FarmTech Solutions | FIAP 2025</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh no final (só se não estiver em um formulário)
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

tempo_decorrido = time.time() - st.session_state.last_refresh
if tempo_decorrido >= 5:
    st.session_state.last_refresh = time.time()
    time.sleep(0.1)
    st.rerun()
