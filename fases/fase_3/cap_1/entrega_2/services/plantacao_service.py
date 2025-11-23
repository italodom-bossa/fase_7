class PlantacaoService:
    def __init__(self, db):
        self.db = db

    def cadastrar(self, plantacao):
        data = {
            'nome': plantacao.nome,
            'localizacao': plantacao.localizacao,
            'data_plantio': plantacao.data_plantio
        }
        return self.db.insert('plantacoes', data)

    def listar_todos(self):
        query = "SELECT id_plantacao, nome, localizacao, data_plantio FROM plantacoes ORDER BY nome"
        return self.db.fetch_all(query)

    def buscar_por_id(self, id_plantacao):
        query = "SELECT id_plantacao, nome, localizacao, data_plantio FROM plantacoes WHERE id_plantacao = %s"
        return self.db.fetch_one(query, (id_plantacao,))

    def atualizar(self, plantacao):
        data = {
            'nome': plantacao.nome,
            'localizacao': plantacao.localizacao,
            'data_plantio': plantacao.data_plantio
        }
        return self.db.update('plantacoes', data, f"id_plantacao = {plantacao.id_plantacao}")

    def excluir(self, id_plantacao):
        return self.db.delete('plantacoes', f"id_plantacao = {id_plantacao}")