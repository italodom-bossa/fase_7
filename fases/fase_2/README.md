# FIAP - Faculdade de Informática e Administração Paulista

## 📌 Nome do projeto
**CanaTrack360 — Sistema de Rastreabilidade e Análise de Perdas na Colheita Mecanizada da Cana-de-Açúcar**

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

A colheita mecanizada da cana-de-açúcar, embora eficiente, ainda sofre com perdas significativas de produtividade que podem chegar a até 15% da produção. Essas perdas são causadas por falhas operacionais, regulagem inadequada das máquinas, desgaste de componentes, condições climáticas desfavoráveis e desempenho inconsistente de operadores.

**CanaTrack360** é uma solução em Python desenvolvida para permitir que produtores e gestores do setor sucroenergético possam **rastrear, registrar e analisar com precisão os dados operacionais de cada colheita**. A aplicação registra informações como:

- Talhão onde ocorreu a colheita;
- Máquina e operador responsáveis;
- Quantidade colhida;
- Tipo de colheita (manual ou mecanizada);
- Perda estimada e real;
- Causa da perda e condições do solo/clima;
- Severidade da perda (leve, moderada ou crítica).

Com base nessas informações, o sistema **gera relatórios detalhados** com rankings e sugestões de melhoria, ajudando na tomada de decisão e na redução de perdas futuras.

---

## 🔧 Como executar o código

### ✅ Pré-requisitos

- Python 3.11+
- Oracle Database (XE ou similar)
- IDE recomendada: PyCharm ou VSCode
- Bibliotecas:
    - `uuid` 
    - `oracledb`
    - `asyncio`

### 🚀 Passo a passo

1. Clone o projeto:
```bash
git clone https://github.com/italodom/projeto-canatrack360.git
cd projeto-canatrack360/src
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o acesso ao banco Oracle no arquivo `config/oracle_config.py`.

4. Execute a aplicação:
```bash
python main.py
```

---

## 🗃 Histórico de lançamentos

| Versão | Data       | Descrição                        |
|------|------------|----------------------------------|
| 1.0  | 21/04/2025 | Primeira versão completa da aplicação |

---

## 📋 Licença

MODELO GIT FIAP por FIAP está licenciado sob a licença [Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
