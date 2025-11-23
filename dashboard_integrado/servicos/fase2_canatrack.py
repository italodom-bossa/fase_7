"""
Serviços da Fase 2 - CanaTrack360
FarmTech Solutions
"""

import uuid
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pandas as pd
from .database import DatabaseManager, DB_FASE2, init_fase2_db


class RegistroColheita:
    """Representa um registro de colheita"""

    def __init__(
        self,
        talhao: str,
        maquina: str,
        operador: str,
        data_colheita: str,
        quantidade_colhida: float,
        tipo_colheita: str,
        perda_estimada: float,
        perda_real: float,
        causa_perda: str = "",
        condicao_solo: str = "Normal",
        condicao_clima: str = "Normal",
        severidade_perda: str = "Leve"
    ):
        self.id = str(uuid.uuid4())[:8]
        self.talhao = talhao
        self.maquina = maquina
        self.operador = operador
        self.data_colheita = data_colheita
        self.quantidade_colhida = quantidade_colhida
        self.tipo_colheita = tipo_colheita
        self.perda_estimada = perda_estimada
        self.perda_real = perda_real
        self.causa_perda = causa_perda
        self.condicao_solo = condicao_solo
        self.condicao_clima = condicao_clima
        self.severidade_perda = severidade_perda
        self.data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calcular_percentual_perda(self) -> float:
        """Calcula percentual de perda em relação à quantidade colhida"""
        if self.quantidade_colhida == 0:
            return 0.0
        return (self.perda_real / self.quantidade_colhida) * 100

    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            "ID": self.id,
            "Talhão": self.talhao,
            "Máquina": self.maquina,
            "Operador": self.operador,
            "Data": self.data_colheita,
            "Quantidade (t)": self.quantidade_colhida,
            "Tipo": self.tipo_colheita,
            "Perda Estimada (t)": self.perda_estimada,
            "Perda Real (t)": self.perda_real,
            "% Perda": f"{self.calcular_percentual_perda():.2f}%",
            "Causa": self.causa_perda,
            "Solo": self.condicao_solo,
            "Clima": self.condicao_clima,
            "Severidade": self.severidade_perda,
            "Registrado": self.data_registro
        }


class AnalisadorPerdas:
    """Analisa perdas de colheita"""

    def __init__(self, registros: List[RegistroColheita]):
        self.registros = registros

    def perda_total(self) -> float:
        """Calcula perda total em toneladas"""
        return sum(r.perda_real for r in self.registros)

    def perda_media(self) -> float:
        """Calcula perda média por colheita"""
        if not self.registros:
            return 0.0
        return self.perda_total() / len(self.registros)

    def quantidade_colhida_total(self) -> float:
        """Calcula quantidade total colhida"""
        return sum(r.quantidade_colhida for r in self.registros)

    def percentual_perda_geral(self) -> float:
        """Calcula percentual de perda geral"""
        total = self.quantidade_colhida_total()
        if total == 0:
            return 0.0
        return (self.perda_total() / total) * 100

    def ranking_operadores(self) -> pd.DataFrame:
        """Retorna ranking de operadores por perda média"""
        if not self.registros:
            return pd.DataFrame()

        df = pd.DataFrame([r.to_dict() for r in self.registros])
        operador_stats = df.groupby("Operador").agg({
            "Perda Real (t)": ["sum", "mean", "count"]
        }).round(2)

        operador_stats.columns = ["Perda Total (t)", "Perda Média (t)", "Colheitas"]
        operador_stats = operador_stats.sort_values("Perda Total (t)", ascending=False)
        return operador_stats

    def ranking_maquinas(self) -> pd.DataFrame:
        """Retorna ranking de máquinas por perda média"""
        if not self.registros:
            return pd.DataFrame()

        df = pd.DataFrame([r.to_dict() for r in self.registros])
        maquina_stats = df.groupby("Máquina").agg({
            "Perda Real (t)": ["sum", "mean", "count"]
        }).round(2)

        maquina_stats.columns = ["Perda Total (t)", "Perda Média (t)", "Colheitas"]
        maquina_stats = maquina_stats.sort_values("Perda Total (t)", ascending=False)
        return maquina_stats

    def ranking_talhaos(self) -> pd.DataFrame:
        """Retorna ranking de talhões com maiores perdas"""
        if not self.registros:
            return pd.DataFrame()

        df = pd.DataFrame([r.to_dict() for r in self.registros])
        talhao_stats = df.groupby("Talhão").agg({
            "Perda Real (t)": ["sum", "mean", "count"]
        }).round(2)

        talhao_stats.columns = ["Perda Total (t)", "Perda Média (t)", "Colheitas"]
        talhao_stats = talhao_stats.sort_values("Perda Total (t)", ascending=False)
        return talhao_stats

    def analise_causa(self) -> Dict[str, int]:
        """Conta ocorrências de causas de perda"""
        causas = {}
        for r in self.registros:
            if r.causa_perda:
                causas[r.causa_perda] = causas.get(r.causa_perda, 0) + 1
        return dict(sorted(causas.items(), key=lambda x: x[1], reverse=True))

    def analise_severidade(self) -> Dict[str, int]:
        """Conta ocorrências por severidade"""
        severidades = {}
        for r in self.registros:
            severidades[r.severidade_perda] = severidades.get(r.severidade_perda, 0) + 1
        return severidades

    def sugestoes_melhorias(self) -> List[str]:
        """Gera sugestões baseadas nas análises"""
        sugestoes = []

        # Análise de perdas altas
        if self.percentual_perda_geral() > 15:
            sugestoes.append("⚠️ Perdas acima do esperado (>15%). Revise configuração de máquinas.")

        # Análise de operadores - usar perda média ao invés de total
        ranking_op = self.ranking_operadores()
        if not ranking_op.empty:
            ranking_op_media = ranking_op.sort_values("Perda Média (t)", ascending=False)
            pior_operador = ranking_op_media.index[0]
            perda_media = ranking_op_media.iloc[0]["Perda Média (t)"]
            sugestoes.append(f"📋 Revisar desempenho do operador: {pior_operador} (média de {perda_media:.1f}t de perda)")

        # Análise de máquinas - usar perda média ao invés de total
        ranking_maq = self.ranking_maquinas()
        if not ranking_maq.empty:
            ranking_maq_media = ranking_maq.sort_values("Perda Média (t)", ascending=False)
            pior_maquina = ranking_maq_media.index[0]
            perda_media_maq = ranking_maq_media.iloc[0]["Perda Média (t)"]
            sugestoes.append(f"🔧 Revisar manutenção da máquina: {pior_maquina} (média de {perda_media_maq:.1f}t de perda)")

        # Análise de condições
        perdas_chuva = sum(1 for r in self.registros if "Chuva" in r.condicao_clima)
        if perdas_chuva > len(self.registros) * 0.3:
            sugestoes.append("☔ Muitas perdas em condições chuvosas. Revise cronograma.")

        return sugestoes


