-- Criação do banco de dados (execute somente se ainda não existir)
-- CREATE DATABASE db_agricultura;

-- Criação do esquema de tabelas
-- Conecte-se ao banco db_agricultura antes de executar este trecho

-- Tabela: plantacoes
CREATE TABLE plantacoes (
                            id_plantacao SERIAL PRIMARY KEY,
                            nome VARCHAR(255) NOT NULL,
                            localizacao VARCHAR(255),
                            data_plantio DATE
);

-- Tabela: sensores
CREATE TABLE sensores (
                          id_sensor SERIAL PRIMARY KEY,
                          id_plantacao INTEGER NOT NULL,
                          nome VARCHAR(255) NOT NULL,
                          data_instalacao DATE,
                          CONSTRAINT fk_plantacao
                              FOREIGN KEY (id_plantacao)
                                  REFERENCES plantacoes(id_plantacao)
                                  ON DELETE CASCADE
);

-- Tabela: dados_sensores
CREATE TABLE dados_sensores (
                                id_dado_sensor SERIAL PRIMARY KEY,
                                id_sensor INTEGER NOT NULL,
                                data_hora_leitura TIMESTAMP NOT NULL,
                                valor_sensor DOUBLE PRECISION,
                                CONSTRAINT fk_sensor
                                    FOREIGN KEY (id_sensor)
                                        REFERENCES sensores(id_sensor)
                                        ON DELETE CASCADE
);