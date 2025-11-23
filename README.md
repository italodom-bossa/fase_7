# FarmTech Solutions - Fases 1 a 6 | FIAP 🌱

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF.svg)](https://github.com/ultralytics/ultralytics)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg)](https://www.sqlite.org/)

## 🌐 Links Importantes

**[🚀 Dashboard Online - Demonstração](https://fase-7-fiap-farm-tech.streamlit.app/)**

**[🎬 Vídeo Demonstrativo - Fase 6 YOLO](SEU_LINK_AQUI)**

---

## 📋 Sobre o Projeto

Este repositório consolida **todas as 6 fases** do projeto FarmTech Solutions da FIAP, integrando soluções de tecnologia para o agronegócio em um **dashboard interativo único**.

## 👨‍💻 Integrantes do Grupo
- **Italo Domingues** – RM: 561787
- **Maison Wendrel Bezerra Ramos** – RM: 565616

---

## 🎯 Dashboard Integrado

O **Dashboard Integrado** (`dashboard_integrado/`) consolida todas as funcionalidades desenvolvidas nas 6 fases em uma aplicação web Streamlit com **persistência de dados em SQLite**.

### 🚀 Como Executar o Dashboard

```bash
# 1. Clone o repositório
git clone <seu-repositorio>
cd fase_7

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o dashboard
cd dashboard_integrado
streamlit run app.py
```

O dashboard estará disponível em: `http://localhost:8501`

### 📊 Fases Implementadas

| Fase | Nome | Descrição | Banco de Dados |
|------|------|-----------|----------------|
| **Fase 1** | 📐 Cálculos | Cálculos de área de plantio e produtividade | `fase1_calculos.db` |
| **Fase 2** | 🌾 CanaTrack | Gestão de lotes de cana-de-açúcar | `fase2_canatrack.db` |
| **Fase 3** | 🤖 IoT | Monitoramento de sensores IoT em tempo real | `fase3_iot.db` |
| **Fase 4** | 💧 Machine Learning | Predição de irrigação com ML | - |
| **Fase 6** | 🔍 YOLO Vision | Detecção de objetos com visão computacional | `fase6_yolo.db` |

---

## 🔍 Fase 6 - YOLO Vision Computacional (Destaque)

A **Fase 6** implementa detecção de objetos utilizando **YOLOv8** para demonstrar o potencial da visão computacional da FarmTech Solutions.

### 📁 Estrutura da Fase 6

```
fases/fase_6_cap_1/
├── dataset/                    # Dataset original (82 imagens)
│   ├── cat/                   # 41 imagens de gatos
│   └── dog/                   # 41 imagens de cachorros
├── labels/                    # 41 anotações YOLO (corrigidas)
├── yolo_dataset/              # Dataset convertido para YOLO
├── runs/detect/
│   ├── train_30epochs/        # Modelo 1 (30 épocas - labels incorretas)
│   ├── train_60epochs/        # Modelo 2 (60 épocas - labels incorretas)
│   └── train_100epochs_corrigido/  # ⭐ Modelo final (100 épocas - labels corrigidas)
├── ItaloDomingues_RM561787_pbl_fase6.ipynb  # Notebook principal
├── corrigir_labels.py         # Script de correção de labels
├── retreinar_modelo.py        # Script de retreinamento
└── README.md                  # Documentação completa da Fase 6
```

**Documentação Completa**: Veja o [README da Fase 6](fases/fase_6_cap_1/README.md) para mais detalhes técnicos.

---

## 💻 Estrutura do Dashboard Integrado

```
dashboard_integrado/
├── app.py                     # Aplicação principal Streamlit
├── pages/
│   ├── 01_📐_Fase1_Calculos.py
│   ├── 02_🌾_Fase2_CanaTrack.py
│   ├── 03_🤖_Fase3_IoT.py
│   ├── 04_💧_Fase4_ML.py
│   └── 06_🔍_Fase6_YOLO.py   # Página de detecção YOLO
├── servicos/
│   ├── database.py            # Gerenciamento de bancos SQLite
│   ├── fase1_calculos.py
│   ├── fase2_canatrack.py
│   ├── fase3_iot.py
│   ├── fase4_ml.py
│   └── fase6_yolo.py          # Serviço de detecção YOLO
├── data/
│   ├── fase1_calculos.db
│   ├── fase2_canatrack.db
│   ├── fase3_iot.db
│   └── fase6_yolo.db          # Persistência de detecções YOLO
├── simulador_iot.py           # Simulador de sensores IoT
└── requirements.txt
```

---

## 🗄️ Persistência de Dados

Todas as fases que requerem persistência utilizam **SQLite**:

### **Fase 1 - Cálculos** (`fase1_calculos.db`)
- Tabela: `calculos`
- Campos: área, produtividade, produção total, timestamp

### **Fase 2 - CanaTrack** (`fase2_canatrack.db`)
- Tabela: `lotes`
- Campos: ID, área, variedade, data plantio, data colheita, produtividade

### **Fase 3 - IoT** (`fase3_iot.db`)
- Tabelas: `sensores`, `leituras`
- Dados: temperatura, umidade, pH, nutrientes em tempo real

### **Fase 6 - YOLO Vision** (`fase6_yolo.db`)
- Tabela `deteccoes`: timestamp, total objetos, confiança média, modo
- Tabela `objetos_detectados`: classe, confiança, bounding boxes, área

---

## 🚀 Tecnologias Utilizadas

### **Frontend & Dashboard**
- **Streamlit**: Framework web interativo
- **Plotly/Matplotlib**: Visualização de dados
- **PIL/OpenCV**: Processamento de imagens

### **Backend & ML**
- **Python 3.8+**: Linguagem principal
- **YOLOv8 (Ultralytics)**: Detecção de objetos
- **PyTorch**: Deep learning
- **Scikit-learn**: Machine learning clássico
- **SQLite**: Banco de dados

### **Cloud & DevOps**
- **AWS Pricing Calculator**: Estimativa de custos
- **Google Colab**: Treinamento de modelos
- **Git/GitHub**: Versionamento

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

**FarmTech Solutions** - Inovação tecnológica para o agronegócio 🌾🤖

*"Da análise de dados à visão computacional: soluções completas para o campo"*
