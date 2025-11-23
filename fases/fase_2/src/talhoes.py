from src.common.utils import gerar_id, get_repositorio

repo = get_repositorio('talhoes')

TIPOS_SOLO_VALIDOS = ["arenoso", "argiloso", "franco", "humoso", "calcário", "outro"]

def validar_nome(nome):
    if not nome or not isinstance(nome, str) or nome.strip() == '':
        raise ValueError("Nome do talhão é obrigatório e não pode estar vazio")
    if len(nome) > 100:
        raise ValueError("Nome do talhão não pode ter mais de 100 caracteres")
    return nome.strip()

def validar_localizacao(localizacao):
    if not localizacao or not isinstance(localizacao, str) or localizacao.strip() == '':
        raise ValueError("Localização é obrigatória e não pode estar vazia")
    if len(localizacao) > 200:
        raise ValueError("Localização não pode ter mais de 200 caracteres")
    return localizacao.strip()

def validar_hectares(hectares):
    if hectares is None or (isinstance(hectares, str) and hectares.strip() == ''):
        raise ValueError("Hectares é obrigatório e não pode estar vazio")
    try:
        hectares_float = float(hectares)
        if hectares_float <= 0:
            raise ValueError("Hectares deve ser um número positivo")
        return hectares_float
    except (ValueError, TypeError):
        raise ValueError("Hectares deve ser um número válido")

def validar_tipo_solo(tipo_solo):
    if not tipo_solo or not isinstance(tipo_solo, str) or tipo_solo.strip() == '':
        raise ValueError("Tipo de solo é obrigatório e não pode estar vazio")
    if tipo_solo not in TIPOS_SOLO_VALIDOS:
        raise ValueError(f"Tipo de solo inválido. Escolha uma das opções: {', '.join(TIPOS_SOLO_VALIDOS)}")
    return tipo_solo

def validar_id(id_talhao):
    if not id_talhao or not isinstance(id_talhao, str) or id_talhao.strip() == '':
        raise ValueError("ID do talhão é obrigatório e não pode estar vazio")
    return id_talhao.strip()

def obter_opcoes_tipo_solo():
    print("Tipos de solo disponíveis:")
    for i, tipo in enumerate(TIPOS_SOLO_VALIDOS, 1):
        print(f"{i}. {tipo}")
    
    while True:
        try:
            escolha = input("Escolha o número correspondente ao tipo de solo: ")
            if escolha.strip() == '':
                print("Por favor, faça uma escolha. O campo não pode estar vazio.")
                continue
                
            indice = int(escolha) - 1
            if 0 <= indice < len(TIPOS_SOLO_VALIDOS):
                return TIPOS_SOLO_VALIDOS[indice]
            else:
                print(f"Por favor, escolha um número entre 1 e {len(TIPOS_SOLO_VALIDOS)}.")
        except ValueError:
            print("Por favor, digite um número válido.")

async def cadastrar_talhao(nome, localizacao, hectares, tipo_solo=None):
    try:
        nome_validado = validar_nome(nome)
        localizacao_validada = validar_localizacao(localizacao)
        hectares_validado = validar_hectares(hectares)
        
        if tipo_solo is None:
            tipo_solo = obter_opcoes_tipo_solo()
        
        tipo_solo_validado = validar_tipo_solo(tipo_solo)
        
        talhao = {
            "id": gerar_id(),
            "nome": nome_validado,
            "localizacao": localizacao_validada,
            "hectares": hectares_validado,
            "tipo_solo": tipo_solo_validado
        }
        await repo.inserir(talhao)
        print(f"Talhão '{nome_validado}' cadastrado com sucesso! ID: {talhao['id']}")
        return True
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False

async def listar_talhoes():
    talhoes = await repo.listar()
    if not talhoes:
        print("Nenhum talhão cadastrado.")
        return

    print("Lista de Talhões:")
    for talhao in talhoes:
        print(f"ID: {talhao['id']}")
        print(f"Nome: {talhao['nome']}")
        print(f"Localização: {talhao['localizacao']}")
        print(f"Hectares: {talhao['hectares']}")
        print(f"Tipo de Solo: {talhao['tipo_solo']}")
        print("-" * 30)

async def atualizar_talhao(id_talhao, nome, localizacao, hectares, tipo_solo=None):
    try:
        id_validado = validar_id(id_talhao)
        nome_validado = validar_nome(nome)
        localizacao_validada = validar_localizacao(localizacao)
        hectares_validado = validar_hectares(hectares)
        
        if tipo_solo is None:
            tipo_solo = obter_opcoes_tipo_solo()
            
        tipo_solo_validado = validar_tipo_solo(tipo_solo)
        
        resultado = await repo.atualizar(id_validado, {
            "nome": nome_validado,
            "localizacao": localizacao_validada,
            "hectares": hectares_validado,
            "tipo_solo": tipo_solo_validado
        })

        if resultado:
            print(f"Talhão com ID '{id_validado}' atualizado com sucesso!")
            return True
        else:
            print(f"Erro: Talhão com ID '{id_validado}' não encontrado.")
            return False
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False

async def deletar_talhao(id_talhao):
    try:
        id_validado = validar_id(id_talhao)
        resultado = await repo.deletar(id_validado)
        if resultado:
            print(f"Talhão com ID '{id_validado}' removido com sucesso!")
            return True
        else:
            print(f"Erro: Talhão com ID '{id_validado}' não encontrado.")
            return False
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False