"""
Estilos CSS globais para o Dashboard FarmTech Solutions
Fornece classes de estilo padronizadas com bom contraste
"""

GLOBAL_CSS = """
<style>
    /* Variáveis de cor */
    :root {
        --primary-dark: #1B5E20;
        --primary-medium: #2E7D32;
        --primary-light: #4CAF50;
        --text-dark: #212121;
        --text-medium: #424242;
        --text-light: #616161;
        --background-light: #ffffff;
        --background-gray: #f5f5f5;
        --border-color: #e0e0e0;
        --success-bg: #E8F5E9;
        --success-border: #4CAF50;
        --warning-bg: #FFF3E0;
        --warning-border: #FF9800;
        --error-bg: #FFEBEE;
        --error-border: #F44336;
        --info-bg: #E3F2FD;
        --info-border: #2196F3;
    }

    /* Card base */
    .card-base {
        background-color: var(--background-light);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        border: 1px solid var(--border-color);
    }

    /* Sensor Card (Fase 3) */
    .sensor-card {
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-medium) 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: none;
    }

    .sensor-card h3 {
        color: white;
        margin: 10px 0;
        font-weight: 600;
    }

    .sensor-card h2 {
        color: white;
        margin: 5px 0;
        font-size: 2rem;
    }

    .sensor-card p {
        color: rgba(255, 255, 255, 0.9);
        margin: 5px 0;
        font-size: 0.9rem;
    }

    /* Alert Cards (Fase 3) */
    .alerta-critico {
        background-color: var(--error-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--error-border);
        margin: 10px 0;
    }

    .alerta-critico strong {
        color: var(--text-dark);
    }

    .alerta-alto {
        background-color: var(--warning-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--warning-border);
        margin: 10px 0;
    }

    .alerta-alto strong {
        color: var(--text-dark);
    }

    .alerta-medio {
        background-color: var(--info-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--info-border);
        margin: 10px 0;
    }

    .alerta-medio strong {
        color: var(--text-dark);
    }

    /* Prediction Cards (Fase 4) */
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .prediction-card h3 {
        color: white;
        margin: 0;
    }

    .prediction-card p {
        color: rgba(255, 255, 255, 0.95);
        margin: 8px 0;
    }

    .positive-prediction {
        background-color: var(--error-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--error-border);
        margin: 10px 0;
    }

    .positive-prediction h3 {
        color: var(--text-dark);
        margin: 0;
    }

    .positive-prediction p {
        color: var(--text-medium);
        margin: 8px 0;
    }

    .negative-prediction {
        background-color: var(--success-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--success-border);
        margin: 10px 0;
    }

    .negative-prediction h3 {
        color: var(--text-dark);
        margin: 0;
    }

    .negative-prediction p {
        color: var(--text-medium);
        margin: 8px 0;
    }

    /* Impact Box (Fase 4) */
    .impact-box {
        background-color: var(--info-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--info-border);
        margin: 10px 0;
    }

    .impact-box h4 {
        color: var(--text-dark);
        margin: 0;
    }

    .impact-box h2 {
        color: var(--primary-dark);
        margin: 10px 0;
    }

    .impact-box p {
        color: var(--text-medium);
        margin: 5px 0;
        font-size: 0.9rem;
    }

    /* Service Card (Fase 5) */
    .service-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .service-card h3 {
        color: white;
        margin: 10px 0;
        font-weight: 600;
    }

    .service-card p {
        color: rgba(255, 255, 255, 0.9);
        margin: 5px 0;
        font-size: 0.95rem;
    }

    /* Status Active (Fase 5) */
    .status-active {
        background-color: var(--success-bg);
        padding: 10px;
        border-radius: 5px;
        color: var(--primary-dark);
        font-weight: bold;
        border: 1px solid var(--success-border);
    }

    /* Cost Card (Fase 5) */
    .cost-card {
        background-color: var(--warning-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--warning-border);
        margin: 10px 0;
    }

    .cost-card strong {
        color: var(--text-dark);
    }

    /* Info Card (Fase 5) */
    .info-card {
        background-color: var(--info-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--info-border);
        margin: 10px 0;
    }

    .info-card strong {
        color: var(--text-dark);
    }

    /* Detection Card (Fase 6) */
    .detection-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .detection-card h3 {
        color: white;
        margin: 10px 0;
    }

    .detection-card p {
        color: rgba(255, 255, 255, 0.9);
        margin: 5px 0;
    }

    /* Health Status Cards (Fase 6) */
    .health-good {
        background-color: var(--success-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--success-border);
        margin: 10px 0;
    }

    .health-good h3 {
        color: var(--primary-dark);
        margin: 0;
    }

    .health-good h2 {
        color: var(--primary-dark);
        margin: 10px 0;
    }

    .health-good p {
        color: var(--text-medium);
        margin: 5px 0;
    }

    .health-warning {
        background-color: var(--warning-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--warning-border);
        margin: 10px 0;
    }

    .health-warning h3 {
        color: var(--text-dark);
        margin: 0;
    }

    .health-warning h2 {
        color: #F57C00;
        margin: 10px 0;
    }

    .health-warning p {
        color: var(--text-medium);
        margin: 5px 0;
    }

    .health-critical {
        background-color: var(--error-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--error-border);
        margin: 10px 0;
    }

    .health-critical h3 {
        color: var(--text-dark);
        margin: 0;
    }

    .health-critical h2 {
        color: var(--error-border);
        margin: 10px 0;
    }

    .health-critical p {
        color: var(--text-medium);
        margin: 5px 0;
    }

    /* Detection Item (Fase 6) */
    .detection-item {
        background-color: var(--info-bg);
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        color: var(--text-dark);
        border: 1px solid var(--info-border);
    }

    /* Metric Box (Fase 2) */
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .metric-box h3 {
        color: white;
        margin: 10px 0;
        font-weight: 600;
    }

    .metric-box h2 {
        color: white;
        margin: 5px 0;
        font-size: 2rem;
    }

    /* Warning Box (Fase 2) */
    .warning-box {
        background-color: var(--warning-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--warning-border);
    }

    .warning-box strong {
        color: var(--text-dark);
    }

    /* Success Box (Fase 2) */
    .success-box {
        background-color: var(--success-bg);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid var(--success-border);
    }

    .success-box strong {
        color: var(--text-dark);
    }

    /* Resultado Card (Fase 1) */
    .resultado-card {
        background-color: var(--success-bg);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid var(--success-border);
        margin: 10px 0;
    }

    .resultado-card h3 {
        color: var(--text-dark);
        margin: 0;
    }

    .resultado-card p {
        color: var(--text-medium);
        margin: 10px 0;
    }

    /* Custo Card (Fase 1) */
    .custo-card {
        background-color: var(--warning-bg);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid var(--warning-border);
        margin: 10px 0;
    }

    .custo-card h3 {
        color: var(--text-dark);
        margin: 0;
    }

    .custo-card p {
        color: var(--text-medium);
        margin: 10px 0;
    }

    /* General Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-dark);
    }

    p {
        color: var(--text-medium);
        line-height: 1.6;
    }

    strong {
        color: var(--text-dark);
        font-weight: 600;
    }
</style>
"""

def apply_global_css():
    """Aplica os estilos globais ao Streamlit"""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
