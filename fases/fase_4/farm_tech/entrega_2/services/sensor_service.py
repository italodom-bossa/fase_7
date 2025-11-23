class SensorService:
    def __init__(self, db):
        self.db = db

    def cadastrar(self, sensor):
        data = {
            'id_plantacao': sensor.id_plantacao,
            'nome': sensor.nome,
            'data_instalacao': sensor.data_instalacao
        }
        return self.db.insert('sensores', data)

    def listar_todos(self):
        query = """
                SELECT s.id_sensor, s.id_plantacao, s.nome, s.data_instalacao, p.nome as nome_plantacao
                FROM sensores s
                         JOIN plantacoes p ON s.id_plantacao = p.id_plantacao
                ORDER BY s.nome \
                """
        return self.db.fetch_all(query)

    def listar_por_plantacao(self, id_plantacao):
        query = """
                SELECT s.id_sensor, s.id_plantacao, s.nome, s.data_instalacao, p.nome as nome_plantacao
                FROM sensores s
                         JOIN plantacoes p ON s.id_plantacao = p.id_plantacao
                WHERE s.id_plantacao = %s
                ORDER BY s.nome \
                """
        return self.db.fetch_all(query, (id_plantacao,))

    def buscar_por_id(self, id_sensor):
        query = """
                SELECT s.id_sensor, s.id_plantacao, s.nome, s.data_instalacao, p.nome as nome_plantacao
                FROM sensores s
                         JOIN plantacoes p ON s.id_plantacao = p.id_plantacao
                WHERE s.id_sensor = %s \
                """
        return self.db.fetch_one(query, (id_sensor,))

    def atualizar(self, sensor):
        data = {
            'id_plantacao': sensor.id_plantacao,
            'nome': sensor.nome,
            'data_instalacao': sensor.data_instalacao
        }
        return self.db.update('sensores', data, f"id_sensor = {sensor.id_sensor}")

    def excluir(self, id_sensor):
        return self.db.delete('sensores', f"id_sensor = {id_sensor}")