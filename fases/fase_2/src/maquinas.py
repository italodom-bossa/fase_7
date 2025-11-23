from src.common.utils import gerar_id, get_repositorio

repo = get_repositorio('maquinas')

TIPOS_MAQUINAS_VALIDOS = ["colheitadeira", "trator", "plantadeira", "pulverizador", "carregadeira", "outro"]

def validar_modelo(modelo):
    if not modelo or not isinstance(modelo, str) or modelo.strip() == '':
        raise ValueError("Modelo da máquina é obrigatório e não pode estar vazio")
    if len(modelo) > 100:
        raise ValueError("Modelo da máquina não pode ter mais de 100 caracteres")
    return modelo.strip()

def validar_ano(ano):
    if ano is None or (isinstance(ano, str) and ano.strip() == ''):
        raise ValueError("Ano da máquina é obrigatório e não pode estar vazio")
    try:
        ano_int = int(ano)
        import datetime
        ano_atual = datetime.datetime.now().year
        if ano_int < 1900 or ano_int > ano_atual + 1:
            raise ValueError(f"Ano deve estar entre 1900 e {ano_atual + 1}")
        return ano_int
    except (ValueError, TypeError):
        raise ValueError("Ano deve ser um número inteiro válido")

def validar_tipo(tipo):
    if not tipo or not isinstance(tipo, str) or tipo.strip() == '':
        raise ValueError("Tipo de máquina é obrigatório e não pode estar vazio")
    if tipo not in TIPOS_MAQUINAS_VALIDOS:
        raise ValueError(f"Tipo de máquina inválido. Escolha uma das opções: {', '.join(TIPOS_MAQUINAS_VALIDOS)}")
    return tipo

def validar_id(id_maquina):
    if not id_maquina or not isinstance(id_maquina, str) or id_maquina.strip() == '':
        raise ValueError("ID da máquina é obrigatório e não pode estar vazio")
    return id_maquina.strip()

def obter_opcoes_tipo_maquina():
    print("Tipos de máquina disponíveis:")
    for i, tipo in enumerate(TIPOS_MAQUINAS_VALIDOS, 1):
        print(f"{i}. {tipo}")
    
    while True:
        try:
            escolha = input("Escolha o número correspondente ao tipo de máquina: ")
            if escolha.strip() == '':
                print("Por favor, faça uma escolha. O campo não pode estar vazio.")
                continue
                
            indice = int(escolha) - 1
            if 0 <= indice < len(TIPOS_MAQUINAS_VALIDOS):
                return TIPOS_MAQUINAS_VALIDOS[indice]
            else:
                print(f"Por favor, escolha um número entre 1 e {len(TIPOS_MAQUINAS_VALIDOS)}.")
        except ValueError:
            print("Por favor, digite um número válido.")

async def cadastrar_maquina(modelo, ano, tipo=None):
    try:
        modelo_validado = validar_modelo(modelo)
        ano_validado = validar_ano(ano)
        
        if tipo is None:
            tipo = obter_opcoes_tipo_maquina()
            
        tipo_validado = validar_tipo(tipo)
        
        maquina = {
            "id": gerar_id(),
            "modelo": modelo_validado,
            "ano": ano_validado,
            "tipo": tipo_validado
        }
        await repo.inserir(maquina)
        print(f"Máquina '{modelo_validado}' cadastrada com sucesso! ID: {maquina['id']}")
        return True
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False

async def listar_maquinas():
    maquinas = await repo.listar()
    if not maquinas:
        print("Nenhuma máquina cadastrada.")
        return

    print("Lista de Máquinas:")
    for maquina in maquinas:
        print(f"ID: {maquina['id']}")
        print(f"Modelo: {maquina['modelo']}")
        print(f"Ano: {maquina['ano']}")
        print(f"Tipo: {maquina['tipo']}")
        print("-" * 30)

async def atualizar_maquina(id_maquina, modelo, ano, tipo=None):
    try:
        id_validado = validar_id(id_maquina)
        modelo_validado = validar_modelo(modelo)
        ano_validado = validar_ano(ano)
        
        if tipo is None:
            tipo = obter_opcoes_tipo_maquina()
            
        tipo_validado = validar_tipo(tipo)
        
        novos_dados = {
            "modelo": modelo_validado,
            "ano": ano_validado,
            "tipo": tipo_validado
        }
        resultado = await repo.atualizar(id_validado, novos_dados)

        if resultado:
            print(f"Máquina com ID '{id_validado}' atualizada com sucesso!")
            return True
        else:
            print(f"Erro: Máquina com ID '{id_validado}' não encontrada.")
            return False
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False

async def deletar_maquina(id_maquina):
    try:
        id_validado = validar_id(id_maquina)
        resultado = await repo.deletar(id_validado)
        if resultado:
            print(f"Máquina com ID '{id_validado}' removida com sucesso!")
            return True
        else:
            print(f"Erro: Máquina com ID '{id_validado}' não encontrada.")
            return False
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False