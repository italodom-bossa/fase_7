"""
Serviços da Fase 1 - Cálculos de Área e Insumos
FarmTech Solutions
"""

import math
from typing import Dict, Tuple


def calcular_area_circulo(raio: float) -> float:
    """
    Calcula área de um círculo

    Args:
        raio: Raio em metros

    Returns:
        Área em m²
    """
    return math.pi * (raio ** 2)


def calcular_area_retangulo(largura: float, comprimento: float) -> float:
    """
    Calcula área de um retângulo

    Args:
        largura: Largura em metros
        comprimento: Comprimento em metros

    Returns:
        Área em m²
    """
    return largura * comprimento


def converter_para_hectares(area_m2: float) -> float:
    """
    Converte área de m² para hectares

    Args:
        area_m2: Área em metros quadrados

    Returns:
        Área em hectares
    """
    return area_m2 / 10000


def calcular_insumos(cultura: str, area_m2: float) -> Dict[str, float]:
    """
    Calcula quantidade de insumos necessários baseado na cultura e área

    Args:
        cultura: Nome da cultura (Café ou Soja)
        area_m2: Área em metros quadrados

    Returns:
        Dicionário com insumos e quantidades
    """
    from config import INSUMOS_POR_CULTURA

    if cultura not in INSUMOS_POR_CULTURA:
        raise ValueError(f"Cultura '{cultura}' não encontrada")

    hectares = converter_para_hectares(area_m2)
    insumos_base = INSUMOS_POR_CULTURA[cultura]

    insumos_calculados = {}
    for nome_insumo, valor_por_ha in insumos_base.items():
        insumos_calculados[nome_insumo] = valor_por_ha * hectares

    return insumos_calculados


def formatar_numero_br(numero: float, casas_decimais: int = 2) -> str:
    """
    Formata número no padrão brasileiro (vírgula como separador decimal)

    Args:
        numero: Número a ser formatado
        casas_decimais: Número de casas decimais

    Returns:
        String formatada
    """
    formato = f"{{:,.{casas_decimais}f}}"
    return formato.format(numero).replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_custo_estimado(insumos: Dict[str, float], cultura: str) -> Dict[str, float]:
    """
    Calcula custo estimado dos insumos (valores fictícios para demonstração)

    Args:
        insumos: Dicionário com insumos e quantidades
        cultura: Nome da cultura

    Returns:
        Dicionário com custos por insumo e total
    """
    # Preços fictícios em R$ por unidade
    precos = {
        "Nitrogênio (kg/ha)": 5.50,
        "Fósforo (kg/ha)": 6.20,
        "Potássio (kg/ha)": 4.80,
        "Micronutrientes (Boro, Zinco) (kg/ha)": 15.00,
        "Micronutrientes e Enxofre (S) (kg/ha)": 12.00,
        "Calcário (t/ha)": 180.00,
        "Gesso Agrícola (t/ha)": 220.00,
        "Inseticidas (mL/ha)": 0.08,
        "Fungicidas (mL/ha)": 0.12,
        "Herbicidas (L/ha)": 45.00,
        "Bradyrhizobium (com Mo e Co) (mL/ha)": 0.15,
        "Aplicações Foliares de Micronutrientes (mL/ha)": 0.10
    }

    custos = {}
    total = 0

    for nome_insumo, quantidade in insumos.items():
        preco_unitario = precos.get(nome_insumo, 0)
        custo = quantidade * preco_unitario
        custos[nome_insumo] = custo
        total += custo

    custos["TOTAL"] = total
    return custos


def gerar_relatorio_completo(
    cultura: str,
    tipo_area: str,
    dimensoes: Dict[str, float]
) -> Tuple[float, float, Dict[str, float], Dict[str, float]]:
    """
    Gera relatório completo com área, insumos e custos

    Args:
        cultura: Nome da cultura (Café ou Soja)
        tipo_area: "circular" ou "retangular"
        dimensoes: {"raio": valor} ou {"largura": valor, "comprimento": valor}

    Returns:
        Tupla com (area_m2, hectares, insumos, custos)
    """
    # Calcular área
    if tipo_area == "circular":
        area_m2 = calcular_area_circulo(dimensoes["raio"])
    elif tipo_area == "retangular":
        area_m2 = calcular_area_retangulo(
            dimensoes["largura"],
            dimensoes["comprimento"]
        )
    else:
        raise ValueError("Tipo de área inválido")

    # Converter para hectares
    hectares = converter_para_hectares(area_m2)

    # Calcular insumos
    insumos = calcular_insumos(cultura, area_m2)

    # Calcular custos
    custos = calcular_custo_estimado(insumos, cultura)

    return area_m2, hectares, insumos, custos
