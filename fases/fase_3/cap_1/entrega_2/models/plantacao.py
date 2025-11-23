class Plantacao:
    def __init__(self, nome, localizacao, data_plantio, id_plantacao=None):
        self.id_plantacao = id_plantacao
        self.nome = nome
        self.localizacao = localizacao
        self.data_plantio = data_plantio
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'localizacao': self.localizacao,
            'data_plantio': self.data_plantio
        }