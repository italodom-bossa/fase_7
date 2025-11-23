from src.common.utils import gerar_id, get_repositorio
from datetime import datetime

repo = get_repositorio('colheitas')

TIPOS_COLHEITA_VALIDOS = ["manual", "mecanica", "mista"]
SEVERIDADES_VALIDAS = ["baixa", "media", "alta", "crítica"]

def validar_id(id_):
    if not id_ or not isinstance(id_, str) or id_.strip() == '':
        raise ValueError("ID é obrigatório e não pode estar vazio")
    return id_.strip()

def validar_quantidade(quantidade):
    if quantidade is None:
        raise ValueError("Quantidade colhida é obrigatória e não pode estar vazia")
    try:
        quantidade_float = float(quantidade)
        if quantidade_float <= 0:
            raise ValueError("Quantidade colhida deve ser um número positivo")
        return quantidade_float
    except (ValueError, TypeError):
        raise ValueError("Quantidade colhida deve ser um número válido")

def validar_perda_real(perda_real, quantidade_colhida):
    if perda_real is None:
        return None
    try:
        perda_float = float(perda_real)
        if perda_float < 0:
            raise ValueError("Perda real não pode ser negativa")
        if perda_float > quantidade_colhida:
            raise ValueError("Perda real não pode ser maior que a quantidade colhida")
        return perda_float
    except (ValueError, TypeError):
        raise ValueError("Perda real deve ser um número válido")

def validar_tipo_colheita(tipo_colheita):
    if not tipo_colheita or not isinstance(tipo_colheita, str) or tipo_colheita.strip() == '':
        raise ValueError("Tipo de colheita é obrigatório e não pode estar vazio")
    tipo_lower = tipo_colheita.lower().strip()
    if tipo_lower not in TIPOS_COLHEITA_VALIDOS:
        raise ValueError(f"Tipo de colheita inválido. Escolha entre: {', '.join(TIPOS_COLHEITA_VALIDOS)}")
    return tipo_lower

def validar_causa_perda(causa_perda):
    if causa_perda is None:
        return ""
    return causa_perda.strip()

def validar_severidade(severidade):
    if not severidade:
        return ""
    severidade_lower = severidade.lower().strip()
    if severidade_lower and severidade_lower not in SEVERIDADES_VALIDAS:
        raise ValueError(f"Severidade inválida. Escolha entre: {', '.join(SEVERIDADES_VALIDAS)}")
    return severidade_lower

def validar_condicoes(condicoes):
    if not condicoes:
        return {}
    if not isinstance(condicoes, dict):
        raise ValueError("Condições deve ser um dicionário")
    return condicoes

def validar_data(data):
    if not data or not isinstance(data, str) or data.strip() == '':
        return datetime.now().strftime("%Y-%m-%d")
    
    try:
        datetime.strptime(data.strip(), "%Y-%m-%d")
        return data.strip()
    except ValueError:
        raise ValueError("Data inválida. Use o formato YYYY-MM-DD")

def calcular_perda_estimada(tipo_colheita: str, quantidade: float) -> float:
    tipo_lower = tipo_colheita.lower()
    if tipo_lower == "manual":
        return round(quantidade * 0.05, 2)
    elif tipo_lower == "mecanica":
        return round(quantidade * 0.15, 2)
    elif tipo_lower == "mista":
        return round(quantidade * 0.10, 2)
    else:
        return 0.0

def obter_opcao_tipo_colheita():
    print("\n--- Tipo de Colheita ---")
    for i, tipo in enumerate(TIPOS_COLHEITA_VALIDOS, 1):
        print(f"{i}. {tipo}")
    
    while True:
        try:
            escolha = input("Escolha o tipo de colheita: ")
            if escolha.strip() == '':
                print("Por favor, faça uma escolha. O campo não pode estar vazio.")
                continue
                
            indice = int(escolha) - 1
            if 0 <= indice < len(TIPOS_COLHEITA_VALIDOS):
                return TIPOS_COLHEITA_VALIDOS[indice]
            else:
                print(f"Por favor, escolha um número entre 1 e {len(TIPOS_COLHEITA_VALIDOS)}.")
        except ValueError:
            print("Por favor, digite um número válido.")

