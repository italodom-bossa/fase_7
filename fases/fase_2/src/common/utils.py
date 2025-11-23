import uuid

from src.persistencia.adapters.oracle_repository import OracleRepository

CONNECTION_STRING = "dev/dev123@localhost:1521/freepdb1"

_REPOSITORIOS = {
    "talhoes": OracleRepository(CONNECTION_STRING, "talhoes"),
    "maquinas": OracleRepository(CONNECTION_STRING, "maquinas"),
    "operadores": OracleRepository(CONNECTION_STRING, "operadores"),
    "colheitas": OracleRepository(CONNECTION_STRING, "colheitas")
}

def get_repositorio(nome: str):
    repo = _REPOSITORIOS.get(nome)
    if not repo:
        raise Exception(f"Repositório '{nome}' não encontrado.")
    return repo

def gerar_id():
    return str(uuid.uuid4())

def obter_entrada_nao_vazia(mensagem, erro_mensagem="Este campo não pode estar vazio."):
    while True:
        valor = input(mensagem)
        if valor.strip():
            return valor
        print(erro_mensagem)

def obter_numero_positivo(mensagem, erro_mensagem="Deve ser um número positivo."):
    while True:
        try:
            valor = input(mensagem)
            if not valor.strip():
                print("Este campo não pode estar vazio.")
                continue

            numero = float(valor)
            if numero <= 0:
                print(erro_mensagem)
                continue

            return numero
        except ValueError:
            print("Por favor, digite um número válido.")