# ===== FUNÇÕES DE BANCO DE DADOS =====

def salvar_registro(registro: RegistroColheita) -> bool:
    """Salva um registro de colheita no banco de dados"""
    try:
        db = DatabaseManager(DB_FASE2)
        db.execute("""
            INSERT INTO registros_colheita (
                id, talhao, maquina, operador, data_colheita,
                quantidade_colhida, tipo_colheita, perda_estimada, perda_real,
                causa_perda, condicao_solo, condicao_clima, severidade_perda,
                data_registro
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            registro.id,
            registro.talhao,
            registro.maquina,
            registro.operador,
            registro.data_colheita,
            registro.quantidade_colhida,
            registro.tipo_colheita,
            registro.perda_estimada,
            registro.perda_real,
            registro.causa_perda,
            registro.condicao_solo,
            registro.condicao_clima,
            registro.severidade_perda,
            registro.data_registro
        ))
        db.close()
        return True
    except Exception as e:
        print(f"Erro ao salvar registro: {e}")
        return False


def carregar_registros() -> List[RegistroColheita]:
    """Carrega todos os registros do banco de dados"""
    try:
        db = DatabaseManager(DB_FASE2)
        rows = db.fetchall("SELECT * FROM registros_colheita ORDER BY data_colheita DESC")

        registros = []
        for row in rows:
            registro = RegistroColheita(
                talhao=row['talhao'],
                maquina=row['maquina'],
                operador=row['operador'],
                data_colheita=row['data_colheita'],
                quantidade_colhida=row['quantidade_colhida'],
                tipo_colheita=row['tipo_colheita'],
                perda_estimada=row['perda_estimada'],
                perda_real=row['perda_real'],
                causa_perda=row['causa_perda'],
                condicao_solo=row['condicao_solo'],
                condicao_clima=row['condicao_clima'],
                severidade_perda=row['severidade_perda']
            )
            registro.id = row['id']
            registro.data_registro = row['data_registro']
            registros.append(registro)

        db.close()
        return registros
    except Exception as e:
        print(f"Erro ao carregar registros: {e}")
        return []


def inicializar_com_exemplos():
    """Inicializa o banco com dados de exemplo se estiver vazio"""
    db = DatabaseManager(DB_FASE2)
    count = db.fetchone("SELECT COUNT(*) as total FROM registros_colheita")
    db.close()

    if count and count['total'] == 0:
        exemplos = gerar_dados_exemplo()
        for registro in exemplos:
            salvar_registro(registro)
        print(f"✅ {len(exemplos)} registros de exemplo adicionados ao banco de dados")


def gerar_dados_exemplo() -> List[RegistroColheita]:
    """Gera dados de exemplo para demonstração"""
    registros = [
        RegistroColheita(
            talhao="A1",
            maquina="Colheitadeira 01",
            operador="João Silva",
            data_colheita="2025-11-20",
            quantidade_colhida=120.0,
            tipo_colheita="Mecanizada",
            perda_estimada=15.0,
            perda_real=8.5,
            causa_perda="Regulagem inadequada",
            condicao_solo="Normal",
            condicao_clima="Seco",
            severidade_perda="Média"
        ),
        RegistroColheita(
            talhao="A2",
            maquina="Colheitadeira 02",
            operador="Maria Santos",
            data_colheita="2025-11-20",
            quantidade_colhida=150.0,
            tipo_colheita="Mecanizada",
            perda_estimada=12.0,
            perda_real=5.2,
            causa_perda="Umidade alta",
            condicao_solo="Úmido",
            condicao_clima="Chuvoso",
            severidade_perda="Leve"
        ),
        RegistroColheita(
            talhao="B1",
            maquina="Colheitadeira 01",
            operador="João Silva",
            data_colheita="2025-11-21",
            quantidade_colhida=135.0,
            tipo_colheita="Mecanizada",
            perda_estimada=18.0,
            perda_real=12.3,
            causa_perda="Desgaste de componentes",
            condicao_solo="Desfavorável",
            condicao_clima="Seco",
            severidade_perda="Alto"
        ),
        RegistroColheita(
            talhao="B2",
            maquina="Colheitadeira 03",
            operador="Pedro Costa",
            data_colheita="2025-11-21",
            quantidade_colhida=110.0,
            tipo_colheita="Mecanizada",
            perda_estimada=10.0,
            perda_real=4.1,
            causa_perda="Regulagem inadequada",
            condicao_solo="Normal",
            condicao_clima="Seco",
            severidade_perda="Leve"
        ),
        RegistroColheita(
            talhao="C1",
            maquina="Colheitadeira 02",
            operador="Maria Santos",
            data_colheita="2025-11-22",
            quantidade_colhida=140.0,
            tipo_colheita="Mecanizada",
            perda_estimada=14.0,
            perda_real=6.8,
            causa_perda="Falha operacional",
            condicao_solo="Normal",
            condicao_clima="Nublado",
            severidade_perda="Média"
        ),
        RegistroColheita(
            talhao="C2",
            maquina="Colheitadeira 03",
            operador="Pedro Costa",
            data_colheita="2025-11-22",
            quantidade_colhida=125.0,
            tipo_colheita="Mecanizada",
            perda_estimada=11.0,
            perda_real=3.5,
            causa_perda="Condições climáticas",
            condicao_solo="Normal",
            condicao_clima="Seco",
            severidade_perda="Leve"
        ),
        RegistroColheita(
            talhao="D1",
            maquina="Colheitadeira 01",
            operador="Carlos Almeida",
            data_colheita="2025-11-22",
            quantidade_colhida=130.0,
            tipo_colheita="Mecanizada",
            perda_estimada=16.0,
            perda_real=9.2,
            causa_perda="Regulagem inadequada",
            condicao_solo="Seco",
            condicao_clima="Ventoso",
            severidade_perda="Média"
        ),
        RegistroColheita(
            talhao="D2",
            maquina="Colheitadeira 04",
            operador="Ana Paula",
            data_colheita="2025-11-23",
            quantidade_colhida=145.0,
            tipo_colheita="Mecanizada",
            perda_estimada=13.0,
            perda_real=4.8,
            causa_perda="Condições climáticas",
            condicao_solo="Normal",
            condicao_clima="Nublado",
            severidade_perda="Leve"
        ),
        RegistroColheita(
            talhao="E1",
            maquina="Colheitadeira 02",
            operador="Maria Santos",
            data_colheita="2025-11-23",
            quantidade_colhida=155.0,
            tipo_colheita="Mecanizada",
            perda_estimada=12.0,
            perda_real=5.9,
            causa_perda="Umidade alta",
            condicao_solo="Úmido",
            condicao_clima="Chuvoso",
            severidade_perda="Média"
        ),
        RegistroColheita(
            talhao="E2",
            maquina="Colheitadeira 03",
            operador="Pedro Costa",
            data_colheita="2025-11-23",
            quantidade_colhida=128.0,
            tipo_colheita="Mecanizada",
            perda_estimada=10.0,
            perda_real=3.2,
            causa_perda="Desgaste de componentes",
            condicao_solo="Normal",
            condicao_clima="Seco",
            severidade_perda="Leve"
        ),
        RegistroColheita(
            talhao="F1",
            maquina="Colheitadeira 01",
            operador="João Silva",
            data_colheita="2025-11-23",
            quantidade_colhida=142.0,
            tipo_colheita="Mecanizada",
            perda_estimada=17.0,
            perda_real=11.5,
            causa_perda="Desgaste de componentes",
            condicao_solo="Desfavorável",
            condicao_clima="Seco",
            severidade_perda="Alto"
        ),
        RegistroColheita(
            talhao="F2",
            maquina="Colheitadeira 04",
            operador="Ana Paula",
            data_colheita="2025-11-23",
            quantidade_colhida=138.0,
            tipo_colheita="Mecanizada",
            perda_estimada=11.0,
            perda_real=4.5,
            causa_perda="Falha operacional",
            condicao_solo="Normal",
            condicao_clima="Seco",
            severidade_perda="Leve"
        ),
    ]
    return registros
