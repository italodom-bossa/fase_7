"""
Configurações Globais do Dashboard Integrado
FarmTech Solutions - Fase 7
"""

import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent

# Diretórios das fases
FASE_1_DIR = BASE_DIR / "fases" / "fase_1"
FASE_2_DIR = BASE_DIR / "fases" / "fase_2"
FASE_3_DIR = BASE_DIR / "fases" / "fase_3"
FASE_4_DIR = BASE_DIR / "fases" / "fase_4" / "farm_tech"
FASE_5_DIR = BASE_DIR / "fases" / "fase5_farmtech_cap1"
FASE_6_DIR = BASE_DIR / "fases" / "fase_6_cap_1"

# Configurações de Banco de Dados
DB_POSTGRES = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
    'database': os.getenv('POSTGRES_DB', 'db_agricultura'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres')
}

DB_ORACLE = {
    'host': os.getenv('ORACLE_HOST', 'localhost'),
    'port': int(os.getenv('ORACLE_PORT', 1521)),
    'service_name': os.getenv('ORACLE_SERVICE', 'XEPDB1'),
    'user': os.getenv('ORACLE_USER', 'system'),
    'password': os.getenv('ORACLE_PASSWORD', 'oracle')
}

# Configurações AWS
AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'sa-east-1')
AWS_SNS_TOPIC_ARN = os.getenv('AWS_SNS_TOPIC_ARN', '')

# Configurações de Insumos (Fase 1)
INSUMOS_POR_CULTURA = {
    "Café": {
        "Nitrogênio (kg/ha)": 100,
        "Fósforo (kg/ha)": 50,
        "Potássio (kg/ha)": 60,
        "Micronutrientes (Boro, Zinco) (kg/ha)": 5,
        "Calcário (t/ha)": 3,
        "Gesso Agrícola (t/ha)": 1.5,
        "Inseticidas (mL/ha)": 1500,
        "Fungicidas (mL/ha)": 2000,
        "Herbicidas (L/ha)": 2
    },
    "Soja": {
        "Fósforo (kg/ha)": 40,
        "Potássio (kg/ha)": 50,
        "Micronutrientes e Enxofre (S) (kg/ha)": 10,
        "Bradyrhizobium (com Mo e Co) (mL/ha)": 500,
        "Calcário (t/ha)": 2.5,
        "Gesso Agrícola (t/ha)": 1,
        "Fungicidas (mL/ha)": 2500,
        "Inseticidas (mL/ha)": 1800,
        "Aplicações Foliares de Micronutrientes (mL/ha)": 300
    }
}

# Configurações de Sensores (Fase 3)
LIMITES_SENSORES = {
    'umidade_min': 40.0,
    'umidade_max': 90.0,
    'ph_min': 5.5,
    'ph_max': 7.5,
    'temperatura_min': 15.0,
    'temperatura_max': 35.0
}

# Culturas disponíveis (Fase 3 ML)
CULTURAS_ML = [
    "apple", "banana", "blackgram", "chickpea", "coconut", "coffee",
    "cotton", "grapes", "jute", "kidneybeans", "lentil", "maize",
    "mango", "mothbeans", "mungbean", "muskmelon", "orange", "papaya",
    "pigeonpeas", "pomegranate", "rice", "watermelon"
]

# Configurações YOLO (Fase 6)
YOLO_CLASSES = ["cat", "dog"]
YOLO_CONFIDENCE_THRESHOLD = 0.5

# Informações da Equipe
TEAM_INFO = {
    "nome_grupo": "FarmTech Solutions",
    "integrantes": [
        {"nome": "Italo Domingues", "rm": "561787"},
        {"nome": "Maison Wendrel Bezerra Ramos", "rm": "565616"},
        {"nome": "Felipe Cristovao da Silva", "rm": "564288"},
        {"nome": "Jocasta de Kacia Bortolacci", "rm": "564730"}
    ],
    "tutor": "Lucas Gomes Moreira",
    "coordenador": "André Godoi Chiovato"
}

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    "page_title": "FarmTech Solutions - Dashboard Integrado",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Mensagens de alerta padrão
ALERT_MESSAGES = {
    "umidade_baixa": {
        "titulo": "🚨 ALERTA: Irrigação Necessária",
        "severidade": "crítico"
    },
    "ph_anormal": {
        "titulo": "⚠️ ALERTA: pH do Solo Anormal",
        "severidade": "alto"
    },
    "irrigacao_ml": {
        "titulo": "💧 ALERTA PREDITIVO: Irrigação Recomendada",
        "severidade": "médio"
    },
    "yolo_deteccao": {
        "titulo": "👁️ ALERTA VISUAL: Anomalia Detectada",
        "severidade": "médio"
    }
}

# Cores do tema
COLORS = {
    "primary": "#2E7D32",
    "secondary": "#4CAF50",
    "success": "#66BB6A",
    "warning": "#FFA726",
    "danger": "#EF5350",
    "info": "#29B6F6",
    "light": "#F5F5F5",
    "dark": "#212121"
}
