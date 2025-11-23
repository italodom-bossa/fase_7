from src.common.utils import gerar_id, get_repositorio

repo = get_repositorio('operadores')

TURNOS_VALIDOS = ["diurno", "noturno", "integral", "manhã", "tarde"]

def validar_nome(nome):
    if not nome or not isinstance(nome, str) or nome.strip() == '':
        raise ValueError("Nome do operador é obrigatório e não pode estar vazio")
    if len(nome) > 100:
        raise ValueError("Nome do operador não pode ter mais de 100 caracteres")
    return nome.strip()

def validar_turno(turno):
    if not turno or not isinstance(turno, str) or turno.strip() == '':
        raise ValueError("Turno é obrigatório e não pode estar vazio")
    turno_lower = turno.lower().strip()
    if turno_lower not in TURNOS_VALIDOS:
        raise ValueError(f"Turno inválido. Escolha uma das opções: {', '.join(TURNOS_VALIDOS)}")
    return turno_lower

def validar_id(id_operador):
    if not id_operador or not isinstance(id_operador, str) or id_operador.strip() == '':
        raise ValueError("ID do operador é obrigatório e não pode estar vazio")
    return id_operador.strip()

def obter_opcoes_turno():
    print("Turnos disponíveis:")
    for i, turno in enumerate(TURNOS_VALIDOS, 1):
        print(f"{i}. {turno}")
    
    while True:
        try:
            escolha = input("Escolha o número correspondente ao turno: ")
            if escolha.strip() == '':
                print("Por favor, faça uma escolha. O campo não pode estar vazio.")
                continue
                
            indice = int(escolha) - 1
            if 0 <= indice < len(TURNOS_VALIDOS):
                return TURNOS_VALIDOS[indice]
            else:
                print(f"Por favor, escolha um número entre 1 e {len(TURNOS_VALIDOS)}.")
        except ValueError:
            print("Por favor, digite um número válido.")

async def cadastrar_operador(nome, turno=None):
    try:
        nome_validado = validar_nome(nome)
        
        if turno is None:
            turno = obter_opcoes_turno()
            
        turno_validado = validar_turno(turno)
        
        operador = {
            "id": gerar_id(),
            "nome": nome_validado,
            "turno": turno_validado
        }
        await repo.inserir(operador)
        print(f"Operador '{nome_validado}' cadastrado com sucesso! ID: {operador['id']}")
        return True
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False

async def listar_operadores():
    operadores = await repo.listar()
    if not operadores:
        print("Nenhum operador cadastrado.")
        return

    print("Lista de Operadores:")
    for operador in operadores:
        print(f"ID: {operador['id']}")
        print(f"Nome: {operador['nome']}")
        print(f"Turno: {operador['turno']}")
        print("-" * 30)

async def atualizar_operador(id_operador, nome, turno=None):
    try:
        id_validado = validar_id(id_operador)
        nome_validado = validar_nome(nome)
        
        if turno is None:
            turno = obter_opcoes_turno()
            
        turno_validado = validar_turno(turno)
        
        novos_dados = {
            "nome": nome_validado,
            "turno": turno_validado
        }
        resultado = await repo.atualizar(id_validado, novos_dados)

        if resultado:
            print(f"Operador com ID '{id_validado}' atualizado com sucesso!")
            return True
        else:
            print(f"Erro: Operador com ID '{id_validado}' não encontrado.")
            return False
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False

async def deletar_operador(id_operador):
    try:
        id_validado = validar_id(id_operador)
        resultado = await repo.deletar(id_validado)
        if resultado:
            print(f"Operador com ID '{id_validado}' removido com sucesso!")
            return True
        else:
            print(f"Erro: Operador com ID '{id_validado}' não encontrado.")
            return False
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False