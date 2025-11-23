from collections import defaultdict
from statistics import mean

from src.common.utils import get_repositorio

repo = get_repositorio("colheitas")
repo_talhoes = get_repositorio("talhoes")
repo_operadores = get_repositorio("operadores")
repo_maquinas = get_repositorio("maquinas")

async def relatorio_por_talhao():
    colheitas = await repo.listar()

    if not colheitas:
        print("\n📊 Perdas por Talhão:")
        print("Não há dados de colheitas disponíveis.")
        return

    resultado = defaultdict(lambda: {"perdas_totais": 0, "qtd_colheitas": 0, "qtd_colhida_total": 0})

    talhoes = await repo_talhoes.listar()
    nomes_talhoes = {t["id"]: t["nome"] for t in talhoes}

    for c in colheitas:
        talhao_id = c["talhao_id"]
        perda = c.get("perda_real")
        if perda is None:
            continue

        resultado[talhao_id]["perdas_totais"] += perda
        resultado[talhao_id]["qtd_colheitas"] += 1
        resultado[talhao_id]["qtd_colhida_total"] += c["quantidade_colhida"]

    print("\n📊 Perdas por Talhão:")
    if not resultado:
        print("Não há perdas registradas para nenhum talhão.")
        return

    for talhao_id, dados in resultado.items():
        nome_talhao = nomes_talhoes.get(talhao_id, f"Talhão {talhao_id}")
        perdas_totais = dados["perdas_totais"]
        total_colhido = dados["qtd_colhida_total"]

        taxa_perda = (perdas_totais / total_colhido * 100) if total_colhido > 0 else 0

        print(f"{nome_talhao}: total de {round(perdas_totais, 2)} toneladas perdidas ({round(taxa_perda, 2)}% do colhido)")

async def relatorio_por_operador():
    colheitas = await repo.listar()

    if not colheitas:
        print("\n👷 Desempenho por Operador:")
        print("Não há dados de colheitas disponíveis.")
        return

    operador_stats = defaultdict(lambda: {"total": 0, "perda": 0})

    operadores = await repo_operadores.listar()
    nomes_operadores = {o["id"]: o["nome"] for o in operadores}

    for c in colheitas:
        perda = c.get("perda_real")
        if perda is None:
            continue

        operador_id = c["operador_id"]
        operador_stats[operador_id]["total"] += c["quantidade_colhida"]
        operador_stats[operador_id]["perda"] += perda

    print("\n👷 Desempenho por Operador:")
    if not operador_stats:
        print("Não há perdas registradas para nenhum operador.")
        return

    for operador_id, stats in operador_stats.items():
        nome_operador = nomes_operadores.get(operador_id, f"Operador {operador_id}")
        total_colhido = stats["total"]
        total_perdido = stats["perda"]

        taxa_perda = (total_perdido / total_colhido * 100) if total_colhido > 0 else 0

        print(f"{nome_operador}: {round(total_colhido, 2)} t colhidas — {round(total_perdido, 2)} t perdidas ({round(taxa_perda, 2)}%)")

async def relatorio_por_maquina():
    colheitas = await repo.listar()

    if not colheitas:
        print("\n🚜 Desempenho por Máquina:")
        print("Não há dados de colheitas disponíveis.")
        return

    maquina_stats = defaultdict(lambda: {"total": 0, "perda": 0})

    maquinas = await repo_maquinas.listar()
    detalhes_maquinas = {m["id"]: f"{m['modelo']} ({m['ano']})" for m in maquinas}

    for c in colheitas:
        perda = c.get("perda_real")
        if perda is None:
            continue

        maquina_id = c["maquina_id"]
        maquina_stats[maquina_id]["total"] += c["quantidade_colhida"]
        maquina_stats[maquina_id]["perda"] += perda

    print("\n🚜 Desempenho por Máquina:")
    if not maquina_stats:
        print("Não há perdas registradas para nenhuma máquina.")
        return

    for maquina_id, stats in maquina_stats.items():
        descricao_maquina = detalhes_maquinas.get(maquina_id, f"Máquina {maquina_id}")
        total_colhido = stats["total"]
        total_perdido = stats["perda"]

        taxa_perda = (total_perdido / total_colhido * 100) if total_colhido > 0 else 0

        print(f"{descricao_maquina}: {round(total_colhido, 2)} t colhidas — {round(total_perdido, 2)} t perdidas ({round(taxa_perda, 2)}%)")

async def ranking_causas_perda():
    colheitas = await repo.listar()

    if not colheitas:
        print("\n🔎 Causas mais frequentes de perda:")
        print("Não há dados de colheitas disponíveis.")
        return

    causas = defaultdict(int)
    causas_perda_total = defaultdict(float)

    for c in colheitas:
        if not c.get("causa_perda"):
            continue

        perda = c.get("perda_real")
        if perda is None:
            continue

        causas[c["causa_perda"]] += 1
        causas_perda_total[c["causa_perda"]] += perda

    print("\n🔎 Causas mais frequentes de perda:")
    if not causas:
        print("Nenhuma causa de perda registrada.")
        return

    for causa, qtd in sorted(causas.items(), key=lambda x: x[1], reverse=True):
        perda_total = causas_perda_total[causa]
        print(f"{causa}: {qtd} ocorrência(s) - Total de {round(perda_total, 2)} t perdidas")

async def resumo_geral():
    colheitas = await repo.listar()

    if not colheitas:
        print("\n📌 RESUMO GERAL:")
        print("Não há dados de colheitas disponíveis.")
        return

    colheitas_com_perda = [c for c in colheitas if c.get("perda_real") is not None]

    if not colheitas_com_perda:
        print("\n📌 RESUMO GERAL:")
        print("Existem colheitas registradas, mas nenhuma possui valor de perda real.")
        return

    total_colhido = sum(c["quantidade_colhida"] for c in colheitas_com_perda)
    total_perda = sum(c["perda_real"] for c in colheitas_com_perda)

    perda_percentual = (total_perda / total_colhido * 100) if total_colhido else 0

    talhoes_unicos = len(set(c["talhao_id"] for c in colheitas_com_perda))
    operadores_unicos = len(set(c["operador_id"] for c in colheitas_com_perda))
    maquinas_unicas = len(set(c["maquina_id"] for c in colheitas_com_perda))

    print("\n📌 RESUMO GERAL:")
    print(f"Total de colheitas com perdas registradas: {len(colheitas_com_perda)}")
    print(f"Talhões envolvidos: {talhoes_unicos}")
    print(f"Operadores envolvidos: {operadores_unicos}")
    print(f"Máquinas utilizadas: {maquinas_unicas}")
    print(f"Total colhido: {round(total_colhido, 2)} t")
    print(f"Total de perda real: {round(total_perda, 2)} t")
    print(f"Taxa média de perda: {round(perda_percentual, 2)}%")