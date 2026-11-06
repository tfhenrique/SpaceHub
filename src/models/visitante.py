from datetime import date, datetime


class Visitante:

    def __init__(self, membro_id, nome, empresa=None, data_visita=None,
                 hora_entrada=None, hora_saida=None, id=None):
        self.id = id
        self.membro_id = membro_id
        self.nome = nome
        self.empresa = empresa
        self.data_visita = data_visita or date.today()
        self.hora_entrada = hora_entrada or datetime.now().time().replace(microsecond=0)
        self.hora_saida = hora_saida