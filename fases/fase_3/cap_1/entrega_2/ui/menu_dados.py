import os
from datetime import datetime

from entrega_2.models.dados_sensor import DadoSensor


class MenuDados:
    def __init__(self, plantacao_service, sensor_service, dado_sensor_service):
        self.plantacao_service = plantacao_service
        self.sensor_service = sensor_service
        self.dado_service = dado_sensor_service

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
            self.exibir_cabecalho("GERENCIAMENTO DE DADOS DE SENSORES")
            print("1. Cadastrar Nova Leitura")
            print("2. Listar Todas as Leituras")
            print("3. Listar Leituras por Sensor")
            print("4. Listar Leituras por Plantação")
            print("5. Buscar Leitura")
            print("6. Editar Leitura")
            print("7. Excluir Leitura")
            print("0. Voltar")
            print()

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_dado_sensor()
            elif opcao == "2":
                self.listar_dados_sensores()
            elif opcao == "3":
                self.listar_dados_por_sensor()
            elif opcao == "4":
                self.listar_dados_por_plantacao()
            elif opcao == "5":
                self.buscar_dado_sensor()
            elif opcao == "6":
                self.editar_dado_sensor()
            elif opcao == "7":
                self.excluir_dado_sensor()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                self.esperar_tecla()

    def cadastrar_dado_sensor(self):
        self.exibir_cabecalho("CADASTRAR LEITURA DE SENSOR")

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

        # Listar sensores da plantação selecionada
        sensores = self.sensor_service.listar_por_plantacao(id_plantacao)

        if not sensores:
            print(f"Não existem sensores cadastrados para a plantação '{plantacao[1]}'. Cadastre um sensor primeiro.")
            self.esperar_tecla()
            return

        print(f"\nSensores disponíveis para a plantação '{plantacao[1]}':")
        for s in sensores:
            print(f"{s[0]}: {s[2]}")

        try:
            id_sensor = int(input("\nID do sensor: "))
            # Verificar se o sensor existe e pertence à plantação selecionada
            sensor_encontrado = False
            for s in sensores:
                if s[0] == id_sensor:
                    sensor_encontrado = True
                    break

            if not sensor_encontrado:
                print(f"Sensor com ID {id_sensor} não encontrado na plantação selecionada.")
                self.esperar_tecla()
                return
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        # Solicitar valor da leitura
        try:
            valor_sensor = float(input("Valor da leitura: "))
        except ValueError:
            print("Valor inválido. Usando 0.0")
            valor_sensor = 0.0

        data_hora_str = input("Data e hora da leitura (AAAA-MM-DD HH:MM:SS, pressione ENTER para usar a atual): ")
        try:
            data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S') if data_hora_str else datetime.now()
        except ValueError:
            print("Formato de data e hora inválido. Usando a data e hora atual.")
            data_hora = datetime.now()

        dado_sensor = DadoSensor(id_sensor=id_sensor, data_hora_leitura=data_hora, valor_sensor=valor_sensor)
        if self.dado_service.cadastrar(dado_sensor):
            print("\nLeitura do sensor cadastrada com sucesso!")
        else:
            print("\nErro ao cadastrar leitura do sensor.")

        self.esperar_tecla()

    def listar_dados_sensores(self):
        self.exibir_cabecalho("LISTA DE LEITURAS DE SENSORES")

        dados = self.dado_service.listar_todos()

        if not dados:
            print("Nenhuma leitura de sensor cadastrada.")
        else:
            print(f"{'ID':<5} | {'Sensor':<20} | {'Plantação':<20} | {'Data e Hora':<20} | {'Valor':<10}")
            print("-" * 80)

            for d in dados:
                data_formatada = d[2].strftime('%d/%m/%Y %H:%M') if d[2] else 'N/A'
                print(f"{d[0]:<5} | {d[4]:<20} | {d[5]:<20} | {data_formatada:<20} | {d[3]:<10.2f}")

        self.esperar_tecla()

    def listar_dados_por_sensor(self):
        self.exibir_cabecalho("LISTAR LEITURAS POR SENSOR")

        # Listar todos os sensores
        sensores = self.sensor_service.listar_todos()

        if not sensores:
            print("Não existem sensores cadastrados.")
            self.esperar_tecla()
            return

        print("Sensores disponíveis:")
        for s in sensores:
            print(f"{s[0]}: {s[2]} (Plantação: {s[4]})")

        try:
            id_sensor = int(input("\nID do sensor: "))
            # Verificar se o sensor existe
            sensor = self.sensor_service.buscar_por_id(id_sensor)
            if not sensor:
                print(f"Sensor com ID {id_sensor} não encontrado.")
                self.esperar_tecla()
                return
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return

        dados = self.dado_service.listar_por_sensor(id_sensor)

        if not dados:
            print(f"Nenhuma leitura cadastrada para o sensor '{sensor[2]}'.")
        else:
            print(f"\nLeituras do sensor '{sensor[2]}' da plantação '{sensor[4]}':")
            print(f"{'ID':<5} | {'Data e Hora':<20} | {'Valor':<10}")
            print("-" * 40)

            for d in dados:
                data_formatada = d[2].strftime('%d/%m/%Y %H:%M') if d[2] else 'N/A'
                print(f"{d[0]:<5} | {data_formatada:<20} | {d[3]:<10.2f}")

        self.esperar_tecla()

    def listar_dados_por_plantacao(self):
        self.exibir_cabecalho("LISTAR LEITURAS POR PLANTAÇÃO")

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

        dados = self.dado_service.listar_por_plantacao(id_plantacao)

        if not dados:
            print(f"Nenhuma leitura cadastrada para a plantação '{plantacao[1]}'.")
        else:
            print(f"\nLeituras da plantação '{plantacao[1]}':")
            print(f"{'ID':<5} | {'Sensor':<20} | {'Data e Hora':<20} | {'Valor':<10}")
            print("-" * 60)

            for d in dados:
                data_formatada = d[2].strftime('%d/%m/%Y %H:%M') if d[2] else 'N/A'
                print(f"{d[0]:<5} | {d[4]:<20} | {data_formatada:<20} | {d[3]:<10.2f}")
        
        self.esperar_tecla()
    
    def buscar_dado_sensor(self):
        self.exibir_cabecalho("BUSCAR LEITURA DE SENSOR")
        
        try:
            id = int(input("Digite o ID da leitura: "))
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return
        
        dado = self.dado_service.buscar_por_id(id)
        
        if not dado:
            print(f"Leitura com ID {id} não encontrada.")
        else:
            print(f"\nID: {dado[0]}")
            print(f"Sensor: {dado[4]} (ID: {dado[1]})")
            print(f"Plantação: {dado[5]}")
            data_formatada = dado[2].strftime('%d/%m/%Y %H:%M:%S') if dado[2] else 'N/A'
            print(f"Data e Hora: {data_formatada}")
            print(f"Valor: {dado[3]}")
        
        self.esperar_tecla()
    
    def editar_dado_sensor(self):
        self.exibir_cabecalho("EDITAR LEITURA DE SENSOR")
        
        try:
            id = int(input("Digite o ID da leitura: "))
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return
        
        dado_data = self.dado_service.buscar_por_id(id)
        
        if not dado_data:
            print(f"Leitura com ID {id} não encontrada.")
            self.esperar_tecla()
            return
        
        print(f"\nEditando leitura ID {dado_data[0]} do sensor '{dado_data[4]}' da plantação '{dado_data[5]}'")
        
        try:
            valor_str = input(f"Novo valor (atual: {dado_data[3]}): ")
            valor = float(valor_str) if valor_str else dado_data[3]
        except ValueError:
            print("Valor inválido. Mantendo o valor atual.")
            valor = dado_data[3]
        
        data_atual_formatada = dado_data[2].strftime('%Y-%m-%d %H:%M:%S') if dado_data[2] else 'N/A'
        data_hora_str = input(f"Nova data e hora (atual: {data_atual_formatada}, formato AAAA-MM-DD HH:MM:SS): ")
        
        try:
            data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S') if data_hora_str else dado_data[2]
        except ValueError:
            print("Formato de data e hora inválido. Mantendo a data e hora atual.")
            data_hora = dado_data[2]
        
        dado_sensor = DadoSensor(
            id_dado_sensor=id,
            id_sensor=dado_data[1],
            data_hora_leitura=data_hora,
            valor_sensor=valor
        )
        
        if self.dado_service.atualizar(dado_sensor):
            print("\nLeitura atualizada com sucesso!")
        else:
            print("\nErro ao atualizar leitura.")
        
        self.esperar_tecla()
    
    def excluir_dado_sensor(self):
        self.exibir_cabecalho("EXCLUIR LEITURA DE SENSOR")
        
        try:
            id = int(input("Digite o ID da leitura a ser excluída: "))
        except ValueError:
            print("ID inválido.")
            self.esperar_tecla()
            return
        
        dado = self.dado_service.buscar_por_id(id)
        
        if not dado:
            print(f"Leitura com ID {id} não encontrada.")
            self.esperar_tecla()
            return
        
        data_formatada = dado[2].strftime('%d/%m/%Y %H:%M:%S') if dado[2] else 'N/A'
        confirmacao = input(f"Confirma a exclusão da leitura ID {dado[0]} do sensor '{dado[4]}' em {data_formatada}? (s/n): ")
        
        if confirmacao.lower() == 's':
            if self.dado_service.excluir(id):
                print("\nLeitura excluída com sucesso!")
            else:
                print("\nErro ao excluir leitura.")
        else:
            print("\nOperação cancelada.")
        
        self.esperar_tecla()