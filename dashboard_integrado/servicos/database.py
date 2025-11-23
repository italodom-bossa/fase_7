"""
Módulo de gerenciamento de banco de dados SQLite
FarmTech Solutions - Dashboard Integrado
"""

import sqlite3
from pathlib import Path
from typing import Optional
import os

# Diretório para armazenar os bancos de dados
DB_DIR = Path(__file__).parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)

# Caminhos dos bancos de dados
DB_FASE1 = DB_DIR / "fase1_calculos.db"
DB_FASE2 = DB_DIR / "fase2_canatrack.db"
DB_FASE3 = DB_DIR / "fase3_iot.db"
DB_FASE6 = DB_DIR / "fase6_yolo.db"


class DatabaseManager:
    """Gerenciador de conexões com banco de dados SQLite"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Conecta ao banco de dados"""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        """Fecha a conexão"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(self, query: str, params: tuple = ()):
        """Executa uma query"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

    def fetchall(self, query: str, params: tuple = ()):
        """Executa query e retorna todos os resultados"""
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def fetchone(self, query: str, params: tuple = ()):
        """Executa query e retorna um resultado"""
        cursor = self.execute(query, params)
        return cursor.fetchone()


def init_fase1_db():
    """Inicializa banco de dados da Fase 1 - Cálculos Agrícolas"""
    db = DatabaseManager(DB_FASE1)

    # Tabela de cálculos salvos
    db.execute("""
        CREATE TABLE IF NOT EXISTS calculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            data_calculo TEXT NOT NULL,
            parametros TEXT NOT NULL,
            resultado TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.close()
    return db


def init_fase2_db():
    """Inicializa banco de dados da Fase 2 - CanaTrack360"""
    db = DatabaseManager(DB_FASE2)

    # Tabela de registros de colheita
    db.execute("""
        CREATE TABLE IF NOT EXISTS registros_colheita (
            id TEXT PRIMARY KEY,
            talhao TEXT NOT NULL,
            maquina TEXT NOT NULL,
            operador TEXT NOT NULL,
            data_colheita TEXT NOT NULL,
            quantidade_colhida REAL NOT NULL,
            tipo_colheita TEXT NOT NULL,
            perda_estimada REAL NOT NULL,
            perda_real REAL NOT NULL,
            causa_perda TEXT,
            condicao_solo TEXT,
            condicao_clima TEXT,
            severidade_perda TEXT,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.close()
    return db


def init_fase3_db():
    """Inicializa banco de dados da Fase 3 - IoT e Sensores"""
    db = DatabaseManager(DB_FASE3)

    # Tabela de leituras de sensores
    db.execute("""
        CREATE TABLE IF NOT EXISTS leituras_sensores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            tipo_sensor TEXT NOT NULL,
            valor REAL NOT NULL,
            unidade TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de histórico de irrigação
    db.execute("""
        CREATE TABLE IF NOT EXISTS historico_irrigacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            motivo TEXT NOT NULL,
            duracao_minutos INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de alertas
    db.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            severidade TEXT NOT NULL,
            sensor_id TEXT,
            timestamp TEXT NOT NULL,
            enviado INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de contatos para notificações
    db.execute("""
        CREATE TABLE IF NOT EXISTS contatos_notificacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            ativo INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.close()
    return db




def init_fase6_db():
    """Inicializa banco de dados da Fase 6 - YOLO Vision"""
    db = DatabaseManager(DB_FASE6)

    # Tabela de detecções YOLO
    db.execute("""
        CREATE TABLE IF NOT EXISTS deteccoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            total_objetos INTEGER NOT NULL,
            confianca_media REAL NOT NULL,
            modo_deteccao TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de objetos detectados (detalhes)
    db.execute("""
        CREATE TABLE IF NOT EXISTS objetos_detectados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deteccao_id INTEGER NOT NULL,
            classe TEXT NOT NULL,
            classe_original TEXT NOT NULL,
            classe_id INTEGER NOT NULL,
            confianca REAL NOT NULL,
            bbox_x INTEGER,
            bbox_y INTEGER,
            bbox_width INTEGER,
            bbox_height INTEGER,
            area_pixels INTEGER,
            FOREIGN KEY (deteccao_id) REFERENCES deteccoes (id)
        )
    """)

    db.close()
    return db


def init_all_databases():
    """Inicializa todos os bancos de dados"""
    init_fase1_db()
    init_fase2_db()
    init_fase3_db()
    print(f"✅ Bancos de dados inicializados em: {DB_DIR}")


if __name__ == "__main__":
    init_all_databases()
