import os
from datetime import date

from entrega_2.models.plantacao import Plantacao


class MenuPlantacao:
    def __init__(self, plantacao_service):
        self.plantacao_service = plantacao_service

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_cabecalho(self, titulo):
        self.limpar_tela()
        print("=" * 50)
        print(f"{titulo.center(50)}")
        print("=" * 50)
        print()

    def esperar_tecla(self):
        input("\nPressione ENTER para continuar...")

    def executar(self):
        while True:
            self.exibir_cabecalho("GERENCIAMENTO DE PLANTAÇÕES")
            print("1. Cadastrar Nova Plantação")
            print("2. Listar Todas as Plantações")
            print("3. Buscar Plantação")
            print("4. Editar Plantação")
            print("5. Excluir Plantação")
            print("0. Voltar")
            print()

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_plantacao()
            elif opcao == "2":
                self.listar_plantacoes()
            elif opcao == "3":
                self.buscar_plantacao()
            elif opcao == "4":
                self.editar_plantacao()
            elif opcao == "5":
                self.excluir_plantacao()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                self.esperar_tecla()

    def cadastrar_plantacao(self):
        self.exibir_cabecalho("CADASTRAR PLANTAÇÃO")
        nome = input("Nome da plantação: ")
        localizacao = input("Localização: ")

        data_plantio_str = input("Data de plantio (AAAA-MM-DD): ")
        try:
            data_plantio = date.fromisoformat(data_plantio_str) if data_plantio_str else None
        except ValueError:
            print("Formato de data inválido. Usando a data atual.")
            data_plantio = date.today()

        plantacao = Plantacao(nome=nome, localizacao=localizacao, data_plantio=data_plantio)
        if self.plantacao_service.cadastrar(plantacao):
            print("\nPlantação cadastrada com sucesso!")
        else:
            print("\nErro ao cadastrar plantação.")

        self.esperar_tecla()

    def listar_plantacoes(self):
        self.exibir_cabecalho("LISTA DE PLANTAÇÕES")

        plantacoes = self.plantacao_service.listar_todos()

        if not plantacoes:
            print("Nenhuma plantação cadastrada.")
        else:
            print(f"{'ID':<5} | {'Nome':<20} | {'Localização':<25} | {'Data Plantio':<12}")
            print("-" * 70)

            for p in plantacoes:
                data_formatada = p[3].strftime('%d/%m/%Y') if p[3] else 'N/A'
                print(f"{p[0]:<5} | {p[1]:<20} | {p[2]:<25} | {data_formatada:<12}")

        self.esperar_tecla()

    def buscar_plantacao(self):
        self.exibir_cabecalho("BUSCAR PLANTAÇÃO")

        try:
            id = int(input("Digite o ID da plantação: "))
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        plantacao = self.plantacao_service.buscar_por_id(id)

        if not plantacao:
            print(f"Plantação com ID {id} não encontrada.")
        else:
            print(f"\nID: {plantacao[0]}")
            print(f"Nome: {plantacao[1]}")
            print(f"Localização: {plantacao[2]}")
            data_formatada = plantacao[3].strftime('%d/%m/%Y') if plantacao[3] else 'N/A'
            print(f"Data de Plantio: {data_formatada}")

        self.esperar_tecla()

    def editar_plantacao(self):
        self.exibir_cabecalho("EDITAR PLANTAÇÃO")

        try:
            id = int(input("Digite o ID da plantação: "))
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        plantacao_data = self.plantacao_service.buscar_por_id(id)

        if not plantacao_data:
            print(f"Plantação com ID {id} não encontrada.")
            self.esperar_tecla()
            return

        print(f"\nEditando plantação: {plantacao_data[1]}")

        nome = input(f"Novo nome (atual: {plantacao_data[1]}): ") or plantacao_data[1]
        localizacao = input(f"Nova localização (atual: {plantacao_data[2]}): ") or plantacao_data[2]

        data_atual_formatada = plantacao_data[3].strftime('%Y-%m-%d') if plantacao_data[3] else 'N/A'
        data_plantio_str = input(f"Nova data de plantio (atual: {data_atual_formatada}, formato AAAA-MM-DD): ")

        try:
            data_plantio = date.fromisoformat(data_plantio_str) if data_plantio_str else plantacao_data[3]
        except ValueError:
            print("Formato de data inválido. Mantendo a data atual.")
            data_plantio = plantacao_data[3]

        plantacao = Plantacao(id_plantacao=id, nome=nome, localizacao=localizacao, data_plantio=data_plantio)
        if self.plantacao_service.atualizar(plantacao):
            print("\nPlantação atualizada com sucesso!")
        else:
            print("\nErro ao atualizar plantação.")

        self.esperar_tecla()

    def excluir_plantacao(self):
        self.exibir_cabecalho("EXCLUIR PLANTAÇÃO")

        try:
            id = int(input("Digite o ID da plantação a ser excluída: "))
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        plantacao = self.plantacao_service.buscar_por_id(id)

        if not plantacao:
            print(f"Plantação com ID {id} não encontrada.")
            self.esperar_tecla()
            return

        confirmacao = input(f"Confirma a exclusão da plantação '{plantacao[1]}'? (s/n): ")

        if confirmacao.lower() == 's':
            if self.plantacao_service.excluir(id):
                print("\nPlantação excluída com sucesso!")
            else:
                print("\nErro ao excluir plantação. Verifique se ela possui sensores cadastrados.")
        else:
            print("\nOperação cancelada.")

        self.esperar_tecla()