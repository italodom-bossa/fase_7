"""
Serviços da Fase 3 - IoT e Sensores
FarmTech Solutions
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pandas as pd
from .database import DatabaseManager, DB_FASE3, init_fase3_db


class LeituraSensor:
    """Representa uma leitura de sensor"""

    def __init__(
        self,
        sensor_id: str,
        tipo_sensor: str,
        valor: float,
        unidade: str,
        timestamp: str = None
    ):
        self.sensor_id = sensor_id
        self.tipo_sensor = tipo_sensor
        self.valor = valor
        self.unidade = unidade
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            "Sensor": self.sensor_id,
            "Tipo": self.tipo_sensor,
            "Valor": f"{self.valor:.2f}",
            "Unidade": self.unidade,
            "Timestamp": self.timestamp
        }


class Sensor:
    """Representa um sensor IoT"""

    def __init__(
        self,
        sensor_id: str,
        tipo: str,
        unidade: str,
        min_valor: float,
        max_valor: float,
        min_ideal: float = None,
        max_ideal: float = None
    ):
        self.sensor_id = sensor_id
        self.tipo = tipo
        self.unidade = unidade
        self.min_valor = min_valor
        self.max_valor = max_valor
        self.min_ideal = min_ideal or min_valor
        self.max_ideal = max_ideal or max_valor
        self.leituras: List[LeituraSensor] = []

    def adicionar_leitura(self, valor: float, timestamp: str = None) -> LeituraSensor:
        """Adiciona nova leitura"""
        leitura = LeituraSensor(
            sensor_id=self.sensor_id,
            tipo_sensor=self.tipo,
            valor=valor,
            unidade=self.unidade,
            timestamp=timestamp
        )
        self.leituras.append(leitura)
        return leitura

    def ultima_leitura(self) -> float:
        """Retorna o valor da última leitura"""
        if self.leituras:
            return self.leituras[-1].valor
        return 0.0

    def valor_medio(self) -> float:
        """Calcula média de leituras"""
        if not self.leituras:
            return 0.0
        return sum(l.valor for l in self.leituras) / len(self.leituras)

    def esta_ideal(self) -> bool:
        """Verifica se está na faixa ideal"""
        valor = self.ultima_leitura()
        return self.min_ideal <= valor <= self.max_ideal

    def status(self) -> str:
        """Retorna status do sensor"""
        valor = self.ultima_leitura()
        if valor < self.min_ideal:
            return "⚠️ Baixo"
        elif valor > self.max_ideal:
            return "⚠️ Alto"
        else:
            return "✅ Ok"


class SistemaIrrigacao:
    """Controla o sistema de irrigação automática"""

    def __init__(self):
        self.ativo = False
        self.historico_acionamentos: List[Dict] = []

    def verificar_condicoes(
        self,
        umidade: float,
        ph: float,
        nutrientes_presentes: bool
    ) -> Tuple[bool, str]:
        """
        Verifica se devem acionar a irrigação
        Critérios:
        - Umidade < 40%
        - pH entre 5.5 e 7.5
        - Nutrientes presentes
        """
        condicoes = []

        if umidade < 40:
            condicoes.append("✅ Umidade baixa")
        else:
            condicoes.append("❌ Umidade ok")

        if 5.5 <= ph <= 7.5:
            condicoes.append("✅ pH ideal")
        else:
            condicoes.append("❌ pH fora do ideal")

        if nutrientes_presentes:
            condicoes.append("✅ Nutrientes presentes")
        else:
            condicoes.append("❌ Nutrientes ausentes")

        # Aciona se todas as condições forem atendidas
        ativar = umidade < 40 and (5.5 <= ph <= 7.5) and nutrientes_presentes

        mensagem = " | ".join(condicoes)
        return ativar, mensagem

    def acionar(self, motivo: str):
        """Registra acionamento"""
        self.ativo = True
        acionamento = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "motivo": motivo,
            "duracao_estimada": "15 minutos"
        }
        self.historico_acionamentos.append(acionamento)

    def desativar(self):
        """Desativa irrigação"""
        self.ativo = False

    def ultima_irrigacao(self) -> str:
        """Retorna informação da última irrigação"""
        if self.historico_acionamentos:
            ultima = self.historico_acionamentos[-1]
            # Suporta ambos os formatos: do banco (Timestamp) e em memória (timestamp)
            return ultima.get("timestamp") or ultima.get("Timestamp", "Nunca")
        return "Nunca"


def gerar_dados_exemplo_sensores() -> Dict[str, Sensor]:
    """Gera sensores de exemplo com leituras"""

    sensores = {
        "DHT22_01": Sensor(
            sensor_id="DHT22_01",
            tipo="Umidade/Temperatura",
            unidade="%/°C",
            min_valor=0,
            max_valor=100,
            min_ideal=40,
            max_ideal=80
        ),
        "LDR_01": Sensor(
            sensor_id="LDR_01",
            tipo="pH (LDR)",
            unidade="pH",
            min_valor=3,
            max_valor=9,
            min_ideal=5.5,
            max_ideal=7.5
        ),
        "BTN_FOSFORO": Sensor(
            sensor_id="BTN_FOSFORO",
            tipo="Fósforo",
            unidade="Presente/Ausente",
            min_valor=0,
            max_valor=1,
            min_ideal=1,
            max_ideal=1
        ),
        "BTN_POTASSIO": Sensor(
            sensor_id="BTN_POTASSIO",
            tipo="Potássio",
            unidade="Presente/Ausente",
            min_valor=0,
            max_valor=1,
            min_ideal=1,
            max_ideal=1
        ),
    }

    # Adicionar leituras de exemplo
    base_time = datetime.now()
    for i in range(24):
        tempo = (base_time - timedelta(hours=24-i)).strftime("%Y-%m-%d %H:%M:%S")

        # DHT22 - Umidade variando de 25 a 75%
        umidade = 50 + random.uniform(-25, 25)
        sensores["DHT22_01"].adicionar_leitura(umidade, tempo)

        # LDR - pH variando de 5.8 a 7.2
        ph = 6.5 + random.uniform(-0.7, 0.7)
        sensores["LDR_01"].adicionar_leitura(ph, tempo)

        # Nutrientes (simulado como botões)
        sensores["BTN_FOSFORO"].adicionar_leitura(1.0, tempo)
        sensores["BTN_POTASSIO"].adicionar_leitura(1.0 if i % 2 == 0 else 0.0, tempo)

    return sensores


def gerar_alertas_sensores(sensores: Dict[str, Sensor]) -> List[Dict]:
    """Gera lista de alertas baseado no status dos sensores"""

    alertas = []

    # Verificar umidade
    umidade_leitura = sensores["DHT22_01"].ultima_leitura()
    if umidade_leitura < 40:
        alertas.append({
            "tipo": "UMIDADE_BAIXA",
            "titulo": "🚨 Umidade Baixa",
            "mensagem": f"Umidade em {umidade_leitura:.1f}% (crítico < 40%)",
            "severidade": "crítico"
        })

    # Verificar pH
    ph_leitura = sensores["LDR_01"].ultima_leitura()
    if ph_leitura < 5.5 or ph_leitura > 7.5:
        alertas.append({
            "tipo": "PH_ANORMAL",
            "titulo": "⚠️ pH Fora do Ideal",
            "mensagem": f"pH em {ph_leitura:.2f} (faixa ideal: 5.5-7.5)",
            "severidade": "alto"
        })

    # Verificar nutrientes
    fosforo = sensores["BTN_FOSFORO"].ultima_leitura() == 1
    potassio = sensores["BTN_POTASSIO"].ultima_leitura() == 1

    if not fosforo or not potassio:
        nutrientes_faltando = []
        if not fosforo:
            nutrientes_faltando.append("Fósforo")
        if not potassio:
            nutrientes_faltando.append("Potássio")

        alertas.append({
            "tipo": "NUTRIENTES_AUSENTES",
            "titulo": "⚠️ Nutrientes Ausentes",
            "mensagem": f"Faltando: {', '.join(nutrientes_faltando)}",
            "severidade": "médio"
        })

    return alertas


def calcular_historico_resumido(sensores: Dict[str, Sensor], horas: int = 24) -> pd.DataFrame:
    """Calcula resumo do histórico dos últimos N horas"""

    dados = []

    for sensor_id, sensor in sensores.items():
        if sensor.leituras:
            leituras_recentes = sensor.leituras[-horas:]
            valores = [l.valor for l in leituras_recentes]

            dados.append({
                "Sensor": sensor_id,
                "Tipo": sensor.tipo,
                "Última": f"{sensor.ultima_leitura():.2f} {sensor.unidade}",
                "Média": f"{sensor.valor_medio():.2f} {sensor.unidade}",
                "Min": f"{min(valores):.2f}",
                "Max": f"{max(valores):.2f}",
                "Status": sensor.status()
            })

    return pd.DataFrame(dados)


# ===== FUNÇÕES DE BANCO DE DADOS =====

def salvar_leitura_sensor(leitura: LeituraSensor, status: str = "Normal") -> bool:
    """Salva uma leitura de sensor no banco de dados"""
    try:
        db = DatabaseManager(DB_FASE3)
        db.execute("""
            INSERT INTO leituras_sensores (
                sensor_id, tipo_sensor, valor, unidade, timestamp, status
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            leitura.sensor_id,
            leitura.tipo_sensor,
            leitura.valor,
            leitura.unidade,
            leitura.timestamp,
            status
        ))
        db.close()
        return True
    except Exception as e:
        print(f"Erro ao salvar leitura: {e}")
        return False


