@echo off
REM FarmTech Solutions - Fase 7 Dashboard Integrado
REM Script para executar o dashboard no Windows

cls
echo ==========================================
echo FarmTech Solutions - Fase 7 Dashboard
echo ==========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ^❌ Python nao encontrado. Instale Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

echo ^✅ Python encontrado

REM Verificar se pip está instalado
pip --version >nul 2>&1
if errorlevel 1 (
    echo ^❌ pip nao encontrado. Instale pip e tente novamente.
    pause
    exit /b 1
)

echo ^✅ pip encontrado
echo.

REM Verificar se venv existe, senão criar
if not exist "venv" (
    echo ^📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv
echo ^🔌 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências (apenas se necessário)
echo.
echo ^📚 Verificando dependencias...

python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ^⬇️  Instalando dependencias (isso pode levar alguns minutos^)...
    pip install -r requirements.txt --quiet
    echo ^✅ Dependencias instaladas
) else (
    echo ^✅ Dependencias ja instaladas
)

REM Executar testes (opcional)
echo.
echo ^🧪 Executando testes de validacao...
python test_dashboard.py

echo.
echo ==========================================
echo ^🚀 Iniciando Dashboard FarmTech Solutions
echo ==========================================
echo.
echo ^📍 O dashboard sera aberto em: http://localhost:8501
echo ^🛑 Para parar: Pressione Ctrl+C
echo.

REM Entrar no diretório do dashboard e executar
cd dashboard_integrado
streamlit run app.py

pause
