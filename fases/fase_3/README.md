# FIAP - Faculdade de Informática e Administração Paulista

## 📌 Nome do projeto
**FarmTech Solutions — Sistema IoT de Irrigação Inteligente e Análise Preditiva de Culturas**

## Nome do Grupo

FarmTech Solutions

## 👨‍🎓 Integrantes:
- Italo Domingues – RM: 561787
- Maison Wendrel Bezerra Ramos – RM: 565616
- Jocasta de Kacia Bortolacci – RM: 564730

## 👩‍🏫 Professores:

**Tutor(a):**
Lucas Gomes Moreira

**Coordenador(a):**
André Godoi Chiovato

---

## 📜 Descrição

A Fase 3 do projeto FarmTech Solutions implementa a **camada IoT e Automação Inteligente**, combinando hardware físico com análise de dados através de Machine Learning. Esta fase é dividida em duas grandes entregas:

### 🔌 Capítulo 1 - Sistema IoT com ESP32

Sistema de irrigação inteligente baseado em **ESP32** que monitora condições ambientais e aciona automaticamente a irrigação quando necessário.

#### Funcionalidades de Hardware:

1. **Monitoramento de Nutrientes**
   - Detecção de Fósforo (P)
   - Detecção de Potássio (K)
   - Interface via botões físicos

2. **Análise de pH do Solo**
   - Simulação usando sensor LDR
   - Faixa ideal: 5.5 a 7.5
   - Conversão de luminosidade para valor de pH

3. **Medição de Umidade**
   - Sensor DHT22 para umidade relativa do ar
   - Monitoramento contínuo
   - Threshold crítico: 40%

4. **Acionamento Automático**
   - LED representando bomba de irrigação
   - Ativação quando:
     - ✅ Nutriente detectado (P ou K)
     - ✅ pH entre 5.5 e 7.5
     - ✅ Umidade < 40%

#### Sistema de Banco de Dados:

**Modelo Entidade-Relacionamento (MER)**
- Tabela **Plantações**: áreas de cultivo
- Tabela **Sensores**: dispositivos IoT associados
- Tabela **Dados_Sensores**: leituras históricas

**Operações CRUD Completas:**
1. **Plantações**: cadastrar, listar, buscar, editar, deletar
2. **Sensores**: registrar, consultar, atualizar, remover
3. **Leituras**: armazenar dados, consultar histórico, analisar tendências

### 🤖 Capítulo 14 - Machine Learning para Recomendação de Culturas

Análise exploratória e modelos preditivos para classificação de culturas agrícolas baseados em condições de solo e clima.

#### Base de Dados:
- **2200 amostras** de culturas agrícolas
- **22 tipos de culturas** diferentes
- **7 variáveis preditoras**:
  - Nitrogênio (N)
  - Fósforo (P)
  - Potássio (K)
  - Temperatura média (°C)
  - Umidade relativa (%)
  - pH do solo
  - Precipitação (mm)

#### Análise Exploratória:

1. **Distribuição de Temperatura**
   - Maioria entre 20°C e 30°C
   - Pico em 25°C
   - Culturas adaptadas a clima moderado

2. **Umidade do Ar**
   - 50% das amostras entre 60% e 90%
   - Mediana em 80%
   - Regiões predominantemente úmidas

3. **Culturas Balanceadas**
   - Dataset com 100 amostras por cultura
   - Equilíbrio para treinamento de ML
   - 22 culturas: rice, coffee, cotton, etc.

4. **Correlação de Nutrientes**
   - Fósforo e Potássio: correlação 0.74 (forte)
   - Nitrogênio: variação independente

5. **Precipitação por Cultura**
   - Rice, papaya, coconut: alta pluviosidade
   - Muskmelon, mungbean: baixa precipitação

#### Perfis de Cultura Analisados:

**Arroz (Rice):**
- Alto nitrogênio (79.89 kg/ha)
- Alta umidade (82.27%)
- Alta precipitação (236.18 mm)
- Temperatura amena (23.69°C)