def carregar_leituras_sensor(sensor_id: str, limite: int = 100) -> List[LeituraSensor]:
    """Carrega leituras de um sensor específico"""
    try:
        db = DatabaseManager(DB_FASE3)
        rows = db.fetchall("""
            SELECT * FROM leituras_sensores
            WHERE sensor_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (sensor_id, limite))

        leituras = []
        for row in rows:
            leitura = LeituraSensor(
                sensor_id=row['sensor_id'],
                tipo_sensor=row['tipo_sensor'],
                valor=row['valor'],
                unidade=row['unidade'],
                timestamp=row['timestamp']
            )
            leituras.append(leitura)

        db.close()
        return list(reversed(leituras))  # Ordem cronológica
    except Exception as e:
        print(f"Erro ao carregar leituras: {e}")
        return []


def salvar_irrigacao(timestamp: str, motivo: str, duracao_minutos: int = None) -> bool:
    """Salva um registro de irrigação"""
    try:
        db = DatabaseManager(DB_FASE3)
        db.execute("""
            INSERT INTO historico_irrigacao (timestamp, motivo, duracao_minutos)
            VALUES (?, ?, ?)
        """, (timestamp, motivo, duracao_minutos))
        db.close()
        return True
    except Exception as e:
        print(f"Erro ao salvar irrigação: {e}")
        return False


def carregar_historico_irrigacao(limite: int = 50) -> List[Dict]:
    """Carrega histórico de irrigações"""
    try:
        db = DatabaseManager(DB_FASE3)
        rows = db.fetchall("""
            SELECT * FROM historico_irrigacao
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limite,))

        historico = []
        for row in rows:
            historico.append({
                "Timestamp": row['timestamp'],
                "Motivo": row['motivo'],
                "Duração (min)": row['duracao_minutos'] or "-"
            })

        db.close()
        return historico
    except Exception as e:
        print(f"Erro ao carregar histórico de irrigação: {e}")
        return []


