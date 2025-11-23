class DadoSensorService:
    def __init__(self, db):
        self.db = db

    def cadastrar(self, dado_sensor):
        data = {
            'id_sensor': dado_sensor.id_sensor,
            'data_hora_leitura': dado_sensor.data_hora_leitura,
            'valor_sensor': dado_sensor.valor_sensor
        }
        return self.db.insert('dados_sensores', data)

    def listar_todos(self):
        query = """
                SELECT ds.id_dado_sensor, ds.id_sensor, ds.data_hora_leitura, ds.valor_sensor,
                       s.nome as nome_sensor, p.nome as nome_plantacao
                FROM dados_sensores ds
                         JOIN sensores s ON ds.id_sensor = s.id_sensor
                         JOIN plantacoes p ON s.id_plantacao = p.id_plantacao
                ORDER BY ds.data_hora_leitura DESC \
                """
        return self.db.fetch_all(query)

    def listar_por_sensor(self, id_sensor):
        query = """
                SELECT ds.id_dado_sensor, ds.id_sensor, ds.data_hora_leitura, ds.valor_sensor,
                       s.nome as nome_sensor, p.nome as nome_plantacao
                FROM dados_sensores ds
                         JOIN sensores s ON ds.id_sensor = s.id_sensor
                         JOIN plantacoes p ON s.id_plantacao = p.id_plantacao
                WHERE ds.id_sensor = %s
                ORDER BY ds.data_hora_leitura DESC \
                """
        return self.db.fetch_all(query, (id_sensor,))

    def listar_por_plantacao(self, id_plantacao):
        query = """
                SELECT ds.id_dado_sensor, ds.id_sensor, ds.data_hora_leitura, ds.valor_sensor,
                       s.nome as nome_sensor, p.nome as nome_plantacao
                FROM dados_sensores ds
                         JOIN sensores s ON ds.id_sensor = s.id_sensor
                         JOIN plantacoes p ON s.id_plantacao = p.id_plantacao
                WHERE s.id_plantacao = %s
                ORDER BY ds.data_hora_leitura DESC \
                """
        return self.db.fetch_all(query, (id_plantacao,))

    def buscar_por_id(self, id_dado_sensor):
        query = """
                SELECT ds.id_dado_sensor, ds.id_sensor, ds.data_hora_leitura, ds.valor_sensor,
                       s.nome as nome_sensor, p.nome as nome_plantacao
                FROM dados_sensores ds
                         JOIN sensores s ON ds.id_sensor = s.id_sensor
                         JOIN plantacoes p ON s.id_plantacao = p.id_plantacao
                WHERE ds.id_dado_sensor = %s \
                """
        return self.db.fetch_one(query, (id_dado_sensor,))

    def atualizar(self, dado_sensor):
        data = {
            'id_sensor': dado_sensor.id_sensor,
            'data_hora_leitura': dado_sensor.data_hora_leitura,
            'valor_sensor': dado_sensor.valor_sensor
        }
        return self.db.update('dados_sensores', data, f"id_dado_sensor = {dado_sensor.id_dado_sensor}")

    def excluir(self, id_dado_sensor):
        return self.db.delete('dados_sensores', f"id_dado_sensor = {id_dado_sensor}")