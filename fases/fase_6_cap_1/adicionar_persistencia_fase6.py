"""
Script para adicionar persistência de dados na página Fase 6 YOLO
"""
from pathlib import Path

# Ler arquivo da página
page_file = Path(__file__).parent.parent.parent / "dashboard_integrado" / "pages" / "06_🔍_Fase6_YOLO.py"

with open(page_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar import do database no topo (depois de from servicos.fase6_yolo)
if "from servicos.database import" not in content:
    content = content.replace(
        'from servicos.fase6_yolo import (',
        'from servicos.database import DatabaseManager, DB_FASE6\nfrom servicos.fase6_yolo import ('
    )

# 2. Adicionar função para salvar detecção no banco
if "def salvar_deteccao_db" not in content:
    funcao_salvar = '''
# Função para salvar detecção no banco de dados
def salvar_deteccao_db(resultado):
    """Salva detecção no banco de dados"""
    try:
        db = DatabaseManager(DB_FASE6)

        # Inserir detecção principal
        cursor = db.execute("""
            INSERT INTO deteccoes (timestamp, total_objetos, confianca_media, modo_deteccao)
            VALUES (?, ?, ?, ?)
        """, (resultado['timestamp'], resultado['total_objetos'], resultado['confianca_media'], resultado.get('modo', 'Desconhecido')))

        deteccao_id = cursor.lastrowid

        # Inserir objetos detectados
        for det in resultado['deteccoes']:
            db.execute("""
                INSERT INTO objetos_detectados
                (deteccao_id, classe, classe_original, classe_id, confianca,
                 bbox_x, bbox_y, bbox_width, bbox_height, area_pixels)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                deteccao_id,
                det['classe'],
                det.get('classe_original', det['classe']),
                det.get('classe_id', 0),
                det['confianca'],
                det['bbox'].get('x', 0),
                det['bbox'].get('y', 0),
                det['bbox'].get('width', 0),
                det['bbox'].get('height', 0),
                det.get('area_pixels', 0)
            ))

        db.close()
        return True
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
        return False

'''
    # Adicionar função antes da seção de tabs
    content = content.replace(
        '# Tabs\ntab1, tab2, tab3, tab4 = st.tabs(',
        funcao_salvar + '\n# Tabs\ntab1, tab2, tab3, tab4 = st.tabs('
    )

# 3. Adicionar chamada para salvar no banco após detectar objetos
if "salvar_deteccao_db(resultado)" not in content:
    content = content.replace(
        '            # Detectar objetos\n            resultado = detector.detectar_objetos(imagem, confianca_minima)',
        '''            # Detectar objetos
            resultado = detector.detectar_objetos(imagem, confianca_minima)

            # Salvar no banco de dados
            if salvar_deteccao_db(resultado):
                st.success("💾 Detecção salva no banco de dados!")'''
    )

# Salvar arquivo atualizado
with open(page_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Página Fase 6 YOLO atualizada!")
print("✅ Adicionado: import database, função salvar_deteccao_db(), chamada para salvar")
print("✅ Agora as detecções serão salvas no banco de dados fase6_yolo.db")