def salvar_alerta(titulo: str, mensagem: str, severidade: str, sensor_id: str = None) -> bool:
    """Salva um alerta no banco de dados"""
    try:
        db = DatabaseManager(DB_FASE3)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.execute("""
            INSERT INTO alertas (titulo, mensagem, severidade, sensor_id, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (titulo, mensagem, severidade, sensor_id, timestamp))
        db.close()
        return True
    except Exception as e:
        print(f"Erro ao salvar alerta: {e}")
        return False


def carregar_alertas(limite: int = 20) -> List[Dict]:
    """Carrega alertas recentes do banco de dados"""
    try:
        db = DatabaseManager(DB_FASE3)
        rows = db.fetchall("""
            SELECT * FROM alertas
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limite,))

        alertas = []
        for row in rows:
            alertas.append({
                "titulo": row['titulo'],
                "mensagem": row['mensagem'],
                "severidade": row['severidade'],
                "sensor_id": row['sensor_id'],
                "timestamp": row['timestamp']
            })

        db.close()
        return alertas
    except Exception as e:
        print(f"Erro ao carregar alertas: {e}")
        return []


def gerar_leitura_simulada(sensor_id: str, valor_anterior: float = None, estado_irrigacao: str = "normal") -> float:
    """Gera uma leitura simulada para um sensor, simulando variações realistas"""

    if sensor_id == "DHT22_01":  # Umidade
        if valor_anterior is None:
            valor_anterior = 50.0

        # Se está em estado de "pós-irrigação", umidade está subindo
        if estado_irrigacao == "pos_irrigacao":
            # Umidade ainda alta após irrigação
            return random.uniform(65, 85)

        # Simulação realista: solo tende a secar (perder umidade) ao longo do tempo
        # Solo seca continuamente até irrigação
        if valor_anterior > 70:
            # Evaporação muito rápida quando solo muito úmido
            variacao = random.uniform(-8, -5)
        elif valor_anterior > 55:
            # Evaporação rápida
            variacao = random.uniform(-6, -4)
        elif valor_anterior > 40:
            # Evaporação moderada
            variacao = random.uniform(-5, -3)
        else:
            # Evaporação lenta quando próximo do limite crítico
            variacao = random.uniform(-4, -2)

        novo_valor = valor_anterior + variacao

        # Manter entre 15% e 95%
        return max(15, min(95, novo_valor))

    elif sensor_id == "LDR_01":  # pH
        if valor_anterior is None:
            valor_anterior = 6.5

        # pH tende a se auto-regular para a faixa ideal (5.5-7.5)
        # Simula um sistema com capacidade tampão do solo
        if valor_anterior < 5.0:
            # pH muito baixo, forte tendência de subir
            variacao = random.uniform(0.3, 0.6)
        elif valor_anterior < 5.5:
            # Abaixo do ideal, tendência de subir
            variacao = random.uniform(0.1, 0.4)
        elif valor_anterior > 8.0:
            # pH muito alto, forte tendência de descer
            variacao = random.uniform(-0.6, -0.3)
        elif valor_anterior > 7.5:
            # Acima do ideal, tendência de descer
            variacao = random.uniform(-0.4, -0.1)
        else:
            # Dentro da faixa ideal, pequenas variações
            variacao = random.uniform(-0.15, 0.15)

        novo_valor = valor_anterior + variacao
        # Manter entre 5.0 e 8.0 (mais restrito)
        return max(5.0, min(8.0, novo_valor))

    elif sensor_id in ["BTN_FOSFORO", "BTN_POTASSIO"]:  # Nutrientes
        # 92% de chance de estar presente
        return 1.0 if random.random() > 0.08 else 0.0

    return 0.0