def obter_opcao_severidade():
    print("\n--- Severidade da Perda ---")
    for i, severidade in enumerate(SEVERIDADES_VALIDAS, 1):
        print(f"{i}. {severidade}")
    print("0. Não informar")
    
    while True:
        try:
            escolha = input("Escolha a severidade da perda: ")
            if escolha.strip() == '':
                print("Por favor, faça uma escolha. Digite 0 para não informar.")
                continue
                
            indice = int(escolha)
            if indice == 0:
                return ""
            indice -= 1
            if 0 <= indice < len(SEVERIDADES_VALIDAS):
                return SEVERIDADES_VALIDAS[indice]
            else:
                print(f"Por favor, escolha um número entre 0 e {len(SEVERIDADES_VALIDAS)}.")
        except ValueError:
            print("Por favor, digite um número válido.")

async def selecionar_talhao():
    repo_talhoes = get_repositorio('talhoes')
    talhoes = await repo_talhoes.listar()

    if not talhoes or len(talhoes) == 0:
        print("Não há talhões cadastrados. Por favor, cadastre um talhão primeiro.")
        return None

    print("\n--- Selecione um Talhão ---")
    for i, talhao in enumerate(talhoes, 1):
        print(f"{i}. {talhao['nome']} - {talhao['localizacao']} ({talhao['hectares']} ha)")

    while True:
        try:
            escolha = input("\nDigite o número do talhão: ")
            if escolha.strip() == '':
                print("Por favor, faça uma escolha. O campo não pode estar vazio.")
                continue
                
            indice = int(escolha) - 1
            if 0 <= indice < len(talhoes):
                return talhoes[indice]['id']
            else:
                print(f"Por favor, escolha um número entre 1 e {len(talhoes)}.")
        except ValueError:
            print("Por favor, digite um número válido.")

async def selecionar_operador():
    repo_operadores = get_repositorio('operadores')
    operadores = await repo_operadores.listar()

    if not operadores or len(operadores) == 0:
        print("Não há operadores cadastrados. Por favor, cadastre um operador primeiro.")
        return None

    print("\n--- Selecione um Operador ---")
    for i, operador in enumerate(operadores, 1):
        print(f"{i}. {operador['nome']} - Turno: {operador['turno']}")

    while True:
        try:
            escolha = input("\nDigite o número do operador: ")
            if escolha.strip() == '':
                print("Por favor, faça uma escolha. O campo não pode estar vazio.")
                continue
                
            indice = int(escolha) - 1
            if 0 <= indice < len(operadores):
                return operadores[indice]['id']
            else:
                print(f"Por favor, escolha um número entre 1 e {len(operadores)}.")
        except ValueError:
            print("Por favor, digite um número válido.")

async def selecionar_maquina():
    repo_maquinas = get_repositorio('maquinas')
    maquinas = await repo_maquinas.listar()

    if not maquinas or len(maquinas) == 0:
        print("Não há máquinas cadastradas. Por favor, cadastre uma máquina primeiro.")
        return None

    print("\n--- Selecione uma Máquina ---")
    for i, maquina in enumerate(maquinas, 1):
        print(f"{i}. {maquina['modelo']} ({maquina['ano']}) - Tipo: {maquina['tipo']}")

    while True:
        try:
            escolha = input("\nDigite o número da máquina: ")
            if escolha.strip() == '':
                print("Por favor, faça uma escolha. O campo não pode estar vazio.")
                continue
                
            indice = int(escolha) - 1
            if 0 <= indice < len(maquinas):
                return maquinas[indice]['id']
            else:
                print(f"Por favor, escolha um número entre 1 e {len(maquinas)}.")
        except ValueError:
            print("Por favor, digite um número válido.")

