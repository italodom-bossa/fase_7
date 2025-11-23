class Sensor:
    def __init__(self, id_plantacao, nome, data_instalacao, id_sensor=None):
        self.id_sensor = id_sensor
        self.id_plantacao = id_plantacao
        self.nome = nome
        self.data_instalacao = data_instalacao
    
    def to_dict(self):
        return {
            'id_plantacao': self.id_plantacao,
            'nome': self.nome,
            'data_instalacao': self.data_instalacao
        }