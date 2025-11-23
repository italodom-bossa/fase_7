import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Carrega o modelo
modelo = joblib.load("modelo_irrigacao.pkl")

# Carrega os dados simulados
df = pd.read_csv("dataset_balanceado.csv")

# Título da página
st.title("🌾 FarmTech - Painel de Irrigação Inteligente")

# Mostra dados mais recentes
st.subheader("📊 Leituras recentes dos sensores")
st.dataframe(df.tail(10))

# Gráficos
st.subheader("📈 Gráficos de sensores")
col1, col2 = st.columns(2)

with col1:
    st.line_chart(df["umidade"], height=200)
with col2:
    st.line_chart(df["ph"], height=200)

# Entrada manual de dados para simular nova leitura
st.subheader("🧠 Prever necessidade de irrigação")
fosforo = st.number_input("Fósforo", min_value=0.0, max_value=1.5, value=1.0)
potassio = st.number_input("Potássio", min_value=0.0, max_value=1.5, value=1.0)
ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=6.5)
umidade = st.number_input("Umidade (%)", min_value=0.0, max_value=100.0, value=35.0)

# Botão para prever
if st.button("🔍 Verificar necessidade de irrigação"):
    entrada = pd.DataFrame([[fosforo, potassio, ph, umidade]], columns=["fosforo", "potassio", "ph", "umidade"])
    pred = modelo.predict(entrada)[0]
    resultado = "💧 IRRIGAÇÃO NECESSÁRIA" if pred == 1 else "✅ Não irrigar"
    st.success(resultado)