**Feijão-Guandu (Pigeonpeas):**
- Baixo nitrogênio (20.73 kg/ha)
- Alto fósforo (67.73 kg/ha)
- Tolera temperaturas altas (27.74°C)
- Umidade baixa (48.06%)

**Feijão-Mungo (Mothbeans):**
- Nutrientes baixos
- Temperatura alta (28.19°C)
- Muito seco (53.16% umidade)
- Baixa precipitação (51.20 mm)

#### Modelos de Machine Learning Desenvolvidos:

**1. Árvore de Decisão**
- Acurácia: **99%**
- Excelente memorização dos padrões
- Leve tendência a overfitting

**2. Regressão Logística**
- Acurácia: **96%**
- Boa generalização
- Algumas dificuldades com classes similares

**3. Random Forest (Melhor Modelo)**
- Acurácia: **99%**
- F1-score quase perfeito
- Mais robusto e menos propenso a overfitting
- **Recomendado para produção**

**4. K-Nearest Neighbors (KNN)**
- Acurácia: **97%**
- Bom desempenho geral
- Sensível à escala (beneficiaria de normalização)

**5. Support Vector Machine (SVM)**
- Acurácia: **96%**
- Excelente em várias classes
- Também sensível à escala

---

## 🔧 Como executar o projeto

### ✅ Pré-requisitos

#### Para o Sistema IoT (Capítulo 1):
- **Hardware:**
  - ESP32 DevKit
  - Sensor DHT22
  - Módulo LDR
  - 2 Botões (push buttons)
  - LED e resistor
  - Jumpers e protoboard
- **Software:**
  - IDE Arduino instalada
  - Biblioteca `DHT.h` instalada

#### Para o Banco de Dados:
- Python 3.8 ou superior
- PostgreSQL
- Docker e Docker Compose (opcional)

#### Para Machine Learning (Capítulo 14):
- Python 3.8+
- Bibliotecas:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `scikit-learn`
- Jupyter Notebook ou Google Colab

---

### 🚀 Passo a passo

#### Para o Sistema IoT (Capítulo 1):

**1. Montagem do Circuito:**
```bash
# Siga o diagrama em: cap_1/entrega_1/circuito.png
```

**2. Upload do Código ESP32:**
```bash
# Abra o Arduino IDE
# Carregue: cap_1/entrega_1/farmtech_solutions.ino
# Configure a porta serial para 115200 bps
# Faça o upload para o ESP32
```

**3. Configuração do Banco de Dados:**
```bash
# Usando Docker (recomendado)
cd cap_1/entrega_2
docker-compose up -d

# Criar tabelas
psql -h localhost -U postgres -d postgres -f sql.sql

# Carregar dados de exemplo (opcional)
psql -h localhost -U postgres -d postgres -f seeds.sql
```

**4. Executar Sistema CRUD:**
```bash
cd cap_1/entrega_2
python main.py
```

#### Para Machine Learning (Capítulo 14):

**1. Abrir Notebook:**
```bash
# Navegar até o diretório
cd cap_14

# Opção 1: Jupyter Notebook Local
jupyter notebook ItaloDomingues_RM561787_fase3_cap14.ipynb

# Opção 2: Google Colab
# Faça upload do arquivo .ipynb para o Colab
```

**2. Executar Análise:**
- Execute todas as células sequencialmente
- O notebook já contém:
  - Carregamento do dataset
  - Análise exploratória completa
  - Treinamento dos 5 modelos
  - Comparação de performance

**3. Dados Necessários:**
- Arquivo: `Atividade_Cap_14_produtos_agricolas.csv`
- Localização: `cap_14/` (já incluído)

---

## 📂 Estrutura do Projeto

