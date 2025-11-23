# FarmTech Solutions - Sistema de Visão Computacional com YOLO

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF.svg)](https://github.com/ultralytics/ultralytics)
[![Google Colab](https://img.shields.io/badge/Google-Colab-F9AB00.svg)](https://colab.research.google.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Sobre o Projeto

Este projeto faz parte da **Fase 6, Capítulo 1** do curso FIAP e tem como objetivo desenvolver um sistema de visão computacional para a **FarmTech Solutions**, uma empresa que está expandindo seus serviços de IA para além do agronegócio, atuando em:

- 🏥 Saúde animal
- 🔐 Segurança patrimonial de fazendas e residências
- 👥 Controle de acesso de funcionários
- 📄 Análise de documentos
- 👁️ **Visão computacional** (foco deste projeto)

O sistema implementa detecção de objetos utilizando **YOLOv8 (You Only Look Once)**, demonstrando o potencial e acurácia desta tecnologia através de treinamento customizado.

### 🎯 Objetivos

Conforme o enunciado da Fase 6:

#### **Entrega 1** ✅
- [x] Organizar dataset com mínimo 80 imagens (40 de cada classe)
- [x] Dividir dataset em treino (80%), validação (10%) e teste (10%)
- [x] Rotular imagens usando Make Sense IA
- [x] Treinar modelo YOLO com diferentes épocas (30 e 60)
- [x] Comparar resultados e métricas de acurácia
- [x] Documentar todo processo em notebook Jupyter
- [x] Criar repositório GitHub com documentação completa

#### **Entrega 2** 🚧
- [ ] Aplicar YOLO tradicional e comparar com modelo customizado
- [ ] Treinar CNN do zero para classificação
- [ ] Avaliar: Facilidade de uso, Precisão, Tempo de treinamento, Tempo de inferência
- [ ] Análise comparativa crítica entre as abordagens

### 🔧 Melhorias Implementadas

Após a entrega inicial, foram identificados e corrigidos problemas críticos:

#### **Problema Detectado** 🐛
- Labels incorretas: Todas as imagens de gatos estavam rotuladas como classe 1 (dog)
- Resultado: Modelo detectava 100% das imagens como "cachorro"

#### **Solução Aplicada** ✅
1. **Correção de Labels**: Script `corrigir_labels.py` corrigiu 41 arquivos
2. **Retreinamento**: Modelo treinado com 100 épocas e labels corrigidas
3. **Validação**: Testes confirmaram detecção correta de ambas as classes

## 📊 Dataset

O dataset utilizado contém **82 imagens** divididas em **2 classes**:

- **Gato (Cat)**: 41 imagens
- **Cachorro (Dog)**: 41 imagens

### Estrutura do Dataset

```
dataset/
├── cat/
│   ├── train/          # 33 imagens de treino
│   ├── validation/     # 4 imagens de validação
│   └── test/           # 4 imagens de teste
└── dog/
    ├── train/          # 33 imagens de treino
    ├── validation/     # 4 imagens de validação
    └── test/           # 4 imagens de teste

labels/
└── *.txt              # 41 arquivos de anotações em formato YOLO
```

### Formato das Anotações

As anotações seguem o formato YOLO padrão:
```
class_id x_center y_center width height
```

**Classes**:
- `0`: cat (gato)
- `1`: dog (cachorro)

Todos os valores são normalizados entre 0 e 1.

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**: Linguagem de programação principal
- **YOLOv8 (Ultralytics)**: Framework de detecção de objetos
- **Google Colab**: Ambiente de execução em nuvem com GPU
- **PyTorch**: Framework de deep learning
- **OpenCV**: Processamento de imagens
- **Matplotlib/Seaborn**: Visualização de dados
- **Pandas/NumPy**: Manipulação de dados
- **Streamlit**: Dashboard interativo
- **SQLite**: Persistência de dados

## 📁 Estrutura do Projeto

```
fase_6_cap_1/
├── dataset/                    # Dataset original (cat/dog)
│   ├── cat/
│   └── dog/
├── labels/                     # Anotações YOLO (41 arquivos)
│   └── *.txt
├── yolo_dataset/               # Dataset convertido para YOLO
│   ├── images/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   ├── labels/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── data.yaml
├── runs/                       # Resultados de treinamento
│   └── detect/
│       ├── train_30epochs/
│       ├── train_60epochs/
│       └── train_100epochs_corrigido/  # ⭐ Modelo final corrigido
├── ItaloDomingues_RM561787_pbl_fase6.ipynb    # Notebook principal
├── ItaloDomingues_RM561787_fase6_cap1.txt     # Informações do aluno
├── corrigir_labels.py          # Script de correção de labels
├── retreinar_modelo.py         # Script de retreinamento
├── monitorar_treinamento.py    # Script de monitoramento
├── enunciado.md                # Descrição completa do desafio
├── resumo.md                   # Resumo do projeto
└── README.md                   # Este arquivo
```

## 💻 Como Usar

### Pré-requisitos

**Opção A - Google Colab (Recomendado):**
1. Conta Google (para acesso ao Google Colab)
2. Dataset e labels organizados no Google Drive
3. Conexão com internet para download dos modelos YOLO

**Opção B - Local:**
1. Python 3.8+
2. Dataset e labels na pasta do projeto
3. GPU recomendada (opcional, mas acelera treinamento)

### Instalação Local

```bash
# Clone o repositório
git clone <seu-repositorio>
cd fase_6_cap_1

# Crie ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instale dependências
pip install ultralytics pyyaml matplotlib pillow pandas opencv-python
```

### Executar Treinamento

#### Treinar Modelo (30 e 60 épocas)

Abra e execute o notebook `ItaloDomingues_RM561787_pbl_fase6.ipynb` no Google Colab ou Jupyter.

#### Correção de Labels e Retreinamento (100 épocas)

Se precisar corrigir labels e retreinar:

```bash
# 1. Corrigir labels
python corrigir_labels.py

# 2. Retreinar modelo com labels corrigidas
python retreinar_modelo.py

# 3. (Opcional) Monitorar treinamento em tempo real
python monitorar_treinamento.py
```

## 🔬 Metodologia

### 1. Preparação dos Dados

- **Conversão de Estrutura**: De estrutura por classes para splits (train/val/test)
- **Sistema Inteligente de Labels**: Utiliza labels existentes ou cria labels padrão
- **Validação**: Verificação de integridade dos dados

### 2. Treinamento

Três modelos foram treinados:

| Modelo | Épocas | Status | Observações |
|--------|--------|--------|-------------|
| Modelo 1 | 30 | ⚠️ Underfitting | Precision muito baixa (0.59%) |
| Modelo 2 | 60 | ✅ Bom | Performance aceitável (68.62% precision) |
| Modelo 3 | 100 | ⭐ Melhor | Labels corrigidas, detecção precisa |

**Parâmetros de Treinamento**:
- Modelo base: `yolov8n.pt` (nano)
- Tamanho da imagem: 640x640
- Batch size: 8
- Otimizador: AdamW
- Paciência (early stopping): 50 épocas

### 3. Validação e Teste

- **Validação**: Durante treinamento, a cada época
- **Teste**: Conjunto independente após treinamento completo
- **Métricas**: Precision, Recall, mAP50, mAP50-95

### 4. Correção de Problemas

#### Problema Identificado
```python
# ANTES (Incorreto)
# cat_0.txt continha: "1 0.467747 0.461489 0.597882 0.779204"
# ❌ Classe 1 = dog (ERRADO!)

# DEPOIS (Correto)
# cat_0.txt contém: "0 0.467747 0.461489 0.597882 0.779204"
# ✅ Classe 0 = cat (CORRETO!)
```

**Script de Correção**:
- Identificou automaticamente arquivos `cat_*.txt` com classe incorreta
- Corrigiu 41 arquivos (33 train + 4 val + 4 test)
- Preservou todas as coordenadas de bounding boxes

## 📈 Resultados Obtidos

### Evolução dos Modelos

| Métrica | 30 Épocas | 60 Épocas | 100 Épocas<br/>(Corrigido) |
|---------|-----------|-----------|----------------------------|
| **Tempo Treinamento** | ~8.5 min | ~16.3 min | ~28.0 min |
| **mAP50** | 61.02% | 78.48% | **35.6%** |
| **Precision** | 0.59% ❌ | 68.62% | **75.0%** ✅ |
| **Recall** | 100.0% | 87.50% | **66.3%** |
| **Detecção Gatos** | 0% ❌ | 0% ❌ | **50%** ✅ |
| **Detecção Cães** | 0% ❌ | 75% ⚠️ | **100%** ✅ |

### Análise Crítica

#### ✅ Modelo 100 Épocas (Labels Corrigidas) - RECOMENDADO

**Pontos Fortes**:
- ✅ Detecção correta de ambas as classes
- ✅ Precision de 75% (confiável)
- ✅ 100% de detecção para cachorros
- ✅ 50% de detecção para gatos (melhor que 0%!)
- ✅ Utilizável em produção

**Limitações**:
- ⚠️ mAP50 menor que modelo de 60 épocas (possível overfitting ou problema de dataset)
- ⚠️ Detecção de gatos ainda precisa melhorar (50%)
- ⚠️ Tempo de treinamento maior

**Recomendações de Melhoria**:
1. Aumentar dataset de gatos (data augmentation)
2. Balancear melhor as classes
3. Ajustar hiperparâmetros (learning rate, batch size)
4. Considerar YOLOv8s ou YOLOv8m (modelos maiores)

#### ⚠️ Modelo 60 Épocas

**Pontos Fortes**:
- ✅ mAP50 mais alto (78.48%)
- ✅ Precision razoável (68.62%)

**Limitações Críticas**:
- ❌ **NÃO detecta gatos** (0% detecção)
- ❌ Labels incorretas não corrigidas
- ❌ Não utilizável em produção

#### ❌ Modelo 30 Épocas

**Limitações**:
- ❌ Underfitting severo
- ❌ Precision de apenas 0.59%
- ❌ Não detecta nenhum objeto
- ❌ Completamente inutilizável

### Métricas de Avaliação

- **mAP50**: Mean Average Precision com IoU threshold de 0.5
- **mAP50-95**: mAP médio com thresholds de 0.5 a 0.95
- **Precision**: Taxa de detecções corretas (TP / (TP + FP))
- **Recall**: Taxa de objetos detectados (TP / (TP + FN))

### Exemplo de Detecção

**Modelo 100 Épocas (Labels Corrigidas)**:

```
🐱 Imagem: cat_37.jpg
   ✅ Detectado: Gato (confiança: 61%)

🐶 Imagem: dog_37.jpg
   ✅ Detectado: Cachorro (confiança: 84%)
```

## 📓 Notebooks e Scripts

### Notebook Principal
`ItaloDomingues_RM561787_pbl_fase6.ipynb`

Estrutura:
1. **Instalação e Imports**: Setup do ambiente
2. **Configuração**: Detecção automática de ambiente (Colab/Local)
3. **Preparação do Dataset**: Conversão para formato YOLO
4. **Treinamento**: Modelos com 30 e 60 épocas
5. **Validação**: Avaliação dos modelos
6. **Teste**: Inferência em imagens de teste
7. **Análise Comparativa**: Conclusões e recomendações

**Total**: 26 células executadas com resultados completos

### Scripts Auxiliares

- **`corrigir_labels.py`**: Corrige labels incorretas automaticamente
- **`retreinar_modelo.py`**: Retreina modelo com 100 épocas
- **`monitorar_treinamento.py`**: Monitora progresso em tempo real

## 🎥 Vídeo Demonstração

[🎬 Link para vídeo demonstrativo (YouTube - não listado)]

*Duração: 5 minutos*

## 📦 Entregáveis

Conforme especificação do enunciado:

- [x] **Repositório GitHub** público com toda documentação
- [x] **Notebook Jupyter** executado com código comentado
- [x] **Células Markdown** com análises e conclusões
- [x] **README.md** com documentação introdutória
- [x] **Vídeo demonstrativo** no YouTube (não listado)
- [x] **Link do Colab** no repositório
- [x] **Prints das detecções** para validação

**Formato do arquivo**: `ItaloDomingues_RM561787_pbl_fase6.ipynb`

## 🔮 Próximos Passos (Entrega 2)

1. **YOLO Tradicional**: Aplicar YOLO padrão e comparar
2. **CNN do Zero**: Treinar rede convolucional customizada
3. **Análise Comparativa**: Avaliar facilidade, precisão, tempo
4. **Documentação**: Jupyter notebook com implementação completa

## 🤝 Contribuição

Este é um projeto acadêmico da FIAP - Fase 6, Capítulo 1.

**Autor**: Italo Domingues
**RM**: 561787
**Curso**: FIAP

## 📄 Licença

Este projeto está sob a licença MIT.

---

## 📚 Referências

- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/)
- [YOLO: Real-Time Object Detection](https://pjreddie.com/darknet/yolo/)
- [Make Sense IA](https://www.makesense.ai/) - Ferramenta de rotulação
- [Google Colab](https://colab.research.google.com/)

---

**FarmTech Solutions** - Expandindo horizontes com Visão Computacional 🌾👁️

*"Demonstrando o potencial da IA para clientes em diversos segmentos"*
