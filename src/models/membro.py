from datetime import date, timedelta

class Membro:
    def __init__(
        self,
        id=None,
        nome=None,
        empresa=None,
        nif=000000000,
        email="",
        telemovel=000000000,
        plano_id=0,
        data_inicio=None,
        data_fim=None,
        ativo=True
        ):
        self.id = id
        self.nome = nome
        self.empresa = empresa
        self.nif = nif
        self.email = email
        self.telemovel = telemovel
        self.plano_id = plano_id
        self.data_inicio = data_inicio if data_inicio else date.today()
        self.data_fim = data_fim if data_fim else (self.data_inicio + timedelta(days=30))
        self.ativo = ativo