```
fase_3/
├── cap_1/                                      # Sistema IoT e Banco de Dados
│   ├── entrega_1/
│   │   ├── farmtech_solutions.ino              # Código Arduino ESP32
│   │   ├── circuito.png                        # Diagrama do circuito
│   │   └── log_esp32.txt                       # Log de exemplo
│   ├── entrega_2/
│   │   ├── main.py                             # Sistema CRUD principal
│   │   ├── sql.sql                             # Schema do banco
│   │   ├── seeds.sql                           # Dados de exemplo
│   │   ├── docker-compose.yml                  # Config PostgreSQL
│   │   ├── mer.png                             # Modelo ER
│   │   ├── models/                             # Classes de modelo
│   │   ├── services/                           # Lógica de negócio
│   │   ├── db/                                 # Adaptadores de BD
│   │   └── ui/                                 # Interfaces de menu
│   └── README.md                               # Doc do cap_1
├── cap_14/                                     # Machine Learning
│   ├── ItaloDomingues_RM561787_fase3_cap14.ipynb # Notebook principal
│   └── Atividade_Cap_14_produtos_agricolas.csv    # Dataset
└── README.md                                   # Este arquivo
```

---

## 📊 Resultados e Métricas

### Performance dos Modelos ML (Cap 14):

| Modelo                  | Acurácia | Precisão Média | Recall Médio | F1-Score Médio |
|------------------------|----------|----------------|--------------|----------------|
| Árvore de Decisão      | 99%      | 0.99           | 0.99         | 0.99           |
| **Random Forest**      | **99%**  | **0.99**       | **0.99**     | **0.99**       |
| K-Nearest Neighbors    | 97%      | 0.97           | 0.97         | 0.97           |
| Regressão Logística    | 96%      | 0.96           | 0.97         | 0.96           |
| SVM                    | 96%      | 0.96           | 0.96         | 0.96           |

### Sistema IoT (Cap 1):

- **Taxa de Leitura:** 1 leitura a cada 2 segundos
- **Precisão pH:** ±0.1
- **Precisão Umidade:** ±2%
- **Tempo de Resposta:** < 500ms
- **Operações CRUD:** < 100ms (banco local)

---

## 🎯 Objetivos da Fase 3

- ✅ Implementar sistema IoT completo com ESP32
- ✅ Integrar sensores físicos (DHT22, LDR, botões)
- ✅ Criar lógica de acionamento automático de irrigação
- ✅ Estruturar banco de dados relacional (PostgreSQL)
- ✅ Desenvolver operações CRUD completas
- ✅ Realizar análise exploratória de dados agrícolas
- ✅ Treinar e comparar 5 modelos de Machine Learning
- ✅ Identificar melhor modelo para classificação de culturas
- ✅ Documentar todo o processo e resultados

---

## 🔗 Integração com Outras Fases

Esta fase fornece:
- **Para Fase 4:** Dados de sensores em tempo real para dashboard
- **Para Fase 5:** Métricas para monitoramento em nuvem
- **Para Fase 6:** Contexto ambiental para análise de imagens
- **Para Fase 7:** Serviços de IoT e ML no sistema integrado

---

## 📈 Principais Conclusões

### Sistema IoT:
- Automação eficaz de irrigação baseada em múltiplos sensores
- Banco de dados estruturado permite rastreabilidade completa
- Sistema escalável para múltiplas plantações e sensores

### Machine Learning:
- **Random Forest** demonstrou melhor performance geral
- Dataset balanceado facilita aprendizado equitativo
- Modelos conseguem distinguir 22 culturas com alta precisão
- Normalização pode melhorar performance de KNN e SVM
- Sistema pronto para implementação em produção

---

## 🗃 Histórico de lançamentos

| Versão | Data       | Descrição                                                        |
|--------|------------|------------------------------------------------------------------|
| 1.0    | 20/05/2025 | Sistema IoT com ESP32 e banco de dados PostgreSQL               |
| 1.1    | 20/05/2025 | Análise de dados e modelos de ML para classificação de culturas |

---

## 📋 Licença

MODELO GIT FIAP por FIAP está licenciado sob a licença [Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