def simular_e_salvar_leituras() -> Dict[str, Sensor]:
    """Simula novas leituras e salva no banco de dados"""

    # Carregar sensores com dados existentes
    sensores = carregar_sensores_do_banco()

    # Para cada sensor, gerar uma nova leitura simulada
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Verificar se houve irrigação recente (últimos 2 minutos)
    historico_recente = carregar_historico_irrigacao(limite=1)
    estado_irrigacao = "normal"
    if historico_recente:
        ultima_irrigacao_str = historico_recente[0]['Timestamp']
        try:
            ultima_irrigacao = datetime.strptime(ultima_irrigacao_str, "%Y-%m-%d %H:%M:%S")
            tempo_decorrido = (datetime.now() - ultima_irrigacao).total_seconds()
            # Se irrigou nos últimos 2 minutos, umidade ainda está alta
            if tempo_decorrido < 120:
                estado_irrigacao = "pos_irrigacao"
        except:
            pass

    for sensor_id, sensor in sensores.items():
        # Obter valor anterior para simular mudança gradual
        valor_anterior = sensor.ultima_leitura() if sensor.leituras else None

        # Gerar nova leitura simulada
        novo_valor = gerar_leitura_simulada(sensor_id, valor_anterior, estado_irrigacao)

        # Adicionar ao sensor
        leitura = sensor.adicionar_leitura(novo_valor, timestamp)

        # Determinar status
        status = sensor.status()

        # Salvar no banco de dados
        salvar_leitura_sensor(leitura, status)

    # Verificar se deve gerar alertas
    alertas = gerar_alertas_sensores(sensores)
    for alerta in alertas:
        salvar_alerta(
            titulo=alerta['titulo'],
            mensagem=alerta['mensagem'],
            severidade=alerta['severidade'],
            sensor_id=sensores["DHT22_01"].sensor_id if alerta['tipo'] == "UMIDADE_BAIXA" else None
        )

    # Verificar irrigação
    umidade = sensores["DHT22_01"].ultima_leitura()
    ph = sensores["LDR_01"].ultima_leitura()
    fosforo = sensores["BTN_FOSFORO"].ultima_leitura() == 1
    potassio = sensores["BTN_POTASSIO"].ultima_leitura() == 1
    nutrientes_presentes = fosforo and potassio

    # Se deve irrigar, salvar no banco
    if umidade < 40 and (5.5 <= ph <= 7.5) and nutrientes_presentes:
        motivo = f"Umidade baixa ({umidade:.1f}%), pH ideal ({ph:.2f}), nutrientes OK"
        salvar_irrigacao(timestamp, motivo, duracao_minutos=15)

    return sensores


