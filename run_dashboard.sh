#!/bin/bash

# FarmTech Solutions - Fase 7 Dashboard Integrado
# Script para executar o dashboard com facilidade

set -e

echo "=========================================="
echo "FarmTech Solutions - Fase 7 Dashboard"
echo "=========================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.8+ e tente novamente."
    exit 1
fi

echo "✅ Python encontrado"

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip não encontrado. Instale pip e tente novamente."
    exit 1
fi

echo "✅ pip encontrado"
echo ""

# Verificar se venv existe, senão criar
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate || . venv/Scripts/activate

# Instalar dependências (apenas se necessário)
echo ""
echo "📚 Verificando dependências..."

# Tenta importar streamlit, se falhar instala dependências
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⬇️  Instalando dependências (isso pode levar alguns minutos)..."
    pip install -r requirements.txt --quiet
    echo "✅ Dependências instaladas"
else
    echo "✅ Dependências já instaladas"
fi

# Executar testes (opcional)
echo ""
echo "🧪 Executando testes de validação..."
python3 test_dashboard.py

echo ""
echo "=========================================="
echo "🚀 Iniciando Dashboard FarmTech Solutions"
echo "=========================================="
echo ""
echo "📍 O dashboard será aberto em: http://localhost:8501"
echo "🛑 Para parar: Pressione Ctrl+C"
echo ""

# Entrar no diretório do dashboard e executar
cd dashboard_integrado
streamlit run app.py
