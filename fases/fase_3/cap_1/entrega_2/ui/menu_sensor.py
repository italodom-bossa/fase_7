import os
from datetime import date

from entrega_2.models.sensor import Sensor


class MenuSensor:
    def __init__(self, plantacao_service, sensor_service):
        self.plantacao_service = plantacao_service
        self.sensor_service = sensor_service

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
            self.exibir_cabecalho("GERENCIAMENTO DE SENSORES")
            print("1. Cadastrar Novo Sensor")
            print("2. Listar Todos os Sensores")
            print("3. Listar Sensores por Plantação")
            print("4. Buscar Sensor")
            print("5. Editar Sensor")
            print("6. Excluir Sensor")
            print("0. Voltar")
            print()

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_sensor()
            elif opcao == "2":
                self.listar_sensores()
            elif opcao == "3":
                self.listar_sensores_por_plantacao()
            elif opcao == "4":
                self.buscar_sensor()
            elif opcao == "5":
                self.editar_sensor()
            elif opcao == "6":
                self.excluir_sensor()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                self.esperar_tecla()

    def cadastrar_sensor(self):
        self.exibir_cabecalho("CADASTRAR SENSOR")

        # Listar plantações disponíveis
        plantacoes = self.plantacao_service.listar_todos()

        if not plantacoes:
            print("Não existem plantações cadastradas. Cadastre uma plantação primeiro.")
            self.esperar_tecla()
            return

        print("Plantações disponíveis:")
        for p in plantacoes:
            print(f"{p[0]}: {p[1]}")

        try:
            id_plantacao = int(input("\nID da plantação: "))
            # Verificar se a plantação existe
            plantacao = self.plantacao_service.buscar_por_id(id_plantacao)
            if not plantacao:
                print(f"Plantação com ID {id_plantacao} não encontrada.")
                self.esperar_tecla()
                return
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        nome = input("Nome do sensor: ")

        data_instalacao_str = input("Data de instalação (AAAA-MM-DD): ")
        try:
            data_instalacao = date.fromisoformat(data_instalacao_str) if data_instalacao_str else None
        except ValueError:
            print("Formato de data inválido. Usando a data atual.")
            data_instalacao = date.today()

        sensor = Sensor(id_plantacao=id_plantacao, nome=nome, data_instalacao=data_instalacao)
        if self.sensor_service.cadastrar(sensor):
            print("\nSensor cadastrado com sucesso!")
        else:
            print("\nErro ao cadastrar sensor.")

        self.esperar_tecla()

    def listar_sensores(self):
        self.exibir_cabecalho("LISTA DE SENSORES")

        sensores = self.sensor_service.listar_todos()

        if not sensores:
            print("Nenhum sensor cadastrado.")
        else:
            print(f"{'ID':<5} | {'Nome':<20} | {'Plantação':<20} | {'Data Instalação':<15}")
            print("-" * 70)

            for s in sensores:
                data_formatada = s[3].strftime('%d/%m/%Y') if s[3] else 'N/A'
                print(f"{s[0]:<5} | {s[2]:<20} | {s[4]:<20} | {data_formatada:<15}")

        self.esperar_tecla()

    def listar_sensores_por_plantacao(self):
        self.exibir_cabecalho("LISTAR SENSORES POR PLANTAÇÃO")

        # Listar plantações disponíveis
        plantacoes = self.plantacao_service.listar_todos()

        if not plantacoes:
            print("Não existem plantações cadastradas.")
            self.esperar_tecla()
            return

        print("Plantações disponíveis:")
        for p in plantacoes:
            print(f"{p[0]}: {p[1]}")

        try:
            id_plantacao = int(input("\nID da plantação: "))
            # Verificar se a plantação existe
            plantacao = self.plantacao_service.buscar_por_id(id_plantacao)
            if not plantacao:
                print(f"Plantação com ID {id_plantacao} não encontrada.")
                self.esperar_tecla()
                return
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        sensores = self.sensor_service.listar_por_plantacao(id_plantacao)

        if not sensores:
            print(f"Nenhum sensor cadastrado para a plantação '{plantacao[1]}'.")
        else:
            print(f"\nSensores da plantação '{plantacao[1]}':")
            print(f"{'ID':<5} | {'Nome':<20} | {'Data Instalação':<15}")
            print("-" * 50)

            for s in sensores:
                data_formatada = s[3].strftime('%d/%m/%Y') if s[3] else 'N/A'
                print(f"{s[0]:<5} | {s[2]:<20} | {data_formatada:<15}")

        self.esperar_tecla()

    def buscar_sensor(self):
        self.exibir_cabecalho("BUSCAR SENSOR")

        try:
            id = int(input("Digite o ID do sensor: "))
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        sensor = self.sensor_service.buscar_por_id(id)

        if not sensor:
            print(f"Sensor com ID {id} não encontrado.")
        else:
            print(f"\nID: {sensor[0]}")
            print(f"Nome: {sensor[2]}")
            print(f"Plantação: {sensor[4]} (ID: {sensor[1]})")
            data_formatada = sensor[3].strftime('%d/%m/%Y') if sensor[3] else 'N/A'
            print(f"Data de Instalação: {data_formatada}")

        self.esperar_tecla()

    def editar_sensor(self):
        self.exibir_cabecalho("EDITAR SENSOR")

        try:
            id = int(input("Digite o ID do sensor: "))
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        sensor_data = self.sensor_service.buscar_por_id(id)

        if not sensor_data:
            print(f"Sensor com ID {id} não encontrado.")
            self.esperar_tecla()
            return

        print(f"\nEditando sensor: {sensor_data[2]}")

        # Listar plantações disponíveis
        plantacoes = self.plantacao_service.listar_todos()

        print("Plantações disponíveis:")
        for p in plantacoes:
            print(f"{p[0]}: {p[1]}")

        try:
            id_plantacao_str = input(f"Nova plantação (atual: {sensor_data[1]}): ")
            id_plantacao = int(id_plantacao_str) if id_plantacao_str else sensor_data[1]
            # Verificar se a plantação existe
            if id_plantacao_str:
                plantacao = self.plantacao_service.buscar_por_id(id_plantacao)
                if not plantacao:
                    print(f"Plantação com ID {id_plantacao} não encontrada. Mantendo a plantação atual.")
                    id_plantacao = sensor_data[1]
        except ValueError:
            print("ID inválido. Mantendo a plantação atual.")
            id_plantacao = sensor_data[1]

        nome = input(f"Novo nome (atual: {sensor_data[2]}): ") or sensor_data[2]

        data_atual_formatada = sensor_data[3].strftime('%Y-%m-%d') if sensor_data[3] else 'N/A'
        data_instalacao_str = input(f"Nova data de instalação (atual: {data_atual_formatada}, formato AAAA-MM-DD): ")

        try:
            data_instalacao = date.fromisoformat(data_instalacao_str) if data_instalacao_str else sensor_data[3]
        except ValueError:
            print("Formato de data inválido. Mantendo a data atual.")
            data_instalacao = sensor_data[3]

        sensor = Sensor(id_sensor=id, id_plantacao=id_plantacao, nome=nome, data_instalacao=data_instalacao)
        if self.sensor_service.atualizar(sensor):
            print("\nSensor atualizado com sucesso!")
        else:
            print("\nErro ao atualizar sensor.")

        self.esperar_tecla()

    def excluir_sensor(self):
        self.exibir_cabecalho("EXCLUIR SENSOR")

        try:
            id = int(input("Digite o ID do sensor a ser excluído: "))
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        sensor = self.sensor_service.buscar_por_id(id)

        if not sensor:
            print(f"Sensor com ID {id} não encontrado.")
            self.esperar_tecla()
            return

        confirmacao = input(f"Confirma a exclusão do sensor '{sensor[2]}' da plantação '{sensor[4]}'? (s/n): ")

        if confirmacao.lower() == 's':
            if self.sensor_service.excluir(id):
                print("\nSensor excluído com sucesso!")
            else:
                print("\nErro ao excluir sensor. Verifique se ele possui leituras cadastradas.")
        else:
            print("\nOperação cancelada.")

        self.esperar_tecla()