1) DESCRIÇÃO RÁPIDA DO PROJETO:

Para a Fase 7, vamos integrar todos os serviços desenvolvidos nas Fases 1 a 6 e consolidar um sistema de gestão para o agronegócio, que pode ser atualizado para qualquer outro setor da economia, necessitando, apenas, inserir os respectivos dados.

2) DESCRIÇÃO DETALHADA DO PROJETO

Começando com um resgate do que aconteceu da Fase 1 a 6:

Fase 1 – Base de Dados Inicial: implementou-se cálculos de área de plantio e manejo de insumos como etapa inicial, alimentando uma base de dados organizada que servirá de entrada para todo o ecossistema digital. Aplicamos uma conexão com uma API meteorológica pública para depois introduzir uma análise estatística usando a linguagem R sobre essa meteorologia.
Fase 2 – Banco de Dados Estruturado: estruturou-se um banco de dados relacional completo (MER e DER) integrando dados e de manejo agrícola que vierem da Fase 1, organizando-os em tempo real para suporte às futuras decisões analíticas.
Fase 3 – IoT e Automação Inteligente: desenvolveu-se um sistema IoT completo com ESP32 integrando sensores físicos para irrigação automatizada e inteligente com operações CRUD diretamente conectadas ao banco de dados estruturado da Fase 2. Criou-se uma lógica robusta e dinâmica para ativação automática de bombas de irrigação, baseada em medições simuladas e reais (nutrientes, pH via LDR e umidade via DHT22).
Fase 4 – Dashboard Interativo com Data Science: integrou-se Machine Learning com o Scikit-Learn e Streamlit em um dashboard online acessível por gestores agrícolas, permitindo visualização interativa e inteligente das informações e insights para tomada de decisão. Utilizou-se um display LCD e Serial Plotter integrados ao ESP32 para monitoramento físico das métricas críticas em tempo real. Implementou-se algoritmos preditivos que sugiram ações futuras de irrigação e manejo agrícola.
Fase 5 – Cloud Computing & Segurança: hospedou-se toda a infra necessária em Cloud Computing na AWS, o que garante segurança, disponibilidade e escalabilidade, aplicando os padrões de segurança como ISO 27001 e ISO 27002 para garantir a proteção dos dados sensíveis que foram coletados pelos sensores e armazenados no banco de dados cloud.
Fase 6 – Visão Computacional com Redes Neurais: desenvolveu-se um sistema de visão computacional com YOLO para monitoramento visual da saúde das plantações (detecção de pragas, doenças ou crescimento irregular). Nessa fase era opcional a implementação desse reconhecedor utilizando um ESP32-CAM físico para a coleta em tempo real de imagens da lavoura. Contudo, ao invés do ESP32-CAM, você pode usar imagens estáticas e salvas em uma pasta para serem processadas pelo seu algoritmo classificador.
Fase 7 – A Consolidação de um Sistema: nessa fase atual, temos o objetivo de integrar essas etapas usando uma única pasta de projeto em Python que dispara o respectivo serviço de cada Fase por meio de um botão (criação de dashboard) ou de um comando no terminal do VS Code.
Metas da entrega:

Aprimorar a dashboard da Fase 4 (realizada preferencialmente em Python), integrando os serviços de cada Fase (1, 2, 3 e 6) usando botões ou comandos de terminal, mas de modo que todos os programas estejam em uma única pasta de projeto no seu VS Code ou outra IDE de desenvolvimento que o grupo tem preferência. Caso alguma entrega entre as Fases 1 e 6 não tenha sido feita, é a sua chance de tentar fazê-la e pontuar por isso.
Gerar um serviço de alerta aproveitando a infraestrutura AWS criada na Fase 5 para monitorar ou os sensores das Fases 1 ou 3 ou, ainda, os resultados das análises visuais da visão computacional da Fase 6, isto é, implemente um serviço de mensageria na AWS que integre a dashboard geral da fazenda, sugerindo aos funcionários ações corretivas a partir dos dados das Fases 1, 3 ou 6. Os funcionários da fazenda precisam receber um e-mail ou um SMS com os devidos alertas e indicando as ações. As ações devem ser definidas pelo grupo.
Entregável do enunciado:

Monte uma dashboard final (a partir da dash feita na Fase 4), em um único VS Code ou outra IDE, que contenha todos os programas desenvolvidos nas Fases 1, 2, 3 e 6. Caso alguma entrega acima citada não tenha sido realizada, é a sua chance de fazê-la e pontuar por isso.
Monte um serviço simples de mensageria na AWS que dispare alerta para leituras de sensor das Fases 1 ou 3 ou análises da Fase 6. Insira a solução no README do seu GitHub, utilizando prints e comentários claros e objetivos da solução provenientes da AWS.
Desenvolva uma documentação no seu GitHub incluindo todas as melhorias e integrações das Fases 1, 2, 3, 4, 5 e 6 em um novo repositório do GitHub com o nome do seu grupo (de 1 a 5 pessoas ou solo), e nos envie o link do GitHub através do portal da FIAP. Pode enviar o link por um arquivo PDF. Pedimos que não realize nenhum novo commit após o prazo. O seu projeto no GitHub deve estar coerente com a mesma estrutura de pastas e subpastas do VS Code e do modelo já adotado nas entregas anteriores. Caso queira compartilhar o link do seu GitHub com o tutor da turma de forma privada para que não haja vazamento de projetos e suspeita de plágio, o nickname do tutor no GitHub é: leoruiz197.
Grave um vídeo de até 10 minutos apresentando todas as funcionalidades das Fases 1, 2, 3, 4, 5 e 6. Poste no YouTube de forma “não listado”, e coloque o link no seu GitHub dentro do README.

Critério

Descrição

Peso

Repositório no GitHub

O repositório foi criado no prazo e possui a estrutura da pasta do projeto coerente com o VSCode local. Não deve haver commits após a data de entrega.

3.0

VS Code

O computador local contém:

Códigos em Python otimizados e funcionais.
Arquivos organizados e separados com os serviços de cada fase.
Para cada item não entregue agora nessa Fase 7, relativo às Fases 1, 2, 3, 4, 5 e 6, terá um desconto de –0,5 nesse critério VS Code.
3.0

Estrutura do README

O README possui:

Documentação clara e objetiva.
Link para o vídeo demonstrativo no YouTube.
2.0

Vídeo Demonstrativo

O vídeo atende às exigências:

Duração de até 10 minutos.
Demonstra o funcionamento do entregável de forma clara.
Postado no YouTube como “não listado” e incluído no README.
2.0



Detalhes adicionais:

VS Code:
Códigos Python devem ser otimizados, funcionais e executados corretamente.
README:
Deve guiar o leitor para o entendimento completo do sistema da fazenda.
Vídeo:
Deve ser breve, claro e focado no funcionamento da solução entregue.
O link deve estar no README.
Pontualidade:
Entrega no prazo sem commits adicionais é um requisito para a nota máxima.
Avaliação:
90 a 100% de sucesso: todos os critérios atendidos com excelência, código funcional, organização excelente, comparações bem concluídas e vídeo demonstrativo claro.
70 a 89% de sucesso: entrega completa, mas com pequenas falhas de organização ou execução.
50 a 69% de sucesso: projeto entregue com falhas significativas (por exemplo, código não funcional ou documentação incompleta).
0 a 50% de sucesso: entrega não atende aos requisitos mínimos ou está fora do prazo.