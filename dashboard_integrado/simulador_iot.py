"""
Simulador IoT em Background
Gera leituras de sensores automaticamente e salva no banco de dados
FarmTech Solutions - Dashboard Integrado
"""

import time
import random
from datetime import datetime
import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.append(str(Path(__file__).parent))

from servicos.database import DatabaseManager, DB_FASE3, init_fase3_db


class SimuladorSensores:
    """Simula leituras de sensores em tempo real"""

    def __init__(self):
        self.db = DatabaseManager(DB_FASE3)
        init_fase3_db()

        # Estado dos sensores
        self.umidade = 65.0
        self.ph = 6.5
        self.fosforo = 1
        self.potassio = 1

        # Tendências
        self.tendencia_umidade = random.choice([-1, 1])
        self.tendencia_ph = random.choice([-0.1, 0.1])

    def simular_umidade(self) -> float:
        """Simula leitura de umidade com variação realista"""
        # Variação gradual
        self.umidade += random.uniform(-2, 2) + (self.tendencia_umidade * 0.5)

        # Manter dentro de limites realistas
        self.umidade = max(20, min(95, self.umidade))

        # Mudar tendência ocasionalmente
        if random.random() < 0.1:
            self.tendencia_umidade *= -1

        return round(self.umidade, 1)

    def simular_ph(self) -> float:
        """Simula leitura de pH com variação realista"""
        # Variação gradual
        self.ph += random.uniform(-0.2, 0.2) + self.tendencia_ph

        # Manter dentro de limites realistas
        self.ph = max(4.0, min(9.0, self.ph))

        # Mudar tendência ocasionalmente
        if random.random() < 0.1:
            self.tendencia_ph *= -1

        return round(self.ph, 2)

    def simular_nutriente(self, atual: int) -> int:
        """Simula presença de nutriente (0 ou 1)"""
        # 95% de chance de manter o estado atual
        if random.random() < 0.95:
            return atual
        # 5% de chance de mudar
        return 1 - atual

    def salvar_leitura(self, sensor_id: str, tipo: str, valor: float, unidade: str):
        """Salva leitura no banco de dados"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determinar status
        status = "Normal"
        if tipo == "Umidade":
            if valor < 40:
                status = "Baixo"
            elif valor > 80:
                status = "Alto"
        elif tipo == "pH":
            if valor < 5.5 or valor > 7.5:
                status = "Fora do ideal"
        elif tipo in ["Fósforo", "Potássio"]:
            status = "Presente" if valor == 1 else "Ausente"

        try:
            self.db.execute("""
                INSERT INTO leituras_sensores (sensor_id, tipo_sensor, valor, unidade, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (sensor_id, tipo, valor, unidade, timestamp, status))
        except Exception as e:
            print(f"Erro ao salvar leitura: {e}")

    def obter_contatos(self):
        """Obtém lista de contatos ativos do banco"""
        try:
            rows = self.db.fetchall("""
                SELECT nome, email, telefone FROM contatos_notificacao WHERE ativo = 1
            """)
            return rows
        except:
            return []

    def gerar_alerta(self, titulo: str, mensagem: str, severidade: str, sensor_id: str = None):
        """Gera um alerta no banco de dados"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.db.execute("""
                INSERT INTO alertas (titulo, mensagem, severidade, sensor_id, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (titulo, mensagem, severidade, sensor_id, timestamp))

            print(f"🚨 ALERTA: {titulo}")

            # Verificar se há contatos cadastrados
            contatos = self.obter_contatos()

            if contatos:
                print(f"   📧 E-mail enviado via AWS SNS para {len(contatos)} contato(s):")
                for contato in contatos:
                    print(f"      ✅ {contato['nome']} - {contato['email']}")
            else:
                print(f"   ❌ Notificação NÃO enviada - Sem contatos cadastrados!")
                print(f"   ⚠️  Acesse a aba 📇 Contatos no dashboard para adicionar destinatários")

        except Exception as e:
            print(f"Erro ao gerar alerta: {e}")

    def verificar_alertas(self, umidade: float, ph: float, fosforo: int, potassio: int):
        """Verifica se deve gerar alertas"""
        # Alerta de umidade crítica
        if umidade < 30:
            self.gerar_alerta(
                "🚨 Umidade Crítica",
                f"Umidade muito baixa: {umidade:.1f}% - Irrigação urgente necessária!",
                "crítico",
                "DHT22_01"
            )
        elif umidade < 40:
            self.gerar_alerta(
                "⚠️ Umidade Baixa",
                f"Umidade abaixo do ideal: {umidade:.1f}% - Considere irrigação",
                "alto",
                "DHT22_01"
            )
        elif umidade > 85:
            self.gerar_alerta(
                "⚠️ Umidade Alta",
                f"Umidade acima do ideal: {umidade:.1f}% - Risco de doenças",
                "alto",
                "DHT22_01"
            )

        # Alerta de pH
        if ph < 5.0 or ph > 8.0:
            self.gerar_alerta(
                "🚨 pH Crítico",
                f"pH fora da faixa segura: {ph:.2f} - Correção urgente necessária!",
                "crítico",
                "LDR_01"
            )
        elif ph < 5.5 or ph > 7.5:
            self.gerar_alerta(
                "⚠️ pH Fora do Ideal",
                f"pH fora do ideal: {ph:.2f} - Recomenda-se correção",
                "médio",
                "LDR_01"
            )

        # Alerta de nutrientes
        if fosforo == 0:
            self.gerar_alerta(
                "⚠️ Fósforo Ausente",
                "Fósforo não detectado - Aplicação de fertilizante necessária",
                "alto",
                "BTN_FOSFORO"
            )

        if potassio == 0:
            self.gerar_alerta(
                "⚠️ Potássio Ausente",
                "Potássio não detectado - Aplicação de fertilizante necessária",
                "alto",
                "BTN_POTASSIO"
            )

    def verificar_irrigacao(self, umidade: float, ph: float, fosforo: int, potassio: int):
        """Verifica se deve acionar irrigação automática"""
        if umidade < 40 and 5.5 <= ph <= 7.5 and fosforo == 1 and potassio == 1:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                self.db.execute("""
                    INSERT INTO historico_irrigacao (timestamp, motivo, duracao_minutos)
                    VALUES (?, ?, ?)
                """, (timestamp, "Acionamento automático - Umidade baixa", 15))
                print(f"💧 IRRIGAÇÃO ACIONADA às {timestamp}")
            except Exception as e:
                print(f"Erro ao registrar irrigação: {e}")

    def executar_ciclo(self):
        """Executa um ciclo de leitura dos sensores"""
        # Simular leituras
        umidade = self.simular_umidade()
        ph = self.simular_ph()
        self.fosforo = self.simular_nutriente(self.fosforo)
        self.potassio = self.simular_nutriente(self.potassio)

        # Salvar leituras
        self.salvar_leitura("DHT22_01", "Umidade", umidade, "%")
        self.salvar_leitura("LDR_01", "pH", ph, "")
        self.salvar_leitura("BTN_FOSFORO", "Fósforo", self.fosforo, "")
        self.salvar_leitura("BTN_POTASSIO", "Potássio", self.potassio, "")

        # Verificar alertas (apenas ocasionalmente para não encher o banco)
        if random.random() < 0.2:
            self.verificar_alertas(umidade, ph, self.fosforo, self.potassio)

        # Verificar irrigação
        self.verificar_irrigacao(umidade, ph, self.fosforo, self.potassio)

        # Log
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Umidade: {umidade:.1f}% | pH: {ph:.2f} | P: {self.fosforo} | K: {self.potassio}")

    def limpar_dados_antigos(self):
        """Remove leituras antigas (mais de 24h)"""
        try:
            self.db.execute("""
                DELETE FROM leituras_sensores
                WHERE datetime(created_at) < datetime('now', '-24 hours')
            """)
            self.db.execute("""
                DELETE FROM alertas
                WHERE datetime(created_at) < datetime('now', '-24 hours')
            """)
        except Exception as e:
            print(f"Erro ao limpar dados antigos: {e}")

    def rodar(self, intervalo_segundos: int = 5):
        """Roda o simulador continuamente"""
        print("🤖 Simulador IoT iniciado!")
        print(f"📊 Gerando leituras a cada {intervalo_segundos} segundos")
        print("⏹️  Pressione Ctrl+C para parar\n")

        ciclo = 0
        try:
            while True:
                self.executar_ciclo()

                # Limpar dados antigos a cada 100 ciclos
                ciclo += 1
                if ciclo % 100 == 0:
                    self.limpar_dados_antigos()
                    print("🧹 Dados antigos removidos")

                time.sleep(intervalo_segundos)

        except KeyboardInterrupt:
            print("\n\n⏹️  Simulador parado pelo usuário")
        finally:
            self.db.close()
            print("✅ Conexão com banco de dados encerrada")


if __name__ == "__main__":
    # Intervalo entre leituras (em segundos)
    INTERVALO = 5  # 5 segundos para demonstração

    simulador = SimuladorSensores()
    simulador.rodar(INTERVALO)
