-- Tabela de Operadores
CREATE TABLE operadores (
                            id VARCHAR2(36) PRIMARY KEY,
                            nome VARCHAR2(100) NOT NULL,
                            turno VARCHAR2(20) NOT NULL
);

-- Tabela de Máquinas
CREATE TABLE maquinas (
                          id VARCHAR2(36) PRIMARY KEY,
                          modelo VARCHAR2(100) NOT NULL,
                          ano NUMBER(4) NOT NULL,
                          tipo VARCHAR2(50) NOT NULL
);

-- Tabela de Talhões
CREATE TABLE talhoes (
                         id VARCHAR2(36) PRIMARY KEY,
                         nome VARCHAR2(100) NOT NULL,
                         localizacao VARCHAR2(200) NOT NULL,
                         hectares NUMBER(10,2) NOT NULL,
                         tipo_solo VARCHAR2(50) NOT NULL
);

-- Tabela de Colheitas
CREATE TABLE colheitas (
                           id VARCHAR2(36) PRIMARY KEY,
                           talhao_id VARCHAR2(36) NOT NULL,
                           operador_id VARCHAR2(36) NOT NULL,
                           maquina_id VARCHAR2(36) NOT NULL,
                           tipo_colheita VARCHAR2(20) NOT NULL,
                           quantidade_colhida NUMBER(10,2) NOT NULL,
                           perda_estimada NUMBER(10,2),
                           perda_real NUMBER(10,2),
                           causa_perda VARCHAR2(200),
                           severidade VARCHAR2(50),
                           data DATE,
                           condicoes CLOB,
                           CONSTRAINT fk_talhao FOREIGN KEY (talhao_id) REFERENCES talhoes(id),
                           CONSTRAINT fk_operador FOREIGN KEY (operador_id) REFERENCES operadores(id),
                           CONSTRAINT fk_maquina FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
);
