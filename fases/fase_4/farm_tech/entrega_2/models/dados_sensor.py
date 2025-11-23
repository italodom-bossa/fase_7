class DadoSensor:
    def __init__(self, id_sensor, data_hora_leitura, valor_sensor, id_dado_sensor=None):
        self.id_dado_sensor = id_dado_sensor
        self.id_sensor = id_sensor
        self.data_hora_leitura = data_hora_leitura
        self.valor_sensor = valor_sensor
    
    def to_dict(self):
        return {
            'id_sensor': self.id_sensor,
            'data_hora_leitura': self.data_hora_leitura,
            'valor_sensor': self.valor_sensor
        }