-- Scripts para inserção de dados seed para o sistema FarmTech Solutions

-- Inserção de uma plantação inicial
INSERT INTO plantacoes (nome, localizacao, data_plantio)
VALUES ('Fazenda Modelo', 'São Paulo, SP', '2025-03-15');

-- Inserção dos sensores utilizados no sistema (cada um monitora um aspecto específico)
INSERT INTO sensores (id_plantacao, nome, data_instalacao)
VALUES
    (1, 'Sensor de Fósforo', '2025-03-20'),
    (1, 'Sensor de Potássio', '2025-03-20'),
    (1, 'Sensor de pH', '2025-03-20'),
    (1, 'Sensor de Umidade', '2025-03-20'),
    (1, 'Monitor de Irrigação', '2025-03-20');

-- Inserção dos dados de leituras dos sensores baseados no log do ESP32
-- Selecionando apenas leituras significativas e não repetidas para demonstrar o funcionamento

-- Dados do sensor de Fósforo (id_sensor = 1)
INSERT INTO dados_sensores (id_sensor, data_hora_leitura, valor_sensor)
VALUES
    (1, '2025-04-01 08:00:00', 0),
    (1, '2025-04-01 08:15:00', 1),
    (1, '2025-04-01 10:30:00', 0),
    (1, '2025-04-01 13:45:00', 1);

-- Dados do sensor de Potássio (id_sensor = 2)
INSERT INTO dados_sensores (id_sensor, data_hora_leitura, valor_sensor)
VALUES
    (2, '2025-04-01 08:05:00', 0),
    (2, '2025-04-01 08:20:00', 1),
    (2, '2025-04-01 11:30:00', 0),
    (2, '2025-04-01 14:10:00', 1);

-- Dados do sensor de pH (id_sensor = 3)
INSERT INTO dados_sensores (id_sensor, data_hora_leitura, valor_sensor)
VALUES
    (3, '2025-04-01 08:00:00', 3.42),
    (3, '2025-04-01 09:15:00', 9.17),
    (3, '2025-04-01 09:30:00', 9.28),
    (3, '2025-04-01 10:00:00', 8.22),
    (3, '2025-04-01 10:30:00', 6.77),
    (3, '2025-04-01 11:00:00', 6.54),
    (3, '2025-04-01 15:00:00', 10.89),
    (3, '2025-04-01 15:30:00', 11.26);

-- Dados do sensor de Umidade (id_sensor = 4)
INSERT INTO dados_sensores (id_sensor, data_hora_leitura, valor_sensor)
VALUES
    (4, '2025-04-01 08:00:00', 37.0),
    (4, '2025-04-01 12:00:00', 54.5),
    (4, '2025-04-01 12:15:00', 55.0),
    (4, '2025-04-01 14:00:00', 40.0),
    (4, '2025-04-01 14:30:00', 37.5);

-- Dados do monitor de irrigação (id_sensor = 5)
-- 1 = Ligada, 0 = Desligada
INSERT INTO dados_sensores (id_sensor, data_hora_leitura, valor_sensor)
VALUES
    (5, '2025-04-01 08:00:00', 0), -- Desligada
    (5, '2025-04-01 11:15:00', 1), -- Ligada (pH adequado + nutriente + umidade baixa)
    (5, '2025-04-01 11:30:00', 0), -- Desligada
    (5, '2025-04-01 11:45:00', 1), -- Ligada
    (5, '2025-04-01 12:30:00', 0), -- Desligada (umidade acima do limite)
    (5, '2025-04-01 14:45:00', 1), -- Ligada
    (5, '2025-04-01 15:15:00', 0); -- Desligada (pH fora da faixa ideal)