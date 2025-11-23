import os

from entrega_2.ui.menu_dados import MenuDados
from entrega_2.ui.menu_plantacao import MenuPlantacao
from entrega_2.ui.menu_sensor import MenuSensor


class MenuPrincipal:
    def __init__(self, plantacao_service, sensor_service, dado_sensor_service):
        self.plantacao_service = plantacao_service
        self.sensor_service = sensor_service
        self.dado_sensor_service = dado_sensor_service

        # Inicializar submenus
        self.menu_plantacao = MenuPlantacao(plantacao_service)
        self.menu_sensor = MenuSensor(plantacao_service, sensor_service)
        self.menu_dados = MenuDados(plantacao_service, sensor_service, dado_sensor_service)

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
            self.exibir_cabecalho("SISTEMA DE MONITORAMENTO DE SENSORES")
            print("1. Gerenciar Plantações")
            print("2. Gerenciar Sensores")
            print("3. Registrar Dados de Sensores")
            print("0. Sair")
            print()

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.menu_plantacao.executar()
            elif opcao == "2":
                self.menu_sensor.executar()
            elif opcao == "3":
                self.menu_dados.executar()
            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!")
                self.esperar_tecla()