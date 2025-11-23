"""
Script para adicionar suporte a banco de dados para Fase 6 YOLO
"""
import sys
from pathlib import Path

# Adicionar path do dashboard
sys.path.append(str(Path(__file__).parent.parent.parent / "dashboard_integrado"))

# Ler arquivo database.py
db_file = Path(__file__).parent.parent.parent / "dashboard_integrado" / "servicos" / "database.py"

with open(db_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar DB_FASE6
if "DB_FASE6" not in content:
    content = content.replace(
        'DB_FASE3 = DB_DIR / "fase3_iot.db"',
        'DB_FASE3 = DB_DIR / "fase3_iot.db"\nDB_FASE6 = DB_DIR / "fase6_yolo.db"'
    )

# Adicionar função init_fase6_db antes de init_all_databases
if "def init_fase6_db():" not in content:
    init_fase6 = '''

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

'''
    content = content.replace(
        'def init_all_databases():',
        init_fase6 + '\ndef init_all_databases():'
    )

# Adicionar chamada init_fase6_db() em init_all_databases
if "init_fase6_db()" not in content:
    content = content.replace(
        '    init_fase3_db()\n    print',
        '    init_fase3_db()\n    init_fase6_db()\n    print'
    )

# Salvar arquivo atualizado
with open(db_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo database.py atualizado com suporte para Fase 6!")
print("✅ Adicionado: DB_FASE6, init_fase6_db(), tabelas de detecções")

# Inicializar banco
from servicos.database import init_fase6_db
init_fase6_db()
print("✅ Banco de dados fase6_yolo.db criado!")
