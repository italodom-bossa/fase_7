import os
import subprocess

if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm'

from db.postgres_adapter import PostgresAdapter
from entrega_2.services.dados_sensor_service import DadoSensorService
from services.plantacao_service import PlantacaoService
from services.sensor_service import SensorService
from ui.menu_principal import MenuPrincipal


def limpar_tela():
    if os.name == 'nt':
        subprocess.call('cls', shell=True)
    else:
        try:
            subprocess.call('clear', shell=True)
        except:
            print("\n" * 100)


def exibir_boas_vindas():
    limpar_tela()
    print("=" * 60)
    print("SISTEMA DE MONITORAMENTO DE SENSORES AGRÍCOLAS".center(60))
    print("Versão 1.0".center(60))
    print("=" * 60)
    print("\nIniciando o sistema...")
    input("\nPressione ENTER para continuar...")

def main():
    exibir_boas_vindas()

    try:
        db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'db_agricultura',
            'user': 'postgres',
            'password': 'postgres'
        }

        db_adapter = PostgresAdapter(**db_config)
        db_adapter.conectar()

        plantacao_service = PlantacaoService(db_adapter)
        sensor_service = SensorService(db_adapter)
        dado_sensor_service = DadoSensorService(db_adapter)

        menu_principal = MenuPrincipal(plantacao_service, sensor_service, dado_sensor_service)

        menu_principal.executar()

    except Exception as e:
        limpar_tela()
        print("=" * 60)
        print("ERRO AO INICIAR O SISTEMA".center(60))
        print("=" * 60)
        print(f"\nOcorreu um erro: {str(e)}")
        print("\nVerifique se o banco de dados está configurado corretamente.")
        print("Entre em contato com o suporte técnico para obter ajuda.")

    finally:
        if 'db_adapter' in locals() and db_adapter:
            db_adapter.desconectar()

        limpar_tela()
        print("=" * 60)
        print("SISTEMA ENCERRADO".center(60))
        print("=" * 60)
        print("\nObrigado por utilizar o Sistema de Monitoramento de Sensores!")
        print("\nDesenvolvido como parte do projeto acadêmico.")
        input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()