import asyncio

from src.common.utils import obter_entrada_nao_vazia, obter_numero_positivo
from src.maquinas import cadastrar_maquina, listar_maquinas, atualizar_maquina, deletar_maquina
from src.operadores import cadastrar_operador, listar_operadores, atualizar_operador, deletar_operador
from src.registro_colheita import registrar_colheita, listar_colheitas, atualizar_colheita, deletar_colheita, \
    selecionar_talhao, selecionar_operador, selecionar_maquina, obter_opcao_tipo_colheita, obter_opcao_severidade
from src.relatorios import resumo_geral, relatorio_por_talhao, relatorio_por_operador, relatorio_por_maquina, \
    ranking_causas_perda
from src.talhoes import cadastrar_talhao, listar_talhoes, atualizar_talhao, deletar_talhao

async def menu_principal():
    while True:
        print("""
========= CanaTrack360 =========
1. Talhões
2. Operadores
3. Máquinas
4. Colheitas
5. Relatórios
0. Sair
===============================""")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            await menu_talhoes()
        elif escolha == "2":
            await menu_operadores()
        elif escolha == "3":
            await menu_maquinas()
        elif escolha == "4":
            await menu_colheitas()
        elif escolha == "5":
            await menu_relatorios()
        elif escolha == "0":
            break
        else:
            print("Opção inválida.")

# TALHÕES
async def menu_talhoes():
    while True:
        print("""
--- TALHÕES ---
1. Cadastrar
2. Listar
3. Atualizar
4. Deletar
0. Voltar""")
        op = input("Escolha: ")

        if op == "1":
            nome = obter_entrada_nao_vazia("Nome: ", "O nome do talhão não pode estar vazio.")
            localizacao = obter_entrada_nao_vazia("Localização: ", "A localização não pode estar vazia.")
            hectares = obter_numero_positivo("Hectares: ", "Hectares deve ser um número positivo.")

            tipo_solo = None

            await cadastrar_talhao(nome, localizacao, hectares, tipo_solo)

        elif op == "2":
            await listar_talhoes()

        elif op == "3":
            id_ = obter_entrada_nao_vazia("ID do talhão: ", "O ID não pode estar vazio.")
            nome = obter_entrada_nao_vazia("Novo nome: ", "O nome não pode estar vazio.")
            localizacao = obter_entrada_nao_vazia("Nova localização: ", "A localização não pode estar vazia.")
            hectares = obter_numero_positivo("Novo hectares: ", "Hectares deve ser um número positivo.")

            tipo_solo = None

            await atualizar_talhao(id_, nome, localizacao, hectares, tipo_solo)

        elif op == "4":
            id_ = obter_entrada_nao_vazia("ID a deletar: ", "O ID não pode estar vazio.")
            await deletar_talhao(id_)

        elif op == "0":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


# OPERADORES
async def menu_operadores():
    while True:
        print("""
--- OPERADORES ---
1. Cadastrar
2. Listar
3. Atualizar
4. Deletar
0. Voltar""")
        op = input("Escolha: ")

        if op == "1":
            nome = obter_entrada_nao_vazia("Nome: ", "O nome do operador não pode estar vazio.")
            
            turno = None
            
            await cadastrar_operador(nome, turno)
            
        elif op == "2":
            await listar_operadores()
            
        elif op == "3":
            id_ = obter_entrada_nao_vazia("ID do operador: ", "O ID não pode estar vazio.")
            nome = obter_entrada_nao_vazia("Novo nome: ", "O nome não pode estar vazio.")
            
            turno = None
            
            await atualizar_operador(id_, nome, turno)
            
        elif op == "4":
            id_ = obter_entrada_nao_vazia("ID a deletar: ", "O ID não pode estar vazio.")
            await deletar_operador(id_)
            
        elif op == "0":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# MAQUINAS
async def menu_maquinas():
    while True:
        print("""
--- MÁQUINAS ---
1. Cadastrar
2. Listar
3. Atualizar
4. Deletar
0. Voltar""")
        op = input("Escolha: ")

        if op == "1":
            modelo = obter_entrada_nao_vazia("Modelo: ", "O modelo da máquina não pode estar vazio.")
            
            ano = None
            while ano is None:
                try:
                    ano_input = input("Ano: ")
                    if not ano_input.strip():
                        print("O ano não pode estar vazio.")
                        continue
                        
                    ano_temp = int(ano_input)
                    import datetime
                    ano_atual = datetime.datetime.now().year
                    if ano_temp < 1900 or ano_temp > ano_atual + 1:
                        print(f"O ano deve estar entre 1900 e {ano_atual + 1}.")
                        continue
                        
                    ano = ano_temp
                except ValueError:
                    print("Por favor, digite um ano válido (número inteiro).")
            
            tipo = None
            
            await cadastrar_maquina(modelo, ano, tipo)
            
        elif op == "2":
            await listar_maquinas()
            
        elif op == "3":
            id_ = obter_entrada_nao_vazia("ID da máquina: ", "O ID não pode estar vazio.")
            modelo = obter_entrada_nao_vazia("Novo modelo: ", "O modelo não pode estar vazio.")
            
            ano = None
            while ano is None:
                try:
                    ano_input = input("Novo ano: ")
                    if not ano_input.strip():
                        print("O ano não pode estar vazio.")
                        continue
                        
                    ano_temp = int(ano_input)
                    import datetime
                    ano_atual = datetime.datetime.now().year
                    if ano_temp < 1900 or ano_temp > ano_atual + 1:
                        print(f"O ano deve estar entre 1900 e {ano_atual + 1}.")
                        continue
                        
                    ano = ano_temp
                except ValueError:
                    print("Por favor, digite um ano válido (número inteiro).")
            
            tipo = None
            
            await atualizar_maquina(id_, modelo, ano, tipo)
            
        elif op == "4":
            id_ = obter_entrada_nao_vazia("ID a deletar: ", "O ID não pode estar vazio.")
            await deletar_maquina(id_)
            
        elif op == "0":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# COLHEITAS
