1)   CHALLENGE REPLY

Olá, turma.

Chegamos agora à terceira entrega do nosso desafio em parceria com a empresa Hermes Reply, avançando para a Fase 5 do curso. Nesta etapa, vamos transformar o que vocês já coletaram nas fases anteriores em um modelo de banco de dados estruturado e funcional, além de uma introdução à Machine Learning (ML). Talvez esta seja a primeira vez, no desafio, que vocês vão trabalhar com a modelagem completa de dados de sensores com foco na Machine Learning!

A Hermes Reply, como vocês já sabem, trabalha com soluções de digitalização industrial. Uma das etapas fundamentais para a transformação digital é justamente a criação de bases de dados bem-organizadas, capazes de armazenar, consultar e analisar grandes volumes de dados de sensores, para depois serem consultadas por um algoritmo de ML, que, por sua vez, tentará encontrar insights desses dados.

2)   CONTEXTO

Em um ambiente industrial moderno, sensores geram uma grande quantidade de dados em tempo real. Esses dados precisam ser armazenados de forma estruturada para que possam ser acessados, analisados e utilizados em processos de Inteligência Artificial, manutenção preditiva ou melhoria de eficiência.

Por isso, nesta fase, a ideia é criar um banco de dados para guardar os dados dos sensores e, a partir desses dados, construir um modelo simples de ML que consiga fazer uma previsão ou uma classificação.

A proposta é que o banco de dados seja a base onde o modelo de ML buscará as informações para trabalhar, permitindo que tudo se conecte de forma prática e coerente com a modelagem de um banco de dados relacional — capaz de armazenar eficientemente os dados coletados pelos sensores — e com a aplicação de técnicas básicas de ML sobre esses dados, como análises preditivas e classificações simples.

Então, de uma forma sucinta, temos esses desafios:

Modelagem de um banco de dados relacional, representando fielmente os dados coletados pelos sensores do seu projeto.
Aplicação de um modelo de Machine Learning básico, utilizando os dados coletados/simulados, com uma tarefa simples de predição ou classificação.
A ferramenta indicada para a modelagem de banco de dados é o Oracle SQL Developer Data Modeler, mas vocês podem utilizar qualquer outra ferramenta de modelagem ER que preferirem (desde que gerem diagramas legíveis e exportáveis para imagem).

3)   OBJETIVOS

Os objetivos desta entrega são:

Propor uma modelagem de banco de dados funcional e normalizada, adequada para armazenar os dados coletados pelos sensores.
Criar um modelo simples de Machine Learning, utilizando os dados gerados na entrega anterior (ou dados simulados).
Vocês deverão:

Na parte do Banco de Dados:
Elaborar um Diagrama Entidade-Relacionamento (DER) completo;
Definir as principais tabelas, campos, chaves primárias e relacionamentos;
Prever restrições de integridade (exemplo: tipos de dados, limites de tamanho etc.);
Criar um script SQL inicial de criação das tabelas (CREATE TABLE);
Na parte da ML Básico:
Escolher uma tarefa simples de ML: classificação, regressão ou análise preditiva simples;
Utilizar Scikit-learn, Pandas, NumPy ou outras ferramentas vistas no material do curso;
Treinar um modelo básico, utilizando o conjunto de dados da entrega anterior. Aqui, a sugestão é que tenha pelo menos 500 leituras de cada sensor. Caso não tenha, você pode trabalhar com a ingestão de dados artificiais no seu banco e justificar na documentação;
Gerar uma visualização simples do resultado (pode ser um gráfico de barras, linha, matriz de confusão ou até um scatter plot). Justificar qual gráfico adotado;
Documentar o código, os dados usados e as análises obtidas, trazer prints dos gráficos e justificar os resultados.
4)   REQUISITOS TÉCNICOS E FUNCIONAIS

Banco de Dados:

Diagrama ER (Entidade-Relacionamento) com entidades, atributos, relacionamentos, cardinalidades e chaves primárias/estrangeiras;
Descrição de cada entidade e campo, explicando o motivo de sua inclusão;
Script SQL inicial com o código de criação das tabelas;
Prints ou exportações gráficas do modelo criado na ferramenta utilizada;
Previsão de integração futura com ferramentas de visualização de dados.
ML Básico:

Código Python (Jupyter ou .py) mostrando o processo de treino do modelo;
Explicação de qual foi o problema escolhido (exemplo: classificação de níveis de temperatura, previsão de um valor futuro etc.);
Dataset utilizado (pode ser CSV com os dados simulados da fase anterior);
Print ou gráfico dos resultados do modelo (exemplo: accuracy, gráfico de predição, matriz de confusão).
5)   ENTREGÁVEIS

5.1) Documentação via GitHub Público

A entrega deverá ser feita por meio de um repositório público no GitHub, contendo:

Arquivos do projeto de modelagem de banco de dados (.dmd, .sql ou outro formato);
Imagem do Diagrama ER exportado;
Script SQL de criação das tabelas;
Código-fonte do modelo de Machine Learning (Python ou Jupyter Notebook);
CSV ou fonte de dados utilizados para treino/teste;
Gráficos e/ou prints dos resultados obtidos com o modelo;
README explicativo, descrevendo:
Como o banco de dados foi modelado;
Como foi feita a implementação do ML;
Principais resultados obtidos.
Vídeo de até 5 minutos explicando e justificando, com áudio (sem música de fundo), todo o seu projeto dessa fase. Postar no YouTube como “não listado” e adicionar o link no README.
5.2) Regras Gerais

O repositório não poderá sofrer alterações após a data limite de entrega;
Todos os integrantes devem participar da criação e documentação da modelagem;
A avaliação irá considerar: qualidade técnica da modelagem, funcionamento do código de ML, clareza na documentação e organização geral do repositório.