# FIAP - Faculdade de Informática e Administração Paulista

## 📌 Nome do projeto
**FarmTech Solutions — Sistema de Cálculo de Área e Gerenciamento de Insumos Agrícolas**

## Nome do Grupo

FarmTech Solutions

## 👨‍🎓 Integrantes:
- Italo Domingues – RM: 561787
- Maison Wendrel Bezerra Ramos – RM: 565616
- Felipe Cristovao da Silva – RM: 564288
- Jocasta de Kacia Bortolacci – RM: 564730

## 👩‍🏫 Professores:

**Tutor(a):**
Lucas Gomes Moreira

**Coordenador(a):**
André Godoi Chiovato

---

## 📜 Descrição

A Fase 1 do projeto FarmTech Solutions estabelece a **base de dados inicial** para o ecossistema digital de gestão agrícola. O sistema permite:

### Funcionalidades Principais:

1. **Cálculo de Área de Plantio**
   - Cálculo de área circular (para culturas como Café)
   - Cálculo de área retangular (para culturas como Soja)
   - Conversão automática de m² para hectares

2. **Gerenciamento de Insumos Agrícolas**
   - Cálculo automático de insumos necessários por cultura
   - Banco de dados com informações detalhadas de:
     - Nitrogênio, Fósforo, Potássio
     - Micronutrientes (Boro, Zinco, Enxofre)
     - Calcário e Gesso Agrícola
     - Inseticidas, Fungicidas e Herbicidas

3. **Operações CRUD**
   - Adicionar novas culturas com cálculo de área e insumos
   - Listar todas as culturas cadastradas
   - Atualizar informações de culturas existentes
   - Deletar culturas do banco de dados

4. **Análise Estatística com R**
   - Importação de dados do banco JSON
   - Cálculo de média e desvio-padrão por cultura
   - Exportação de estatísticas em formato CSV

### Culturas Suportadas:

**Café (Área Circular)**
- Nitrogênio: 100 kg/ha
- Fósforo: 50 kg/ha
- Potássio: 60 kg/ha
- Micronutrientes (Boro, Zinco): 5 kg/ha
- Calcário: 3 t/ha
- Gesso Agrícola: 1.5 t/ha
- Inseticidas: 1500 mL/ha
- Fungicidas: 2000 mL/ha
- Herbicidas: 2 L/ha

**Soja (Área Retangular)**
- Fósforo: 40 kg/ha
- Potássio: 50 kg/ha
- Micronutrientes e Enxofre (S): 10 kg/ha
- Bradyrhizobium (com Mo e Co): 500 mL/ha
- Calcário: 2.5 t/ha
- Gesso Agrícola: 1 t/ha
- Fungicidas: 2500 mL/ha
- Inseticidas: 1800 mL/ha
- Aplicações Foliares de Micronutrientes: 300 mL/ha

---

## 🔧 Como executar o código

### ✅ Pré-requisitos

#### Para o sistema Python:
- Python 3.8 ou superior
- Bibliotecas padrão do Python (json, os)

#### Para análise estatística em R:
- R 4.0 ou superior
- Bibliotecas:
  - `jsonlite` (manipulação de JSON)
  - `dplyr` (manipulação de dados)

---

### 🚀 Passo a passo

#### 1. Executar o Sistema Python

```bash
# Navegar até o diretório do projeto
cd "fases/fase_1/Cap 1 - play na sua carreira em IA/codigo_python_e_R"

# Executar o programa principal
python main.py
```

#### Menu do Sistema:
```
========== FarmTech Solutions - Agricultura Digital ==========
1. Adicionar Cultura
2. Listar Culturas e Insumos
3. Atualizar Cultura
4. Remover Cultura
5. Sair
```

#### 2. Executar Análise Estatística em R

```bash
# Navegar até o diretório de dados estatísticos
cd "fases/fase_1/Cap 1 - play na sua carreira em IA/codigo_python_e_R/dados_estatisticos_em_r"

# Executar o script R
Rscript main.R
```

**Saída esperada:**
- Exibição de média e desvio-padrão por cultura
- Geração do arquivo `estatisticas_insumos_por_cultura.csv`

---

## 📂 Estrutura do Projeto

```
fase_1/
├── Cap 1 - play na sua carreira em IA/
│   └── codigo_python_e_R/
│       ├── main.py                          # Programa principal
│       ├── config.py                        # Configurações e dados de insumos
│       ├── funcoes/
│       │   ├── adicionar_plantio.py         # Adiciona nova cultura
│       │   ├── atualizar_cultura.py         # Atualiza cultura existente
│       │   ├── deletar_cultura.py           # Remove cultura
│       │   ├── listar_culturas.py           # Lista todas as culturas
│       │   ├── calculos/
│       │   │   ├── calcular_area_circulo.py # Cálculo área circular
│       │   │   ├── calcular_area_retangulo.py # Cálculo área retangular
│       │   │   ├── calcular_insumos.py      # Cálculo de insumos
│       │   │   ├── converte_para_hectares.py # Conversão m² → ha
│       │   │   └── formatar_numero.py       # Formatação números BR
│       │   └── database/
│       │       ├── database.py              # Estrutura do banco de dados
│       │       ├── ler_database.py          # Leitura do JSON
│       │       └── salvar_database.py       # Gravação no JSON
│       └── dados_estatisticos_em_r/
│           ├── main.R                       # Script de análise estatística
│           └── estatisticas_insumos_por_cultura.csv # Resultados
└── README.md                                # Este arquivo
```

---

## 💾 Persistência de Dados

O sistema utiliza um arquivo JSON para armazenar os dados:
- **Localização:** `funcoes/database/database.json`
- **Formato:**
```json
[
  {
    "cultura": "Café",
    "area": 31415.93,
    "insumos": {
      "Nitrogênio (kg/ha)": 314.16,
      "Fósforo (kg/ha)": 157.08,
      "Potássio (kg/ha)": 188.50,
      ...
    }
  }
]
```

---

## 📊 Análise Estatística com R

O script R realiza:
1. Importação dos dados do arquivo JSON
2. Transformação dos dados em DataFrame
3. Cálculo de estatísticas por cultura:
   - Média da área plantada
   - Desvio-padrão da área
4. Exportação dos resultados em CSV

**Exemplo de saída:**
```
Cultura | Media      | DesvioPadrao
--------|------------|-------------
Café    | 28500.50   | 5230.45
Soja    | 45000.75   | 8120.30
```

---

## 🎯 Objetivos da Fase 1

- ✅ Implementar cálculos de área de plantio
- ✅ Gerenciar insumos agrícolas por cultura
- ✅ Criar banco de dados organizado (JSON)
- ✅ Implementar operações CRUD completas
- ✅ Integrar análise estatística com linguagem R
- ✅ Preparar base de dados para integração com fases seguintes

---

## 🔗 Integração com Outras Fases

Esta fase fornece a **base de dados inicial** que alimenta:
- **Fase 2:** Estruturação em banco de dados relacional
- **Fase 3:** Dados para sistema IoT e sensores
- **Fase 4:** Informações para dashboard e Machine Learning
- **Fase 7:** Integração completa no sistema unificado

---

## 🗃 Histórico de lançamentos

| Versão | Data       | Descrição                                    |
|--------|------------|----------------------------------------------|
| 1.0    | 24/03/2025 | Sistema de cálculo e gerenciamento de insumos |

---

## 📋 Licença

MODELO GIT FIAP por FIAP está licenciado sob a licença [Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