async def menu_colheitas():
    while True:
        print("""
--- REGISTRO DE COLHEITAS ---
1. Registrar Nova Colheita
2. Listar Colheitas
3. Atualizar Colheita
4. Deletar Colheita
0. Voltar""")
        op = input("Escolha: ")

        if op == "1":
            talhao_id = await selecionar_talhao()
            if not talhao_id:
                continue

            operador_id = await selecionar_operador()
            if not operador_id:
                continue

            maquina_id = await selecionar_maquina()
            if not maquina_id:
                continue

            tipo_colheita = obter_opcao_tipo_colheita()

            quantidade_colhida = obter_numero_positivo("Quantidade colhida (toneladas): ")

            tem_perda_real = input("Informar perda real? (s/n): ").lower().strip() == 's'
            perda_real = None
            causa_perda = ""
            severidade = ""

            if tem_perda_real:
                while True:
                    try:
                        perda_input = input("Perda real (toneladas): ")
                        if not perda_input.strip():
                            print("Informe a perda real ou digite '0'.")
                            continue

                        perda_real = float(perda_input)
                        if perda_real < 0:
                            print("A perda real não pode ser negativa.")
                            continue

                        if perda_real > quantidade_colhida:
                            print("A perda real não pode ser maior que a quantidade colhida.")
                            continue

                        causa_perda = input("Causa da perda: ").strip()
                        severidade = obter_opcao_severidade()
                        break
                    except ValueError:
                        print("Por favor, digite um número válido.")

            data_input = input("Data da colheita (YYYY-MM-DD) ou deixe em branco para usar data atual: ").strip()
            data = data_input if data_input else None

            await registrar_colheita(
                talhao_id,
                operador_id,
                maquina_id,
                tipo_colheita,
                quantidade_colhida,
                perda_real,
                causa_perda,
                severidade,
                None,  # Condições
                data
            )

        elif op == "2":
            await listar_colheitas()

        elif op == "3":
            colheitas = await listar_colheitas()
            if not colheitas:
                continue

            id_colheita = input("Digite o ID da colheita que deseja atualizar: ").strip()
            if not id_colheita:
                print("ID não pode estar vazio.")
                continue

            print("Deixe em branco os campos que não deseja alterar:")

            novos_dados = {}

            alterar_tipo = input("Alterar tipo de colheita? (s/n): ").lower().strip() == 's'
            if alterar_tipo:
                novos_dados['tipo_colheita'] = obter_opcao_tipo_colheita()

            alterar_quantidade = input("Alterar quantidade colhida? (s/n): ").lower().strip() == 's'
            if alterar_quantidade:
                novos_dados['quantidade_colhida'] = obter_numero_positivo("Nova quantidade colhida (toneladas): ")

            alterar_perda = input("Alterar perda real? (s/n): ").lower().strip() == 's'
            if alterar_perda:
                tem_perda = input("Informar perda real? (s/n): ").lower().strip() == 's'
                if tem_perda:
                    quantidade = novos_dados.get('quantidade_colhida', None)
                    while True:
                        try:
                            perda_input = input("Nova perda real (toneladas): ")
                            if not perda_input.strip():
                                print("Informe a perda real ou digite '0'.")
                                continue

                            perda_real = float(perda_input)
                            if perda_real < 0:
                                print("A perda real não pode ser negativa.")
                                continue

                            if quantidade and perda_real > quantidade:
                                print("A perda real não pode ser maior que a quantidade colhida.")
                                continue

                            novos_dados['perda_real'] = perda_real
                            break
                        except ValueError:
                            print("Por favor, digite um número válido.")

                    novos_dados['causa_perda'] = input("Nova causa da perda: ").strip()
                    novos_dados['severidade'] = obter_opcao_severidade()
                else:
                    novos_dados['perda_real'] = None
                    novos_dados['causa_perda'] = ""
                    novos_dados['severidade'] = ""

            alterar_data = input("Alterar data? (s/n): ").lower().strip() == 's'
            if alterar_data:
                data_input = input("Nova data (YYYY-MM-DD): ").strip()
                if data_input:
                    novos_dados['data'] = data_input

            if novos_dados:
                await atualizar_colheita(id_colheita, novos_dados)
            else:
                print("Nenhum dado foi alterado.")

        elif op == "4":
            colheitas = await listar_colheitas()
            if not colheitas:
                continue

            id_colheita = input("Digite o ID da colheita que deseja deletar: ").strip()
            if not id_colheita:
                print("ID não pode estar vazio.")
                continue

            confirma = input(f"Tem certeza que deseja deletar a colheita {id_colheita}? (s/n): ").lower().strip()
            if confirma == 's':
                await deletar_colheita(id_colheita)

        elif op == "0":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


# RELATÓRIOS
async def menu_relatorios():
    await resumo_geral()
    await relatorio_por_talhao()
    await relatorio_por_operador()
    await relatorio_por_maquina()
    await ranking_causas_perda()

async def main():
    await menu_principal()

# INÍCIO
if __name__ == "__main__":
    asyncio.run(main())