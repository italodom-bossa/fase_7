from src.persistencia.base_repository import BaseRepository
import oracledb
import json
from datetime import datetime

class OracleRepository(BaseRepository):
    def __init__(self, connection_string, tabela):
        self.connection_string = connection_string
        self.tabela = tabela

    async def _obter_conexao(self):
        try:
            conn = oracledb.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'")
            cursor.close()
            return conn
        except Exception as e:
            print(f"Erro ao conectar ao banco Oracle: {e}")
            raise

    def _processar_valores(self, dados):
        processados = {}
        for chave, valor in dados.items():
            if isinstance(valor, dict):
                processados[chave] = json.dumps(valor)
            else:
                processados[chave] = valor
        return processados

    async def inserir(self, entidade):
        conexao = await self._obter_conexao()
        cursor = conexao.cursor()

        try:
            entidade_copia = dict(entidade)

            if 'data' in entidade_copia and entidade_copia['data']:
                if isinstance(entidade_copia['data'], str) and '/' in entidade_copia['data']:
                    try:
                        data_obj = datetime.strptime(entidade_copia['data'], '%d/%m/%Y')
                        entidade_copia['data'] = data_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        print(f"Data inválida: {entidade_copia['data']}. Usando NULL.")
                        entidade_copia['data'] = None

            dados_processados = self._processar_valores(entidade_copia)

            colunas = ", ".join(dados_processados.keys())
            placeholders = ", ".join([f":{i+1}" for i in range(len(dados_processados))])

            query = f"INSERT INTO {self.tabela} ({colunas}) VALUES ({placeholders})"

            cursor.execute(query, list(dados_processados.values()))
            conexao.commit()
            return True
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao inserir dados: {e}")
            raise
        finally:
            cursor.close()
            conexao.close()

    async def listar(self):
        conexao = await self._obter_conexao()
        cursor = conexao.cursor()

        try:
            query = f"SELECT * FROM {self.tabela}"
            cursor.execute(query)

            colunas = [coluna[0].lower() for coluna in cursor.description]
            resultado = []

            for linha in cursor:
                item = dict(zip(colunas, linha))

                for chave, valor in list(item.items()):
                    if isinstance(valor, str) and valor.startswith('{') and valor.endswith('}'):
                        try:
                            item[chave] = json.loads(valor)
                        except json.JSONDecodeError:
                            pass

                    if chave.lower() == 'data' and valor is not None:
                        if hasattr(valor, 'strftime'):
                            item[chave] = valor.strftime('%d/%m/%Y')
                        elif isinstance(valor, str) and '-' in valor:
                            try:
                                data_obj = datetime.strptime(valor, '%Y-%m-%d')
                                item[chave] = data_obj.strftime('%d/%m/%Y')
                            except ValueError:
                                pass

                resultado.append(item)

            return resultado
        except Exception as e:
            print(f"Erro ao listar dados: {e}")
            raise
        finally:
            cursor.close()
            conexao.close()

    async def atualizar(self, id, novos_dados):
        conexao = await self._obter_conexao()
        cursor = conexao.cursor()

        try:
            dados_copia = dict(novos_dados)

            if 'data' in dados_copia and dados_copia['data']:
                if isinstance(dados_copia['data'], str) and '/' in dados_copia['data']:
                    try:
                        data_obj = datetime.strptime(dados_copia['data'], '%d/%m/%Y')
                        dados_copia['data'] = data_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        print(f"Data inválida: {dados_copia['data']}. Usando NULL.")
                        dados_copia['data'] = None

            dados_processados = self._processar_valores(dados_copia)

            set_clause = ", ".join([f"{coluna} = :{i+1}" for i, coluna in enumerate(dados_processados.keys())])

            query = f"UPDATE {self.tabela} SET {set_clause} WHERE id = :{len(dados_processados)+1}"

            params = list(dados_processados.values()) + [id]
            cursor.execute(query, params)

            afetados = cursor.rowcount
            conexao.commit()

            return afetados > 0
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao atualizar dados: {e}")
            raise
        finally:
            cursor.close()
            conexao.close()

    async def deletar(self, id):
        conexao = await self._obter_conexao()
        cursor = conexao.cursor()

        try:
            query = f"DELETE FROM {self.tabela} WHERE id = :1"
            cursor.execute(query, [id])

            afetados = cursor.rowcount
            conexao.commit()

            return afetados > 0
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao deletar dados: {e}")
            raise
        finally:
            cursor.close()
            conexao.close()