def carregar_sensores_do_banco() -> Dict[str, Sensor]:
    """Carrega sensores com dados do banco de dados"""

    sensores = {
        "DHT22_01": Sensor(
            sensor_id="DHT22_01",
            tipo="Umidade/Temperatura",
            unidade="%/°C",
            min_valor=0,
            max_valor=100,
            min_ideal=40,
            max_ideal=80
        ),
        "LDR_01": Sensor(
            sensor_id="LDR_01",
            tipo="pH (LDR)",
            unidade="pH",
            min_valor=3,
            max_valor=9,
            min_ideal=5.5,
            max_ideal=7.5
        ),
        "BTN_FOSFORO": Sensor(
            sensor_id="BTN_FOSFORO",
            tipo="Fósforo",
            unidade="Presente/Ausente",
            min_valor=0,
            max_valor=1,
            min_ideal=1,
            max_ideal=1
        ),
        "BTN_POTASSIO": Sensor(
            sensor_id="BTN_POTASSIO",
            tipo="Potássio",
            unidade="Presente/Ausente",
            min_valor=0,
            max_valor=1,
            min_ideal=1,
            max_ideal=1
        ),
    }

    # Carregar últimas 24 leituras de cada sensor
    for sensor_id, sensor in sensores.items():
        leituras = carregar_leituras_sensor(sensor_id, limite=24)
        sensor.leituras = leituras

    return sensores


# ===== FUNÇÕES DE GERENCIAMENTO DE CONTATOS =====

def adicionar_contato(nome: str, email: str, telefone: str = None) -> bool:
    """Adiciona um novo contato para notificações"""
    try:
        db = DatabaseManager(DB_FASE3)
        db.execute("""
            INSERT INTO contatos_notificacao (nome, email, telefone)
            VALUES (?, ?, ?)
        """, (nome, email, telefone))
        db.close()
        return True
    except Exception as e:
        print(f"Erro ao adicionar contato: {e}")
        return False


def remover_contato(contato_id: int) -> bool:
    """Remove um contato"""
    try:
        db = DatabaseManager(DB_FASE3)
        db.execute("DELETE FROM contatos_notificacao WHERE id = ?", (contato_id,))
        db.close()
        return True
    except Exception as e:
        print(f"Erro ao remover contato: {e}")
        return False


def listar_contatos_ativos() -> List[Dict]:
    """Lista todos os contatos ativos"""
    try:
        db = DatabaseManager(DB_FASE3)
        rows = db.fetchall("""
            SELECT * FROM contatos_notificacao
            WHERE ativo = 1
            ORDER BY nome
        """)

        contatos = []
        for row in rows:
            contatos.append({
                "id": row['id'],
                "nome": row['nome'],
                "email": row['email'],
                "telefone": row['telefone'] or "-"
            })

        db.close()
        return contatos
    except Exception as e:
        print(f"Erro ao listar contatos: {e}")
        return []


def contar_contatos_ativos() -> int:
    """Retorna o número de contatos ativos"""
    try:
        db = DatabaseManager(DB_FASE3)
        result = db.fetchone("SELECT COUNT(*) as total FROM contatos_notificacao WHERE ativo = 1")
        db.close()
        return result['total'] if result else 0
    except Exception as e:
        print(f"Erro ao contar contatos: {e}")
        return 0
