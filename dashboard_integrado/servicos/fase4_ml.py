"""
Serviços da Fase 4 - Irrigação Inteligente com Machine Learning
FarmTech Solutions
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import joblib
import os


class ModeloIrrigacao:
    """Gerencia o modelo de ML para previsão de irrigação"""

    def __init__(self, caminho_modelo: str = None):
        """
        Inicializa o modelo de irrigação

        Args:
            caminho_modelo: Caminho para o arquivo .pkl do modelo treinado
        """
        self.modelo = None
        self.feature_names = ["fosforo", "potassio", "ph", "umidade"]

        # Tentar carregar o modelo do caminho especificado ou do caminho padrão
        if caminho_modelo is None:
            # Caminho padrão para o modelo treinado
            caminho_default = os.path.join(
                os.path.dirname(__file__),
                "..", "..", "fases", "fase_4", "farm_tech", "entrega_2", "dashboard", "modelo_irrigacao.pkl"
            )
            caminho_modelo = os.path.abspath(caminho_default)

        if caminho_modelo and os.path.exists(caminho_modelo):
            try:
                self.modelo = joblib.load(caminho_modelo)
                print(f"✅ Modelo carregado com sucesso: {caminho_modelo}")
            except Exception as e:
                print(f"⚠️ Aviso: Não foi possível carregar o modelo: {e}")
                self.modelo = None
        else:
            print(f"⚠️ Aviso: Arquivo do modelo não encontrado em: {caminho_modelo}")

    def prever_irrigacao(self, fosforo: float, potassio: float, ph: float, umidade: float) -> Dict:
        """
        Prediz a necessidade de irrigação

        Args:
            fosforo: Nível de fósforo (0-1.5)
            potassio: Nível de potássio (0-1.5)
            ph: Valor de pH (0-14)
            umidade: Umidade do solo (0-100%)

        Returns:
            Dict com resultado, confiança e recomendação
        """
        if self.modelo is None:
            return self._recomendacao_heuristica(fosforo, potassio, ph, umidade)

        try:
            entrada = pd.DataFrame(
                [[fosforo, potassio, ph, umidade]],
                columns=self.feature_names
            )

            predicao = self.modelo.predict(entrada)[0]

            # Tentar obter probabilidade se disponível
            if hasattr(self.modelo, 'predict_proba'):
                proba = self.modelo.predict_proba(entrada)[0]
                confianca = max(proba) * 100
            else:
                confianca = 100.0

            return {
                "deve_irrigar": bool(predicao == 1),
                "confianca": round(confianca, 2),
                "recomendacao": "💧 IRRIGAÇÃO NECESSÁRIA" if predicao == 1 else "✅ Não irrigar",
                "motivo": self._gerar_motivo_ml(predicao, fosforo, potassio, ph, umidade)
            }
        except Exception as e:
            print(f"Erro ao fazer predição: {e}")
            return self._recomendacao_heuristica(fosforo, potassio, ph, umidade)

    def _recomendacao_heuristica(self, fosforo: float, potassio: float, ph: float, umidade: float) -> Dict:
        """Fornece recomendação baseada em regras heurísticas quando modelo não está disponível"""

        # Lógica baseada em limiares
        # Irrigar se: umidade baixa OU condições nutricionais ruins
        umidade_critica = umidade < 30  # Umidade muito baixa
        umidade_baixa = umidade < 40  # Umidade abaixo do ideal
        ph_inadequado = ph < 5.5 or ph > 7.5
        nutrientes_baixos = fosforo < 0.8 or potassio < 0.8

        # Decisão: irrigar se umidade está baixa
        # (independente dos outros parâmetros, pois a planta precisa de água)
        deve_irrigar = umidade_baixa

        # Calcular confiança baseada nas condições
        confianca = 85.0
        if umidade_critica:
            confianca = 95.0  # Alta confiança quando umidade está crítica
        elif umidade_baixa and (ph_inadequado or nutrientes_baixos):
            confianca = 90.0  # Alta confiança quando múltiplos fatores indicam irrigação

        return {
            "deve_irrigar": deve_irrigar,
            "confianca": confianca,
            "recomendacao": "💧 IRRIGAÇÃO NECESSÁRIA" if deve_irrigar else "✅ Não irrigar",
            "motivo": self._gerar_motivo_heuristica(fosforo, potassio, ph, umidade)
        }

    def _gerar_motivo_ml(self, predicao: int, fosforo: float, potassio: float, ph: float, umidade: float) -> str:
        """Gera texto explicativo para predição do modelo"""
        motivos = []

        if umidade < 30:
            motivos.append("Umidade muito baixa")
        elif umidade < 40:
            motivos.append("Umidade abaixo do ideal")

        if ph < 5.5 or ph > 7.5:
            motivos.append(f"pH fora da faixa ideal (atual: {ph:.2f})")

        if fosforo < 0.8:
            motivos.append("Fósforo insuficiente")

        if potassio < 0.8:
            motivos.append("Potássio insuficiente")

        if not motivos:
            motivos.append("Condições ótimas")

        return " | ".join(motivos)

    def _gerar_motivo_heuristica(self, fosforo: float, potassio: float, ph: float, umidade: float) -> str:
        """Gera texto explicativo para recomendação heurística"""
        motivos = []

        if umidade < 40:
            motivos.append(f"Umidade baixa ({umidade:.1f}%)")

        if ph < 5.5 or ph > 7.5:
            motivos.append(f"pH inadequado ({ph:.2f})")

        if fosforo < 0.8:
            motivos.append(f"Fósforo baixo ({fosforo:.2f})")

        if potassio < 0.8:
            motivos.append(f"Potássio baixo ({potassio:.2f})")

        if not motivos:
            return "Condições ótimas - sem necessidade de irrigação"

        return " | ".join(motivos)


class AnalisadorHistoricoML:
    """Analisa histórico de predições de irrigação"""

    def __init__(self, dados: List[Dict]):
        """
        Inicializa o analisador

        Args:
            dados: Lista de predições com timestamp
        """
        self.dados = dados

    def estatisticas_gerais(self) -> Dict:
        """Retorna estatísticas gerais das predições"""
        if not self.dados:
            return {
                "total_predicoes": 0,
                "predicoes_positivas": 0,
                "predicoes_negativas": 0,
                "confianca_media": 0.0,
                "taxa_irrigacao": 0.0
            }

        total = len(self.dados)
        positivas = sum(1 for d in self.dados if d.get("deve_irrigar", False))
        negativas = total - positivas
        confianca_media = np.mean([d.get("confianca", 0) for d in self.dados])
        taxa = (positivas / total * 100) if total > 0 else 0

        return {
            "total_predicoes": total,
            "predicoes_positivas": positivas,
            "predicoes_negativas": negativas,
            "confianca_media": round(confianca_media, 2),
            "taxa_irrigacao": round(taxa, 2)
        }

    def tendencia_umidade(self) -> List[float]:
        """Extrai tendência de umidade"""
        return [d.get("umidade", 0) for d in self.dados if "umidade" in d]

    def tendencia_ph(self) -> List[float]:
        """Extrai tendência de pH"""
        return [d.get("ph", 0) for d in self.dados if "ph" in d]

    def predicoes_por_confianca(self) -> Dict[str, int]:
        """Agrupa predições por faixa de confiança"""
        faixas = {
            "Muito Alta (90-100%)": 0,
            "Alta (80-89%)": 0,
            "Média (70-79%)": 0,
            "Baixa (<70%)": 0
        }

        for d in self.dados:
            conf = d.get("confianca", 0)
            if conf >= 90:
                faixas["Muito Alta (90-100%)"] += 1
            elif conf >= 80:
                faixas["Alta (80-89%)"] += 1
            elif conf >= 70:
                faixas["Média (70-79%)"] += 1
            else:
                faixas["Baixa (<70%)"] += 1

        return faixas


def gerar_dados_exemplo_ml() -> Tuple[List[Dict], pd.DataFrame]:
    """
    Gera dados de exemplo para demonstração

    Returns:
        Tupla com (lista de predições, DataFrame dos sensores)
    """
    # Gerar dados de sensores para 24 horas
    base_time = datetime.now()
    sensores_data = []
    predicoes = []

    for i in range(24):
        tempo = (base_time - timedelta(hours=24-i)).strftime("%Y-%m-%d %H:%M:%S")

        # Valores simulados
        umidade = 50 + np.sin(i/6) * 20 + np.random.normal(0, 5)
        ph = 6.5 + np.cos(i/8) * 0.5 + np.random.normal(0, 0.2)
        fosforo = 1.0 + np.random.normal(0, 0.1)
        potassio = 0.9 + np.random.normal(0, 0.1)

        # Garantir valores nos limites
        umidade = max(20, min(80, umidade))
        ph = max(5.0, min(8.0, ph))
        fosforo = max(0.5, min(1.5, fosforo))
        potassio = max(0.5, min(1.5, potassio))

        sensores_data.append({
            "timestamp": tempo,
            "umidade": round(umidade, 1),
            "ph": round(ph, 2),
            "fosforo": round(fosforo, 2),
            "potassio": round(potassio, 2)
        })

        # Gerar predição (simulada)
        modelo = ModeloIrrigacao()
        pred = modelo.prever_irrigacao(fosforo, potassio, ph, umidade)
        pred["timestamp"] = tempo
        pred["umidade"] = round(umidade, 1)
        pred["ph"] = round(ph, 2)
        pred["fosforo"] = round(fosforo, 2)
        pred["potassio"] = round(potassio, 2)
        predicoes.append(pred)

    df_sensores = pd.DataFrame(sensores_data)
    return predicoes, df_sensores


def calcular_impacto_ml(predicoes_positivas: int, total_predicoes: int, area_hectares: float) -> Dict:
    """
    Calcula o impacto econômico e ambiental das predições

    Args:
        predicoes_positivas: Quantidade de predições que indicam irrigação
        total_predicoes: Total de predições
        area_hectares: Área em hectares

    Returns:
        Dict com impactos calculados
    """
    # Supor 1000 litros por hectare por irrigação
    litros_por_ha = 1000

    # Consumo total estimado
    consumo_total = predicoes_positivas * litros_por_ha * area_hectares

    # Economia estimada (economia média: 20% com ML)
    economia_litros = consumo_total * 0.20

    # Custos (valor aproximado: R$0.001 por litro)
    custo_total = consumo_total * 0.001
    economia_custo = economia_litros * 0.001

    # Emissões de CO2 (aproximadamente 0.0005 kg CO2/litro)
    emissoes_total = consumo_total * 0.0005
    reducao_emissoes = economia_litros * 0.0005

    return {
        "consumo_total_litros": round(consumo_total),
        "economia_litros": round(economia_litros),
        "custo_total": round(custo_total, 2),
        "economia_custo": round(economia_custo, 2),
        "emissoes_kg_co2": round(emissoes_total, 2),
        "reducao_emissoes": round(reducao_emissoes, 2)
    }