async def registrar_colheita(
        talhao_id,
        operador_id,
        maquina_id,
        tipo_colheita,
        quantidade_colhida,
        perda_real=None,
        causa_perda="",
        severidade="",
        condicoes=None,
        data=None
):
    try:
        talhao_id_validado = validar_id(talhao_id)
        operador_id_validado = validar_id(operador_id)
        maquina_id_validado = validar_id(maquina_id)
        
        tipo_colheita_validado = validar_tipo_colheita(tipo_colheita)
        quantidade_validada = validar_quantidade(quantidade_colhida)
        perda_real_validada = validar_perda_real(perda_real, quantidade_validada)
        causa_perda_validada = validar_causa_perda(causa_perda)
        severidade_validada = validar_severidade(severidade)
        condicoes_validadas = validar_condicoes(condicoes)
        data_validada = validar_data(data)
        
        perda_estimada = calcular_perda_estimada(tipo_colheita_validado, quantidade_validada)
        
        colheita = {
            "id": gerar_id(),
            "talhao_id": talhao_id_validado,
            "operador_id": operador_id_validado,
            "maquina_id": maquina_id_validado,
            "tipo_colheita": tipo_colheita_validado,
            "quantidade_colhida": quantidade_validada,
            "perda_estimada": perda_estimada,
            "perda_real": perda_real_validada,
            "causa_perda": causa_perda_validada,
            "severidade": severidade_validada,
            "condicoes": condicoes_validadas,
            "data": data_validada
        }

        await repo.inserir(colheita)
        print(f"Colheita registrada com sucesso! ID: {colheita['id']}")
        return colheita
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return None

async def listar_colheitas():
    colheitas = await repo.listar()
    if not colheitas:
        print("Não há colheitas registradas.")
    else:
        print("\n--- Lista de Colheitas ---")
        for colheita in colheitas:
            print(f"ID: {colheita['id']}")
            print(f"Talhão: {colheita['talhao_id']}")
            print(f"Operador: {colheita['operador_id']}")
            print(f"Máquina: {colheita['maquina_id']}")
            print(f"Tipo: {colheita['tipo_colheita']}")
            print(f"Quantidade: {colheita['quantidade_colhida']} t")
            print(f"Perda Estimada: {colheita['perda_estimada']} t")
            print(f"Perda Real: {colheita.get('perda_real', 'Não informada')} t")
            print(f"Causa: {colheita.get('causa_perda', 'Não informada')}")
            print(f"Severidade: {colheita.get('severidade', 'Não informada')}")
            print(f"Data: {colheita.get('data', 'Não informada')}")
            print("-----------------------")
    return colheitas

async def atualizar_colheita(id_colheita, novos_dados):
    try:
        id_validado = validar_id(id_colheita)
        
        colheita_atual = await repo.buscar(id_validado)
        if not colheita_atual:
            print(f"Colheita com ID '{id_validado}' não encontrada.")
            return False
        
        dados_validados = {}
        
        if 'tipo_colheita' in novos_dados:
            dados_validados['tipo_colheita'] = validar_tipo_colheita(novos_dados['tipo_colheita'])
            
        if 'quantidade_colhida' in novos_dados:
            dados_validados['quantidade_colhida'] = validar_quantidade(novos_dados['quantidade_colhida'])
            dados_validados['perda_estimada'] = calcular_perda_estimada(
                dados_validados.get('tipo_colheita', colheita_atual['tipo_colheita']),
                dados_validados['quantidade_colhida']
            )
            
        if 'perda_real' in novos_dados:
            quantidade = dados_validados.get('quantidade_colhida', colheita_atual['quantidade_colhida'])
            dados_validados['perda_real'] = validar_perda_real(novos_dados['perda_real'], quantidade)
            
        if 'causa_perda' in novos_dados:
            dados_validados['causa_perda'] = validar_causa_perda(novos_dados['causa_perda'])
            
        if 'severidade' in novos_dados:
            dados_validados['severidade'] = validar_severidade(novos_dados['severidade'])
            
        if 'condicoes' in novos_dados:
            dados_validados['condicoes'] = validar_condicoes(novos_dados['condicoes'])
            
        if 'data' in novos_dados:
            dados_validados['data'] = validar_data(novos_dados['data'])
        
        resultado = await repo.atualizar(id_validado, dados_validados)
        if resultado:
            print(f"Colheita com ID '{id_validado}' atualizada com sucesso!")
            return True
        else:
            print(f"Erro ao atualizar colheita com ID '{id_validado}'.")
            return False
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False

async def deletar_colheita(id_colheita):
    try:
        id_validado = validar_id(id_colheita)
        resultado = await repo.deletar(id_validado)
        if resultado:
            print(f"Colheita com ID '{id_validado}' removida com sucesso!")
            return True
        else:
            print(f"Erro: Colheita com ID '{id_validado}' não encontrada.")
            return False
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        return False